<img width="200" height="200" alt="Nilam logo" src="https://github.com/Brindha-m/Nilam_Kaggle/blob/main/assets/479230373-fcc4a050-49c8-4cba-8ea7-6e76e5cfbb4c.png" />
<br>

**Nilam (Native Intelligence for Land and Agriculture Management) is an integrated AI-powered agricultural  multilingual chat assistance, leaf disease detection, and personalized crop recommendation system.**

## Modules Architecture

<img width="642" height="661" alt="NILAM ARCH" src="https://github.com/Brindha-m/Nilam_Kaggle/blob/main/assets/479232011-52861f5c-95d3-41ff-b3b1-8e8b7279fbe4.png" />


### 🌱 **Nilam Chat**
- **AI-Powered Assistant**: Powered by Google's Generative AI (Gemini).
- **Specialized in farming queries, crop advice and available in multiple Indian languages adding on with market trends and price analysis**

### 🍃 **Leafine**
- **Leaf Disease Detection**: Custom trained on our leafine dataset with improved YOLOv8 architecture Resnext-50 with XAI.
- **Recognize & Perceive the leaf illness and figure out how to treat them!**
# Nilam AI Agents

## Problem Statement

**The Challenge:** Farmers in India and across the globe face critical challenges in making informed agricultural decisions. They struggle with:

1. **Fragmented Information Access**: Agricultural knowledge is scattered across multiple sources - weather services, crop databases, disease identification guides, market prices, and government schemes. Farmers need to consult multiple platforms to get comprehensive advice.

2. **Language Barriers**: Many agricultural resources are only available in English, while a significant portion of farmers speak regional languages. This creates a barrier to accessing critical information.

3. **Lack of Personalized Recommendations**: Generic agricultural advice doesn't account for specific local conditions - soil type, climate patterns, water availability, and regional market dynamics.

4. **Delayed Disease Detection**: Early detection of plant diseases is crucial for crop health, but farmers often lack access to expert diagnosis tools, leading to significant crop losses.

5. **Complex Decision-Making**: Choosing the right crop, understanding market trends, accessing government schemes, and planning agricultural activities requires synthesizing information from multiple domains simultaneously.

**Why This Matters**: Agriculture is the backbone of many economies, and small-scale farmers often lack access to the sophisticated tools and expertise available to large agricultural operations. Providing AI-powered, accessible, and comprehensive agricultural assistance can significantly improve crop yields, reduce losses, and enhance farmers' livelihoods.

**The Solution**: Nilam (Native Intelligence for Land and Agriculture Management) - an integrated AI-powered multi-agent system that provides personalized, multilingual, and context-aware agricultural assistance through a unified interface.

---

## Why Agents?

Agents are the **perfect solution** for this problem because:

### 1. **Specialized Expertise**
Each agent can be a specialist in a specific domain:
- **Crop Recommendation Agent**: Expert in analyzing soil, weather, and market conditions to recommend optimal crops
- **Disease Detection Agent**: Specialized in identifying plant diseases from images
- **Chat Agent**: Conversational expert powered by LLM for natural language interaction
- **Weather Agent**: Real-time weather data specialist

### 2. **Parallel Processing**
Multiple agents can work simultaneously on different aspects of a query:
- While one agent fetches weather data, another can analyze soil conditions
- Disease detection and crop recommendation can happen in parallel
- This dramatically reduces response time and improves user experience

### 3. **Modularity and Scalability**
- New capabilities can be added by introducing new agents without disrupting existing functionality
- Agents can be independently updated, tested, and deployed
- The system can scale horizontally by adding more agent instances

### 4. **Tool Integration**
Agents can leverage specialized tools:
- **MCP Tools**: Standardized protocol for external service integration
- **OpenAPI Tools**: RESTful API integration
- **Custom Tools**: Domain-specific tools (weather, crop analysis, market data)
- **Built-in Tools**: General-purpose tools (search, calculator)

### 5. **Context Awareness and Memory**
- Agents maintain conversation history and user preferences
- Long-term memory allows personalized recommendations based on past interactions
- Context compaction ensures efficient memory usage

