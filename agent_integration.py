"""
Agent System Integration for Main Application
Integrates multi-agent system with Streamlit UI
"""
import streamlit as st
import os
import sys
from typing import Optional
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def get_gemini_api_key():
    """
    Get Gemini API key from multiple sources:
    1. Streamlit secrets (current project)
    2. External secrets file (Nilam_Kaggle/.streamlit/secrets.toml)
    3. Environment variable
    """
    # Try Streamlit secrets first
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if api_key:
            return api_key
    except:
        pass
    
    # Try external secrets file (Nilam_Kaggle)
    try:
        current_dir = Path(__file__).parent.absolute()
        # Try different possible paths
        possible_paths = [
            current_dir.parent / "Nilam_Kaggle" / ".streamlit" / "secrets.toml",
            Path.home() / "Nilam_Kaggle" / ".streamlit" / "secrets.toml",
            Path("..") / "Nilam_Kaggle" / ".streamlit" / "secrets.toml",
            Path("../Nilam_Kaggle/.streamlit/secrets.toml"),
        ]
        
        for secrets_path in possible_paths:
            if secrets_path.exists():
                try:
                    # Try tomllib (Python 3.11+)
                    import tomllib
                    with open(secrets_path, 'rb') as f:
                        secrets = tomllib.load(f)
                        api_key = secrets.get("GEMINI_API_KEY")
                        if api_key:
                            return api_key
                except ImportError:
                    # Fallback to toml library or manual parsing
                    try:
                        import toml
                        with open(secrets_path, 'r') as f:
                            secrets = toml.load(f)
                            api_key = secrets.get("GEMINI_API_KEY")
                            if api_key:
                                return api_key
                    except ImportError:
                        # Manual parsing as last resort
                        with open(secrets_path, 'r') as f:
                            for line in f:
                                if line.strip().startswith('GEMINI_API_KEY'):
                                    # Extract value from line like: GEMINI_API_KEY = "value"
                                    parts = line.split('=', 1)
                                    if len(parts) == 2:
                                        value = parts[1].strip().strip('"').strip("'")
                                        if value:
                                            return value
    except Exception as e:
        print(f"Could not read external secrets file: {e}")
    
    # Try environment variable
    # api_key = os.getenv("GEMINI_API_KEY")
    api_key = "AIzaSyCOqGuHJgfv_Gd2uHti0KKSsDFjkvV3Z84"
    if api_key:
        return api_key
    
    return ""

from agents import (
    ChatAgent,
    CropRecommendationAgent,
    DiseaseDetectionAgent,
    LongRunningAgent,
    MultiAgentOrchestrator,
    AgentPattern,
    InMemorySessionService,
    MemoryBank,
    ObservabilitySystem,
    AgentEvaluator,
    A2AProtocol,
    AgentMessage,
    AgentContext
)
from agents.tools.mcp_tools import MCPToolRegistry, MCPWeatherTool, MCPCropRecommendationTool
from agents.tools.openapi_tools import OpenAPIToolRegistry, OpenAPIWeatherTool, OpenAPICropTool


