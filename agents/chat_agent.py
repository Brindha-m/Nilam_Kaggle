"""
Chat Agent - LLM-powered conversational agent for agricultural queries
"""
import uuid
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from google.adk.apps.app import App, ResumabilityConfig
from google.adk.tools.function_tool import FunctionTool
from typing import Dict, Any
import google.generativeai as genai
from agents.base_agent import BaseAgent, AgentMessage, AgentContext, AgentState
from agents.tools.builtin_tools import GoogleSearchTool, CalculatorTool

print("✅ ADK components imported successfully.")


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
        # Initialize LLM using google-generativeai
        # Always use GenerativeModel, not ADK Gemini class
        if api_key:
            try:
                # Using standard google-generativeai library
                genai.configure(api_key=api_key)
                llm_model = genai.GenerativeModel("gemini-2.5-flash")
            except Exception as e:
                print(f"Error initializing Gemini: {e}")
                llm_model = None
        elif llm_model is not None:
            # If llm_model is passed but it's not a GenerativeModel, try to recreate it
            # Check if it's an ADK Gemini object (which doesn't have generate_content)
            if hasattr(llm_model, 'generate') and not hasattr(llm_model, 'generate_content'):
                # This is likely an ADK Gemini object, we need to recreate it
                print("Warning: ADK Gemini object detected. Please provide api_key instead.")
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
                # Ensure we're using GenerativeModel with generate_content method
                if hasattr(self.llm_model, 'generate_content'):
                    response = self.llm_model.generate_content(prompt)
                    response_text = response.text
                else:
                    # Fallback if wrong model type is passed
                    response_text = "Error: LLM model is not properly configured. Please provide a valid API key."
                    self.log_trace("llm_model_error", {"error": "Model does not have generate_content method"})
            else:
                response_text = "I'm a chat agent. Please configure the LLM model to get responses."
            
            # Enhanced tool integration - only use real tools, filter out demo content
            # Use tools for calculations and real-time data, but skip demo search results
            if any(keyword in message.content.lower() for keyword in ['calculate', 'compute', 'roi', 'profit', 'cost']):
                try:
                    # Use calculator for financial analysis
                    if 'calculate' in message.content.lower() or 'compute' in message.content.lower():
                        # Extract calculation expressions if present
                        import re
                        calc_expressions = re.findall(r'[\d+\-*/().\s]+', message.content)
                        if calc_expressions:
                            calc_result = self.execute_tool("calculator", {"expression": calc_expressions[0]})
                            if calc_result.get("success"):
                                response_text += f"\n\n**Quick Calculation**: {calc_result.get('result')}\n"
                except:
                    pass
            
            # Remove any demo/placeholder content that might have been generated
            response_text = self._clean_demo_content(response_text)
            
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
        """Format search results in a readable way - filters out demo/placeholder content"""
        if isinstance(search_result, dict) and "results" in search_result:
            formatted = "\n\n### 🔍 Real-Time Market Intelligence\n\n"
            results = search_result.get("results", [])
            valid_results = []
            
            for result in results:
                url = result.get("url", "")
                title = result.get("title", "")
                snippet = result.get("snippet", "")
                
                # Filter out all demo/placeholder/test URLs and content
                if any(demo_term in url.lower() for demo_term in ['example.com', 'demo', 'test', 'placeholder', 'mock']):
                    continue
                if any(demo_term in title.lower() for demo_term in ['result for:', 'demo', 'test', 'placeholder']):
                    continue
                if any(demo_term in snippet.lower() for demo_term in ['relevant content here', 'demo', 'test', 'placeholder']):
                    continue
                
                valid_results.append(result)
            
            # Only show real, valid results (no demo links)
            for i, result in enumerate(valid_results[:3], 1):
                title = result.get("title", "").strip()
                snippet = result.get("snippet", "").strip()
                url = result.get("url", "").strip()
                
                if title and snippet:
                    formatted += f"**{i}. {title}**\n"
                    formatted += f"{snippet}\n"
                    if url and not any(demo_term in url.lower() for demo_term in ['example.com', 'demo', 'test']):
                        formatted += f"🔗 {url}\n"
                    formatted += "\n"
            
            return formatted if valid_results else ""
        elif isinstance(search_result, str):
            # Clean any demo references from string results
            cleaned = search_result.replace('[Search Results:', '').replace(']', '')
            if not any(demo_term in cleaned.lower() for demo_term in ['example.com', 'demo', 'test', 'placeholder']):
                return f"\n\n### 🔍 Additional Intelligence\n\n{cleaned}\n"
        return ""
    
    def _build_prompt(self, user_message: str, history: list, context: AgentContext) -> str:
        """Build advanced analytical prompt with real-time insights and future planning"""
        from datetime import datetime
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_season = self._get_current_season()
        
        prompt = f"""You are Dr. Agricultural Intelligence, India's premier agricultural strategist and futurist with 30+ years of cutting-edge research and field experience. You combine deep domain expertise with real-time market intelligence, climate science, and innovative farming technologies.

CORE CAPABILITIES:
- Real-time market analysis and price forecasting
- Climate-resilient farming strategies
- Precision agriculture and IoT integration
- Sustainable intensification techniques
- Future-proof farming roadmaps
- Risk mitigation and contingency planning
- Government scheme optimization
- Supply chain and market linkage strategies

CURRENT CONTEXT (Real-Time):
- Date: {current_date}
- Season: {current_season}
- Market Phase: {self._get_market_phase()}

RESPONSE REQUIREMENTS:
1. **IMMEDIATE ANALYSIS**: Start with current market conditions, real-time prices, and immediate actionable steps
2. **CORE INSIGHTS**: Provide deep analytical insights with specific data points, percentages, costs, yields, and ROI calculations
3. **OUT-OF-THE-BOX THINKING**: Suggest innovative approaches, unconventional strategies, and emerging technologies
4. **FUTURE PLANNING**: Include 6-month, 1-year, and 3-year strategic roadmaps with milestones
5. **RISK ANALYSIS**: Identify potential challenges and provide mitigation strategies
6. **COMPETITIVE ADVANTAGE**: Highlight opportunities for differentiation and premium pricing
7. **DATA-DRIVEN**: Use specific numbers, statistics, and evidence-based recommendations
8. **NO DEMO CONTENT**: Never include placeholder links, demo URLs, or example.com references - only real, actionable information

RESPONSE STRUCTURE:
- **Executive Summary**: Key insights in 2-3 sentences
- **Current Market Intelligence**: Real-time analysis
- **Strategic Recommendations**: Core actionable steps
- **Innovation Opportunities**: Out-of-the-box solutions
- **Future Roadmap**: Short, medium, and long-term plans
- **Risk & Mitigation**: Potential challenges and solutions
- **Financial Projections**: ROI, costs, revenue forecasts
- **Next Steps**: Immediate actions with timelines

"""
        
        # Add memory context if available
        if context.memory:
            prompt += "**LEARNED CONTEXT FROM PREVIOUS INTERACTIONS:**\n"
            for key, value in list(context.memory.items())[:5]:
                prompt += f"- {key}: {value}\n"
            prompt += "\n"
        
        # Add conversation history for continuity
        if history:
            prompt += "**CONVERSATION HISTORY:**\n"
            for msg in history[-5:]:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                prompt += f"{role.upper()}: {content}\n"
            prompt += "\n"
        
        prompt += f"""**USER QUERY:** {user_message}

**YOUR TASK**: Provide a comprehensive, advanced analysis that combines:
- Real-time market intelligence
- Deep analytical insights
- Innovative, out-of-the-box solutions
- Strategic future planning
- Actionable recommendations with specific data

Remember: NO demo links, NO placeholder content, NO example URLs. Only real, actionable, data-driven insights.

Begin your response:"""
        
        return prompt
    
    def _clean_demo_content(self, text: str) -> str:
        """Remove all demo, placeholder, and example content from response"""
        import re
        
        # Remove demo URLs
        text = re.sub(r'https?://(?:www\.)?(?:example\.com|demo|test|placeholder)[^\s]*', '', text, flags=re.IGNORECASE)
        
        # Remove placeholder text patterns
        placeholder_patterns = [
            r'\[.*?placeholder.*?\]',
            r'\[.*?demo.*?\]',
            r'\[.*?example.*?\]',
            r'Result \d+ for:',
            r'relevant content here',
            r'Information about.*?- relevant content',
        ]
        
        for pattern in placeholder_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Clean up multiple spaces and newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)
        
        return text.strip()
    
    def _get_current_season(self) -> str:
        """Determine current agricultural season"""
        from datetime import datetime
        month = datetime.now().month
        if month in [6, 7, 8, 9]:
            return "Kharif (Monsoon Season)"
        elif month in [10, 11, 12, 1]:
            return "Rabi (Winter Season)"
        elif month in [2, 3, 4, 5]:
            return "Zaid (Summer Season)"
        return "Transition Period"
    
    def _get_market_phase(self) -> str:
        """Determine current market phase"""
        from datetime import datetime
        month = datetime.now().month
        if month in [9, 10, 11]:
            return "Harvest & Peak Selling Season"
        elif month in [12, 1, 2]:
            return "Post-Harvest & Storage Planning"
        elif month in [3, 4, 5]:
            return "Pre-Monsoon Preparation & Input Procurement"
        elif month in [6, 7, 8]:
            return "Active Growing Season & Market Monitoring"
        return "Market Analysis Phase"