### 6. **Resilience and Fault Tolerance**
- If one agent fails, others can continue processing
- Long-running operations can be paused and resumed
- System observability allows for proactive issue detection

### 7. **Agent-to-Agent Communication (A2A)**
- Agents can collaborate, share information, and build upon each other's work
- Capability-based discovery allows dynamic agent composition
- Enables complex workflows that no single agent could handle alone

**Traditional Approach Limitations:**
- Monolithic systems are hard to maintain and extend
- Single-threaded processing is slow for complex queries
- Difficult to integrate multiple data sources and services
- Limited personalization and context awareness

**Agent-Based Approach Benefits:**
- ✅ Modular, maintainable, and extensible
- ✅ Parallel processing for faster responses
- ✅ Easy integration of new tools and services
- ✅ Rich context and personalization
- ✅ Fault-tolerant and resilient

---

## What You Created

### Overall Architecture

Nilam is built as a **multi-agent orchestration system** with the following architecture:


## Architecture Overview
   ```
   Nilam AI Agents System
   ├── agents/
   │   ├── base_agent.py          # Base agent class with LLM integration
   │   ├── chat_agent.py          # LLM-powered conversational agent
   │   ├── crop_agent.py          # Crop recommendation specialist
   │   ├── disease_agent.py       # Disease detection specialist
   │   ├── long_running_agent.py  # Pause/resume operations
   │   ├── orchestrator.py        # Multi-agent orchestration
   │   ├── session_manager.py     # Session & state management
   │   ├── memory_bank.py         # Long-term memory
   │   ├── observability.py       # Logging, tracing, metrics
   │   ├── evaluation.py          # Agent evaluation
   │   ├── a2a_protocol.py        # Agent-to-agent protocol
   │   └── tools/
   │       ├── agricultural_tools.py  # Custom agricultural tools
   │       ├── builtin_tools.py       # Built-in tools (Google Search, Code Execution)
   │       ├── mcp_tools.py           # MCP protocol tools
   │       └── openapi_tools.py       # OpenAPI tools
   ├── main.py                    # Main Streamlit application
   ├── Dockerfile                 # Docker containerization
   ├── docker-compose.yml         # Docker Compose configuration
   └── requirements.txt          # Python dependencies
   
   ```

### Core Components

#### 1. **Agent Layer**
- **BaseAgent**: Abstract base class with LLM integration, tool execution, and memory management
- **ChatAgent**: LLM-powered conversational agent using Google Gemini 2.5 Flash
- **CropRecommendationAgent**: ML-based crop recommendation specialist
- **DiseaseDetectionAgent**: Disease identification and treatment specialist

#### 2. **Orchestration Layer**
- **MultiAgentOrchestrator**: Coordinates agent execution patterns
  - **Sequential**: Agents execute one after another (pipeline pattern)
  - **Parallel**: Multiple agents execute simultaneously (fan-out pattern)
  - **Loop**: Agents execute iteratively until conditions are met (refinement pattern)

#### 3. **Tool Layer**
- **MCP Tools** (`mcp_tools.py`): Model Context Protocol-compatible tools
  - MCPWeatherTool: Weather data via MCP protocol
  - MCPCropRecommendationTool: Crop recommendations via MCP
- **OpenAPI Tools** (`openapi_tools.py`): OpenAPI specification-compatible tools
  - OpenAPIWeatherTool: RESTful weather API integration
  - OpenAPICropTool: Crop data API integration
- **Custom Tools** (`agricultural_tools.py`): Domain-specific tools
  - CropRecommendationTool: ML-based crop analysis
  - WeatherDataTool: Weather data fetching
  - SoilAnalysisTool: Soil parameter analysis
  - MarketPriceTool: Market price information
  - GovernmentSchemeTool: Government scheme lookup
- **Built-in Tools** (`builtin_tools.py`): General-purpose tools
  - GoogleSearchTool: Web search functionality
  - CalculatorTool: Mathematical calculations
  - CodeExecutionTool: Safe Python code execution