@st.cache_resource
def initialize_agent_system():
    """Initialize the multi-agent system (cached for performance)"""
    # Initialize core components
    memory_bank = MemoryBank(storage_path="data/memory_bank.json")
    session_service = InMemorySessionService(memory_bank=memory_bank)
    observability = ObservabilitySystem(log_level="INFO")
    evaluator = AgentEvaluator()
    a2a_protocol = A2AProtocol()
    
    # Initialize orchestrator
    orchestrator = MultiAgentOrchestrator(session_service)
    
    # Get API key from multiple sources (including external Nilam_Kaggle secrets)
    gemini_api_key = get_gemini_api_key()
    
    # Create agents
    chat_agent = ChatAgent(
        agent_id="chat_agent",
        api_key=gemini_api_key
    )
    crop_agent = CropRecommendationAgent(agent_id="crop_agent")
    disease_agent = DiseaseDetectionAgent(agent_id="disease_agent")
    long_running_agent = LongRunningAgent(
        agent_id="long_running_agent",
        session_service=session_service
    )
    
    # Register agents with orchestrator
    orchestrator.register_agents([
        chat_agent,
        crop_agent,
        disease_agent,
        long_running_agent
    ])
    
    # Register agents with A2A protocol
    a2a_protocol.register_agent("chat_agent", ["conversation", "query_answering"])
    a2a_protocol.register_agent("crop_agent", ["crop_recommendation", "weather_analysis"])
    a2a_protocol.register_agent("disease_agent", ["disease_detection", "image_processing"])
    a2a_protocol.register_agent("long_running_agent", ["long_running_operations"])
    
    # Initialize tool registries
    mcp_registry = MCPToolRegistry()
    mcp_registry.register_tool(MCPWeatherTool())
    mcp_registry.register_tool(MCPCropRecommendationTool())
    
    openapi_registry = OpenAPIToolRegistry()
    openapi_registry.register_tool(OpenAPIWeatherTool())
    openapi_registry.register_tool(OpenAPICropTool())
    
    return {
        "orchestrator": orchestrator,
        "session_service": session_service,
        "memory_bank": memory_bank,
        "observability": observability,
        "evaluator": evaluator,
        "a2a_protocol": a2a_protocol,
        "mcp_registry": mcp_registry,
        "openapi_registry": openapi_registry,
        "agents": {
            "chat": chat_agent,
            "crop": crop_agent,
            "disease": disease_agent,
            "long_running": long_running_agent
        }
    }


def _format_agent_response(response: str) -> str:
    """Format agent response for better display"""
    import re
    
    # Remove raw search result dictionaries
    response = re.sub(r'\[Search Results:.*?\]', '', response, flags=re.DOTALL)
    
    # Clean up multiple newlines
    response = re.sub(r'\n{3,}', '\n\n', response)
    
    # Format crop recommendations better
    if '🌾' in response or 'Crop Recommendation' in response:
        # Ensure proper markdown formatting
        response = re.sub(r'\*\*Recommended Crop:\*\*', '**Recommended Crop:**', response)
        response = re.sub(r'\*\*Confidence:\*\*', '**Confidence:**', response)
    
    # Clean up any remaining JSON-like structures
    response = re.sub(r'\{[^}]*query[^}]*\}', '', response)
    
    return response.strip()


def get_or_create_session(session_service: InMemorySessionService, user_id: Optional[str] = None) -> str:
    """Get or create a session for the user"""
    if "agent_session_id" not in st.session_state:
        session_id = session_service.create_session(user_id=user_id)
        st.session_state.agent_session_id = session_id
    return st.session_state.agent_session_id


def process_with_agents(
    user_input: str,
    agent_system: dict,
    pattern: AgentPattern = AgentPattern.SEQUENTIAL
) -> str:
    """Process user input through the multi-agent system"""
    session_id = get_or_create_session(agent_system["session_service"])
    context = agent_system["session_service"].get_context(session_id)
    
    if not context:
        return "Error: Could not create session context"
    
    # Create user message
    user_message = AgentMessage(
        sender="user",
        receiver="orchestrator",
        content=user_input,
        session_id=session_id
    )
    
    # Add message to session
    agent_system["session_service"].add_message(
        session_id,
        "user",
        user_input
    )
    
    # Track observability
    start_time = __import__('time').time()
    agent_system["observability"].trace("orchestrator", "request_start", metadata={"input": user_input[:100]})
    
    try:
        # Route message through orchestrator
        results = agent_system["orchestrator"].route_message(
            user_message,
            context,
            pattern=pattern
        )
        
        # Extract final response
        if isinstance(results, list):
            final_response = results[-1].content if results else "No response generated"
        elif isinstance(results, dict):
            # Parallel execution - combine results
            final_response = "\n\n".join([
                f"**{agent_id}**: {msg.content[:200]}"
                for agent_id, msg in results.items()
            ])
        else:
            final_response = str(results)
        
        # Clean and format response
        final_response = _format_agent_response(final_response)
        
        # Calculate response time
        response_time = (__import__('time').time() - start_time) * 1000
        
        # Track observability
        agent_system["observability"].trace(
            "orchestrator",
            "request_complete",
            duration_ms=response_time,
            metadata={"response_length": len(final_response)}
        )
        agent_system["observability"].record_metric(
            "response_time_ms",
            response_time,
            tags={"pattern": pattern.value}
        )
        
        # Add response to session
        agent_system["session_service"].add_message(
            session_id,
            "assistant",
            final_response
        )
        
        # Evaluate agent performance
        agent_system["evaluator"].evaluate_agent(
            agent_id="orchestrator",
            user_query=user_input,
            agent_response=final_response,
            response_time_ms=response_time,
            success=True
        )
        
        return final_response
        
    except Exception as e:
        # Track error
        response_time = (__import__('time').time() - start_time) * 1000
        agent_system["observability"].log(
            "ERROR",
            f"Agent processing error: {str(e)}",
            agent_id="orchestrator",
            metadata={"error": str(e)}
        )
        agent_system["evaluator"].evaluate_performance(
            agent_id="orchestrator",
            response_time_ms=response_time,
            success=False,
            error_count=1
        )
        return f"I encountered an error: {str(e)}"


