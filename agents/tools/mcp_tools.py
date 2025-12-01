"""
MCP (Model Context Protocol) Tools
Implements MCP-compatible tools for agent integration
"""
from typing import Dict, Any, Optional, List
import json
import logging
from .builtin_tools import BaseTool


class MCPTool(BaseTool):
    """
    Base class for MCP-compatible tools
    Implements MCP protocol for tool communication
    """
    
    def __init__(self, name: str, description: str, parameters: Dict[str, Any] = None):
        super().__init__(name, description)
        self.parameters = parameters or {}
        self.mcp_enabled = True
    
    def get_mcp_schema(self) -> Dict[str, Any]:
        """Get MCP schema for this tool"""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": {
                "type": "object",
                "properties": self.parameters,
                "required": []
            }
        }
    
    def execute_mcp(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tool via MCP protocol"""
        return {
            "content": [
                {
                    "type": "text",
                    "text": json.dumps(self.execute(**arguments))
                }
            ],
            "isError": False
        }


class MCPWeatherTool(MCPTool):
    """MCP-compatible weather tool"""
    
    def __init__(self):
        super().__init__(
            name="mcp_weather",
            description="Get weather data via MCP",
            parameters={
                "latitude": {"type": "number", "description": "Latitude"},
                "longitude": {"type": "number", "description": "Longitude"},
                "days": {"type": "integer", "description": "Number of forecast days", "default": 7}
            }
        )
    
    def execute(self, latitude: float, longitude: float, days: int = 7, **kwargs) -> Dict[str, Any]:
        """Execute weather query"""
        from .agricultural_tools import WeatherDataTool
        tool = WeatherDataTool()
        return tool.execute(latitude=latitude, longitude=longitude, days=days)


class MCPCropRecommendationTool(MCPTool):
    """MCP-compatible crop recommendation tool"""
    
    def __init__(self, model_path: str = None):
        super().__init__(
            name="mcp_crop_recommendation",
            description="Get crop recommendations via MCP",
            parameters={
                "state": {"type": "string", "description": "State name"},
                "district": {"type": "string", "description": "District name"},
                "latitude": {"type": "number", "description": "Latitude"},
                "longitude": {"type": "number", "description": "Longitude"},
                "soil_type": {"type": "string", "description": "Soil type"},
                "ph": {"type": "number", "description": "pH value"},
                "temperature": {"type": "number", "description": "Temperature in Celsius"},
                "rainfall": {"type": "number", "description": "Rainfall in mm"}
            }
        )
        self.model_path = model_path
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute crop recommendation"""
        from .agricultural_tools import CropRecommendationTool
        tool = CropRecommendationTool(model_path=self.model_path)
        return tool.execute(**kwargs)


class MCPToolRegistry:
    """Registry for MCP tools"""
    
    def __init__(self):
        self.tools: Dict[str, MCPTool] = {}
        self.logger = logging.getLogger("mcp_registry")
    
    def register_tool(self, tool: MCPTool):
        """Register an MCP tool"""
        self.tools[tool.name] = tool
        self.logger.info(f"Registered MCP tool: {tool.name}")
    
    def get_tool(self, name: str) -> Optional[MCPTool]:
        """Get tool by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all registered MCP tools with schemas"""
        return [tool.get_mcp_schema() for tool in self.tools.values()]
    
    def execute_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an MCP tool"""
        tool = self.get_tool(name)
        if not tool:
            return {
                "content": [{"type": "text", "text": f"Tool {name} not found"}],
                "isError": True
            }
        
        try:
            return tool.execute_mcp(arguments)
        except Exception as e:
            self.logger.error(f"Error executing MCP tool {name}: {e}")
            return {
                "content": [{"type": "text", "text": f"Error: {str(e)}"}],
                "isError": True
            }






