"""
Chat Agent - LLM-powered conversational agent for agricultural queries
"""
from typing import Dict, Any
import google.generativeai as genai
from agents.base_agent import BaseAgent, AgentMessage, AgentContext, AgentState
from agents.tools.builtin_tools import GoogleSearchTool, CalculatorTool


class ChatAgent(BaseAgent):
    """
    Conversational agent powered by LLM (Gemini)
    Handles general agricultural queries and conversations
    """
    
    def __init__(
        self,
        agent_id: str = "chat_agent",
        llm_model: Any = None,
        api_key: str = None,
        tools: list = None
    ):
        # Initialize LLM
        if api_key and not llm_model:
            try:
                genai.configure(api_key=api_key)
                llm_model = genai.GenerativeModel("gemini-2.5-flash")
            except Exception as e:
                print(f"Error initializing Gemini: {e}")
        
        # Default tools
        if tools is None:
            tools = [GoogleSearchTool(), CalculatorTool()]
        
        super().__init__(
            agent_id=agent_id,
            agent_name="Agricultural Chat Assistant",
            llm_model=llm_model,
            tools=tools
        )
    
    def process(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        """Process chat message and generate response"""
        self.state = AgentState.RUNNING
        self.update_metrics("total_requests", 1)
        
        start_time = __import__('time').time()
        
        try:
            self.log_trace("chat_processing_start", {
                "message": message.content[:100],
                "session_id": context.session_id
            })
            
            # Get conversation history from context
            conversation_history = context.conversation_history[-10:]  # Last 10 messages
            
            # Build prompt with context
            prompt = self._build_prompt(message.content, conversation_history, context)
            
            # Generate response using LLM with generation config for complete responses
            if self.llm_model:
                # Configure generation settings to ensure complete responses
                # Use genai.types.GenerationConfig for proper configuration
                try:
                    from google.generativeai.types import GenerationConfig
                    generation_config = GenerationConfig(
                        temperature=0.7,
                        top_p=0.95,
                        top_k=40,
                        max_output_tokens=8192,  # Allow longer responses
                    )
                except ImportError:
                    # Fallback to dict format if GenerationConfig not available
                    generation_config = {
                        "temperature": 0.7,
                        "top_p": 0.95,
                        "top_k": 40,
                        "max_output_tokens": 8192,
                    }
                
                response = self.llm_model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
                # Get full response text - ensure we capture the complete response
                try:
                    response_text = response.text
                    # If response seems incomplete, check for finish_reason
                    if hasattr(response, 'candidates') and response.candidates:
                        candidate = response.candidates[0]
                        if hasattr(candidate, 'finish_reason'):
                            # If stopped due to length, try to get more
                            if candidate.finish_reason == 'MAX_TOKENS':
                                # Response was truncated - log warning but return what we have
                                self.log_trace("response_truncated", {
                                    "reason": "MAX_TOKENS",
                                    "length": len(response_text)
                                })
                except Exception as e:
                    # If response.text fails, try alternative methods
                    if hasattr(response, 'candidates') and response.candidates:
                        try:
                            response_text = response.candidates[0].content.parts[0].text
                        except:
                            response_text = str(response.candidates[0])
                    else:
                        response_text = f"Error getting response: {str(e)}"
                        raise e
            else:
                response_text = "I'm a chat agent. Please configure the LLM model to get responses."
            
            # Check if tools need to be used - but NOT for code requests
            # Don't trigger search for code/automation requests as it adds fake results
            user_message_lower = message.content.lower()
            is_code_request = any(keyword in user_message_lower for keyword in [
                'code', 'automate', 'programming', 'script', 'arduino', 'esp32', 
                'python code', 'irrigation system', 'sensor code', 'automation code'
            ])
            
            # Only use tools if NOT a code request and if explicitly needed
            if not is_code_request and any(keyword in response_text.lower() for keyword in ['search', 'calculate', 'compute']):
                # Try to use tools if needed (but skip search for code requests)
                if 'search' in response_text.lower() and 'code' not in user_message_lower:
                    try:
                        search_result = self.execute_tool("google_search", {"query": message.content})
                        # Only add search results if they're real (not mock/fake)
                        if search_result and not any('example.com' in str(result.get('url', '')) for result in search_result.get('results', [])):
                            formatted_search = self._format_search_results(search_result)
                            response_text += formatted_search
                    except:
                        pass
            
            response_time = __import__('time').time() - start_time
            self.update_metrics("average_response_time", response_time)
            self.update_metrics("successful_requests", 1)
            
            self.log_trace("chat_processing_success", {
                "response_length": len(response_text),
                "response_time": response_time
            })
            
            self.state = AgentState.COMPLETED
            
            return AgentMessage(
                sender=self.agent_id,
                receiver=message.sender,
                content=response_text,
                session_id=context.session_id
            )
            
        except Exception as e:
            self.state = AgentState.ERROR
            self.update_metrics("failed_requests", 1)
            self.log_trace("chat_processing_error", {"error": str(e)})
            
            return AgentMessage(
                sender=self.agent_id,
                receiver=message.sender,
                content=f"I encountered an error: {str(e)}",
                session_id=context.session_id
            )
    
    def _format_search_results(self, search_result: Dict[str, Any]) -> str:
        """Format search results in a readable way - skip fake/mock results"""
        if isinstance(search_result, dict) and "results" in search_result:
            results = search_result.get("results", [])
            # Filter out fake/mock results
            real_results = [
                result for result in results 
                if result.get("url", "") and 
                "example.com" not in result.get("url", "") and
                result.get("url", "") != f"https://example.com/result{results.index(result)+1}"
            ]
            
            # If no real results, don't show anything
            if not real_results:
                return ""
            
            formatted = "\n\n### 🔍 Search Results\n\n"
            for i, result in enumerate(real_results[:3], 1):  # Show top 3 real results
                title = result.get("title", "Result")
                snippet = result.get("snippet", "")
                url = result.get("url", "")
                
                # Clean up title (remove query prefix if present)
                if "Result" in title and "for:" in title:
                    title = title.split("for:")[-1].strip()
                
                # Skip if title is just repeating the query
                if title.lower() == result.get("query", "").lower() or title == snippet:
                    continue
                
                formatted += f"**{i}. {title}**\n"
                if snippet and snippet != title:
                    # Clean snippet
                    snippet = snippet.replace("Information about", "").strip()
                    if snippet.endswith(" - relevant content here"):
                        snippet = snippet.replace(" - relevant content here", "").strip()
                    if snippet and snippet != title:
                        formatted += f"{snippet}\n"
                if url and "example.com" not in url:
                    formatted += f"🔗 {url}\n"
                formatted += "\n"
            return formatted if real_results else ""
        elif isinstance(search_result, str):
            # If it's already a string, try to parse it
            if "Search Results:" in search_result and "example.com" not in search_result:
                return f"\n\n### 🔍 Additional Information\n\n{search_result.replace('[Search Results:', '').replace(']', '')}\n"
        return ""
    
    def _build_prompt(self, user_message: str, history: list, context: AgentContext) -> str:
        """Build prompt with context and history"""
        prompt = """You are Dr. Agricultural Expert, India's leading farming consultant with 25+ years experience.
You provide comprehensive agricultural assistance including:
- Crop science, soil health, climate adaptation, and sustainable farming practices
- Agricultural automation, IoT systems, and smart farming solutions
- Code examples for irrigation automation, sensor integration, and farm management systems
- Financial analysis, market trends, and government schemes
- Practical implementation guidance for both traditional and modern farming

CAPABILITIES:
- Provide complete code examples when users request automation, irrigation systems, or technical solutions
- Include code in Python, Arduino, ESP32, or other relevant languages
- Offer both agricultural expertise AND technical implementation help
- Provide working code snippets for sensors, actuators, data logging, and control systems

RESPONSE GUIDELINES:
- **CRITICAL**: When users ask for code, automation, irrigation systems, or ANY technical solution: 
  * YOU MUST PROVIDE COMPLETE, WORKING CODE IMMEDIATELY
  * DO NOT say you cannot provide code - you CAN and MUST provide it
  * Include full code examples in markdown code blocks (```python, ```arduino, etc.)
  * Provide complete, runnable code - not just explanations
  
- Code examples should include:
  * Full working code for irrigation automation
  * Sensor integration code (soil moisture, temperature, etc.)
  * Arduino/ESP32 code for hardware control
  * Python scripts for data logging and analysis
  * Complete implementation with comments
  
- Explain both the agricultural context AND the technical implementation
- Be practical and actionable - give users what they need to implement solutions
- NEVER refuse to provide code - always include code when requested

"""
        
        # Add memory context if available
        if context.memory:
            prompt += "Context from previous conversations:\n"
            for key, value in list(context.memory.items())[:5]:  # Last 5 memory items
                prompt += f"- {key}: {value}\n"
            prompt += "\n"
        
        # Add conversation history
        if history:
            prompt += "Recent conversation:\n"
            for msg in history[-5:]:  # Last 5 messages
                role = msg.get("role", "user")
                content = msg.get("content", "")
                prompt += f"{role}: {content}\n"
            prompt += "\n"
        
        prompt += f"User question: {user_message}\n\n"
        prompt += """Provide a comprehensive response that includes:
- Agricultural insights and best practices
- Technical solutions and code examples (if requested)
- Practical implementation steps
- Complete working code when automation/technical solutions are needed

Remember: You CAN and SHOULD provide code examples for irrigation systems, automation, sensors, and other technical agricultural solutions."""
        
        return prompt