def display_agent_status(agent_system: dict):
    """Display agent system status in sidebar"""
    with st.sidebar.expander("🤖 Agent System Status"):
        # Agent status
        agent_status = agent_system["orchestrator"].get_agent_status()
        st.write("**Registered Agents:**")
        for agent_id, status in agent_status.items():
            st.write(f"- {agent_id}: {status['state']}")
        
        # Session stats
        session_stats = agent_system["session_service"].get_session_stats()
        st.write(f"\n**Sessions:** {session_stats['total_sessions']} total, {session_stats['active_sessions']} active")
        
        # Memory stats
        memory_stats = agent_system["memory_bank"].get_stats()
        st.write(f"**Memory:** {memory_stats['total_entries']} entries across {memory_stats['total_sessions']} sessions")
        
        # Observability summary
        dashboard = agent_system["observability"].get_dashboard_data()
        st.write(f"**Observability:** {dashboard['traces_count']} traces, {dashboard['metrics_count']} metrics")


def display_observability_dashboard(agent_system: dict):
    """Display observability dashboard"""
    st.header("📊 Observability Dashboard")
    
    dashboard = agent_system["observability"].get_dashboard_data()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Traces", dashboard["traces_count"])
    with col2:
        st.metric("Metrics", dashboard["metrics_count"])
    with col3:
        st.metric("Logs", dashboard["logs_count"])
    
    # Aggregated metrics
    st.subheader("Aggregated Metrics")
    aggregated = dashboard["aggregated_metrics"]
    if aggregated:
        for metric_name, stats in aggregated.items():
            st.write(f"**{metric_name}**:")
            st.write(f"- Count: {stats['count']}")
            st.write(f"- Average: {stats['avg']:.2f}")
            st.write(f"- Min: {stats['min']:.2f}, Max: {stats['max']:.2f}")
    
    # Recent traces
    st.subheader("Recent Traces")
    recent_traces = dashboard["recent_traces"]
    for trace in recent_traces[-10:]:
        st.write(f"- **{trace['agent_id']}**: {trace['event_type']} ({trace.get('duration_ms', 'N/A')}ms)")


def display_a2a_network(agent_system: dict):
    """Display A2A protocol network topology"""
    st.header("🌐 A2A Protocol Network")
    
    topology = agent_system["a2a_protocol"].get_network_topology()
    
    st.write(f"**Total Agents:** {topology['total_agents']}")
    st.write(f"**Active Agents:** {topology['active_agents']}")
    st.write(f"**Total Messages:** {topology['total_messages']}")
    
    st.subheader("Agent Capabilities")
    for agent_id, info in topology["agents"].items():
        st.write(f"**{agent_id}**:")
        st.write(f"- Status: {info['status']}")
        st.write(f"- Capabilities: {', '.join(info['capabilities'])}")



