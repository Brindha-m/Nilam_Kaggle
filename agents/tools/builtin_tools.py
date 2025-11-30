"""
Built-in Tools: Google Search, Code Execution, etc.
"""
from typing import Dict, Any, Optional
import logging
import subprocess
import json
import re


class BaseTool:
    """Base class for all tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"tool.{name}")
    
    def execute(self, **kwargs) -> Any:
        """Execute the tool - must be implemented by subclasses"""
        raise NotImplementedError


class GoogleSearchTool(BaseTool):
    """Tool for searching Google (mock implementation)"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            name="google_search",
            description="Searches Google for information"
        )
        self.api_key = api_key
    
    def execute(
        self,
        query: str,
        num_results: int = 5,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute Google search"""
        try:
            # In production, this would use Google Search API
            # For now, return mock results
            results = [
                {
                    "title": f"Result {i+1} for: {query}",
                    "snippet": f"Information about {query} - relevant content here",
                    "url": f"https://example.com/result{i+1}"
                }
                for i in range(num_results)
            ]
            
            return {
                "query": query,
                "results": results,
                "count": len(results)
            }
        except Exception as e:
            self.logger.error(f"Error in Google search: {e}")
            return {"error": str(e)}


class CodeExecutionTool(BaseTool):
    """Tool for executing Python code safely"""
    
    def __init__(self):
        super().__init__(
            name="code_execution",
            description="Executes Python code safely in a sandboxed environment"
        )
        # Restricted imports and functions
        self.allowed_modules = ['math', 'numpy', 'pandas', 'datetime']
        self.blocked_keywords = ['import os', 'import sys', 'subprocess', 'eval', 'exec']
    
    def execute(
        self,
        code: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute Python code safely"""
        try:
            # Security check
            for blocked in self.blocked_keywords:
                if blocked in code.lower():
                    return {"error": f"Blocked keyword detected: {blocked}"}
            
            # Simple execution (in production, use proper sandboxing)
            # This is a simplified version - use restricted execution in production
            result = eval(code) if code.strip() else None
            
            return {
                "code": code,
                "result": str(result),
                "success": True
            }
        except Exception as e:
            self.logger.error(f"Error executing code: {e}")
            return {
                "code": code,
                "error": str(e),
                "success": False
            }


class CalculatorTool(BaseTool):
    """Tool for mathematical calculations"""
    
    def __init__(self):
        super().__init__(
            name="calculator",
            description="Performs mathematical calculations"
        )
    
    def execute(
        self,
        expression: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute mathematical calculation"""
        try:
            # Safe evaluation of mathematical expressions
            # Remove any non-math characters
            safe_expr = re.sub(r'[^0-9+\-*/().\s]', '', expression)
            result = eval(safe_expr)
            
            return {
                "expression": expression,
                "result": result,
                "success": True
            }
        except Exception as e:
            self.logger.error(f"Error in calculation: {e}")
            return {
                "expression": expression,
                "error": str(e),
                "success": False
            }
