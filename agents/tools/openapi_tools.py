"""
OpenAPI Tools Support
Implements OpenAPI-compatible tools for agent integration
"""
from typing import Dict, Any, Optional, List
import json
import logging
import requests
from .builtin_tools import BaseTool


class OpenAPITool(BaseTool):
    """
    Base class for OpenAPI-compatible tools
    Implements OpenAPI specification for tool communication
    """
    
    def __init__(self, name: str, description: str, openapi_spec: Dict[str, Any] = None):
        super().__init__(name, description)
        self.openapi_spec = openapi_spec or {}
        self.openapi_enabled = True
    
    def get_openapi_spec(self) -> Dict[str, Any]:
        """Get OpenAPI specification for this tool"""
        return {
            "openapi": "3.0.0",
            "info": {
                "title": self.name,
                "description": self.description,
                "version": "1.0.0"
            },
            "paths": self.openapi_spec.get("paths", {}),
            "components": self.openapi_spec.get("components", {})
        }
    
    def execute_openapi(self, method: str, path: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute tool via OpenAPI protocol"""
        try:
            result = self.execute(**parameters or {})
            return {
                "status": 200,
                "data": result,
                "headers": {"Content-Type": "application/json"}
            }
        except Exception as e:
            return {
                "status": 500,
                "error": str(e),
                "headers": {"Content-Type": "application/json"}
            }


class OpenAPIWeatherTool(OpenAPITool):
    """OpenAPI-compatible weather tool"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            name="weather_api",
            description="Weather data API",
            openapi_spec={
                "paths": {
                    "/weather": {
                        "get": {
                            "summary": "Get weather data",
                            "parameters": [
                                {"name": "lat", "in": "query", "schema": {"type": "number"}},
                                {"name": "lon", "in": "query", "schema": {"type": "number"}},
                                {"name": "days", "in": "query", "schema": {"type": "integer", "default": 7}}
                            ],
                            "responses": {
                                "200": {
                                    "description": "Weather data",
                                    "content": {"application/json": {"schema": {"type": "object"}}}
                                }
                            }
                        }
                    }
                }
            }
        )
        self.api_key = api_key
    
    def execute(self, lat: float, lon: float, days: int = 7, **kwargs) -> Dict[str, Any]:
        """Execute weather query via OpenAPI"""
        from .agricultural_tools import WeatherDataTool
        tool = WeatherDataTool(api_key=self.api_key)
        return tool.execute(latitude=lat, longitude=lon, days=days)


class OpenAPICropTool(OpenAPITool):
    """OpenAPI-compatible crop recommendation tool"""
    
    def __init__(self, model_path: str = None):
        super().__init__(
            name="crop_recommendation_api",
            description="Crop recommendation API",
            openapi_spec={
                "paths": {
                    "/recommend": {
                        "post": {
                            "summary": "Get crop recommendation",
                            "requestBody": {
                                "required": True,
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "type": "object",
                                            "properties": {
                                                "state": {"type": "string"},
                                                "district": {"type": "string"},
                                                "latitude": {"type": "number"},
                                                "longitude": {"type": "number"},
                                                "soil_type": {"type": "string"},
                                                "ph": {"type": "number"},
                                                "temperature": {"type": "number"},
                                                "rainfall": {"type": "number"}
                                            }
                                        }
                                    }
                                }
                            },
                            "responses": {
                                "200": {
                                    "description": "Crop recommendation",
                                    "content": {"application/json": {"schema": {"type": "object"}}}
                                }
                            }
                        }
                    }
                }
            }
        )
        self.model_path = model_path
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute crop recommendation via OpenAPI"""
        from .agricultural_tools import CropRecommendationTool
        tool = CropRecommendationTool(model_path=self.model_path)
        return tool.execute(**kwargs)


class OpenAPIToolRegistry:
    """Registry for OpenAPI tools"""
    
    def __init__(self):
        self.tools: Dict[str, OpenAPITool] = {}
        self.logger = logging.getLogger("openapi_registry")
    
    def register_tool(self, tool: OpenAPITool):
        """Register an OpenAPI tool"""
        self.tools[tool.name] = tool
        self.logger.info(f"Registered OpenAPI tool: {tool.name}")
    
    def get_tool(self, name: str) -> Optional[OpenAPITool]:
        """Get tool by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all registered OpenAPI tools with specs"""
        return [tool.get_openapi_spec() for tool in self.tools.values()]
    
    def execute_tool(self, name: str, method: str, path: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute an OpenAPI tool"""
        tool = self.get_tool(name)
        if not tool:
            return {
                "status": 404,
                "error": f"Tool {name} not found",
                "headers": {"Content-Type": "application/json"}
            }
        
        try:
            return tool.execute_openapi(method, path, parameters)
        except Exception as e:
            self.logger.error(f"Error executing OpenAPI tool {name}: {e}")
            return {
                "status": 500,
                "error": str(e),
                "headers": {"Content-Type": "application/json"}
            }