#### 4. **Infrastructure Layer**
- **Session Management** (`session_manager.py`): InMemorySessionService for conversation state
- **Memory Bank** (`memory_bank.py`): Long-term persistent memory storage
- **Observability** (`observability.py`): Logging, tracing, and metrics collection
- **Evaluation** (`evaluation.py`): Agent performance and quality assessment
- **A2A Protocol** (`a2a_protocol.py`): Agent-to-agent communication and discovery

#### 5. **Application Layer**
- **Streamlit UI** (`main.py`): Unified web interface
  - Nilam Chat: Conversational agricultural assistant
  - Leafine: Leaf disease detection interface
  - Multi-Agent System: Advanced agent orchestration interface
- **Agent Integration** (`agent_integration.py`): Streamlit integration for agent system

### Technologies & Tools Used

#### **Core Framework**
- **Python 3.9+**: Primary programming language
- **Streamlit 1.28+**: Web application framework for UI
- **Google Generative AI (Gemini 2.5 Flash)**: LLM for conversational agents

#### **Tool Integration**
- **MCP (Model Context Protocol)**: Standardized tool communication
- **OpenAPI**: RESTful API integration
- **requests**: HTTP client for external APIs
- **Custom tool registry**: Flexible tool registration and execution

### Development Process

#### Phase 1: Foundation
1. Designed base agent architecture with LLM integration
2. Implemented message passing and context management
3. Created tool abstraction layer

#### Phase 2: Agent Specialization
1. Built specialized agents (Chat, Crop, Disease)
2. Integrated Google Gemini for conversational AI
3. Implemented ML models for crop recommendations

#### Phase 3: Orchestration
1. Developed MultiAgentOrchestrator
2. Implemented sequential, parallel, and loop patterns
3. Added agent registration and discovery

#### Phase 4: Tool Ecosystem
1. Implemented MCP protocol tools
2. Created OpenAPI-compatible tools
3. Built custom agricultural tools
4. Added built-in utility tools

#### Phase 5: Infrastructure
1. Session management system
2. Memory bank for long-term storage
3. Observability (logging, tracing, metrics)
4. Agent evaluation system
5. A2A protocol implementation

#### Phase 6: Integration & Deployment
1. Streamlit UI integration
2. Docker containerization
3. Docker Compose setup

<img width="1904" height="708" alt="Screenshot 2025-12-01 054431" src="https://github.com/user-attachments/assets/32a50175-a57f-40da-b9d5-c32f620d45c0" />
<img width="1503" height="700" alt="Screenshot 2025-12-01 054451" src="https://github.com/user-attachments/assets/aa49c70e-4b50-475f-bce0-54e2ac20b9cd" />
<img width="1351" height="808" alt="Screenshot" src="https://github.com/Brindha-m/Nilam_Kaggle/blob/main/assets/479259597-40e0a610-a778-4995-b66f-55fac4ec0c5c.png?raw=true" />
<img width="1351" height="808" alt="Screenshot" src="https://github.com/Brindha-m/Nilam_Kaggle/blob/main/assets/479259621-3481ef28-3e1a-4b80-87c5-01d9f2b4c3e7.png?raw=true"/>
<img width="1351" height="808" alt="Screenshot" src="https://github.com/Brindha-m/Nilam_Kaggle/blob/main/assets/479495496-a66067be-80bc-4b88-a994-5d5267d86160.png?raw=true"/>

## 🛠️ Installation

1. **Clone the repository**
   
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API Keys**
   - Create a `.streamlit/secrets.toml` file
   - Add your Gemini API key:
   ```toml
   GEMINI_API_KEY = "your-gemini-api-key-here"
   ```
   
4. **Start the main application**
   ```bash
   streamlit run main.py
   ```


## Conclusion

Nilam represents a comprehensive solution to agricultural information fragmentation, leveraging the power of multi-agent AI systems to provide farmers with accessible, personalized, and actionable agricultural assistance. The modular architecture ensures scalability and extensibility, while the rich feature set demonstrates the potential of agent-based systems in solving real-world problems.

The system successfully implements **8+ key concepts** from the AI Agents Intensive Capstone Project, far exceeding the minimum requirements, and provides a solid foundation for future enhancements that can make a significant impact on agricultural productivity and farmer livelihoods.

