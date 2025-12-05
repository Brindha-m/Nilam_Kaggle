"""
Chat Agent - LLM-powered conversational agent for agricultural queries
"""
import uuid

# ADK imports - wrapped in try/except for optional installation
try:
    from google.adk.agents import LlmAgent
    from google.adk.models.google_llm import Gemini
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
    from google.adk.tools.tool_context import ToolContext
    from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
    from mcp import StdioServerParameters
    from google.adk.apps.app import App, ResumabilityConfig
    from google.adk.tools.function_tool import FunctionTool
    ADK_AVAILABLE = True
    print("✅ ADK components imported successfully.")
except ImportError:
    # ADK not installed - set to None for optional usage
    LlmAgent = None
    Gemini = None
    Runner = None
    InMemorySessionService = None
    McpToolset = None
    ToolContext = None
    StdioConnectionParams = None
    StdioServerParameters = None
    App = None
    ResumabilityConfig = None
    FunctionTool = None
    ADK_AVAILABLE = False
    print("⚠️ ADK components not available. Install google-adk package to use ADK features.")

from typing import Dict, Any
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
        # Store API key for later use
        self.api_key = api_key
        
        # Initialize LLM - use google-generativeai for compatibility
        # ADK components are imported but Gemini model is used differently in ADK
        # For direct content generation, we use google-generativeai
        if api_key and not llm_model:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                llm_model = genai.GenerativeModel("gemini-2.5-flash")
            except Exception as e:
                print(f"Error initializing Gemini: {e}")
                llm_model = None
        
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
            
            # Generate response using LLM
            if self.llm_model:
                try:
                    # Use standard google-generativeai API
                    response = self.llm_model.generate_content(prompt)
                    response_text = response.text
                except Exception as e:
                    print(f"Error generating content: {e}")
                    response_text = "I encountered an error generating a response."
            else:
                response_text = "I'm a chat agent. Please configure the LLM model to get responses."
            
            # Check if tools need to be used
            if any(keyword in response_text.lower() for keyword in ['search', 'calculate', 'compute']):
                # Try to use tools if needed
                if 'search' in response_text.lower():
                    try:
                        search_result = self.execute_tool("google_search", {"query": message.content})
                        formatted_search = self._format_search_results(search_result)
                        response_text += formatted_search
                    except:
                        pass
            
            # Format code blocks with white color and remove demo links
            response_text = self._format_code_blocks(response_text)
            response_text = self._remove_demo_links(response_text)
            
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
        """Format search results in a readable way"""
        if isinstance(search_result, dict) and "results" in search_result:
            formatted = "\n\n### 🔍 Search Results\n\n"
            results = search_result.get("results", [])
            for i, result in enumerate(results[:3], 1):  # Show top 3 results
                title = result.get("title", "Result")
                snippet = result.get("snippet", "")
                url = result.get("url", "")
                
                # Clean up title (remove query prefix if present)
                if "Result" in title and "for:" in title:
                    title = title.split("for:")[-1].strip()
                
                formatted += f"**{i}. {title}**\n"
                if snippet:
                    # Clean snippet
                    snippet = snippet.replace("Information about", "").strip()
                    if snippet.endswith(" - relevant content here"):
                        snippet = snippet.replace(" - relevant content here", "").strip()
                    formatted += f"{snippet}\n"
                if url and url != "https://example.com/result":
                    formatted += f"🔗 {url}\n"
                formatted += "\n"
            return formatted
        elif isinstance(search_result, str):
            # If it's already a string, try to parse it
            if "Search Results:" in search_result:
                return f"\n\n### 🔍 Additional Information\n\n{search_result.replace('[Search Results:', '').replace(']', '')}\n"
        return ""
    
    def _format_code_blocks(self, text: str) -> str:
        """Format code blocks with grey background and white text"""
        import re
        
        # Format code blocks (triple backticks) with grey background
        def format_code_block(match):
            lang = match.group(1) or ''
            code_content = match.group(2).strip()
            # Display code with grey background, not the markdown syntax
            return f'<div style="background-color: #2d2d2d; padding: 1rem; border-radius: 5px; overflow-x: auto; margin: 1rem 0; border: 1px solid #444;"><pre style="margin: 0; color: white; font-family: monospace; white-space: pre-wrap; word-wrap: break-word; font-size: 14px;"><code style="color: white;">{code_content}</code></pre></div>'
        
        # Match code blocks and format them
        text = re.sub(
            r'```(\w+)?\n(.*?)```',
            format_code_block,
            text,
            flags=re.DOTALL
        )
        
        # Format inline code (single backticks) with grey background
        text = re.sub(
            r'`([^`]+)`',
            r'<code style="background-color: #2d2d2d; color: white; padding: 2px 6px; border-radius: 3px; font-family: monospace; font-size: 14px;">\1</code>',
            text
        )
        
        return text
    
    def _remove_demo_links(self, text: str) -> str:
        """Remove demo links and example URLs from response"""
        import re
        
        # Remove demo/example URLs
        text = re.sub(r'https?://(?:www\.)?(?:demo|example|test|localhost)[^\s\)]+', '', text, flags=re.IGNORECASE)
        
        # Remove lines containing demo links
        lines = text.split('\n')
        filtered_lines = []
        for line in lines:
            # Skip lines that are just demo links or contain demo/example URLs
            if re.search(r'(demo|example|test)\.(com|org|net|io)', line, re.IGNORECASE):
                continue
            # Skip lines that are just URLs pointing to demo/example sites
            if re.match(r'^\s*https?://(?:www\.)?(?:demo|example|test)', line, re.IGNORECASE):
                continue
            filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)
    
    def _build_prompt(self, user_message: str, history: list, context: AgentContext) -> str:
        """Build prompt with context and history"""
        prompt = """You are Dr. Agricultural Expert, India's leading farming consultant with 25+ years experience.
Provide concise, actionable responses with deep insights and data-driven analysis.

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
        prompt += "Provide a helpful, accurate response:"
        
        return prompt
