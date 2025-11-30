"""
Crop Recommendation Agent - Specialized agent for crop recommendations
"""
from agents.base_agent import BaseAgent, AgentMessage, AgentContext, AgentState
from agents.tools.agricultural_tools import CropRecommendationTool, WeatherDataTool, SoilAnalysisTool, MarketPriceTool


class CropRecommendationAgent(BaseAgent):
    """
    Specialized agent for crop recommendations
    Uses ML model and agricultural tools
    """
    
    def __init__(
        self,
        agent_id: str = "crop_agent",
        model_path: str = None,
        tools: list = None
    ):
        # Initialize tools
        if tools is None:
            tools = [
                CropRecommendationTool(model_path=model_path),
                WeatherDataTool(),
                SoilAnalysisTool(),
                MarketPriceTool()
            ]
        
        super().__init__(
            agent_id=agent_id,
            agent_name="Crop Recommendation Specialist",
            tools=tools
        )
    
    def process(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        """Process crop recommendation request"""
        self.state = AgentState.RUNNING
        self.update_metrics("total_requests", 1)
        
        try:
            self.log_trace("crop_recommendation_start", {
                "message": message.content[:100]
            })
            
            # Extract parameters from message or context
            params = self._extract_parameters(message, context)
            
            # Get weather data
            weather_data = self.execute_tool(
                "weather_data",
                {
                    "latitude": params.get("latitude", 17.69),
                    "longitude": params.get("longitude", 83.3),
                    "days": 7
                }
            )
            
            # Analyze soil
            soil_analysis = self.execute_tool(
                "soil_analysis",
                {
                    "ph": params.get("ph", 7.0),
                    "nitrogen": params.get("nitrogen", 200),
                    "phosphorus": params.get("phosphorus", 15),
                    "potassium": params.get("potassium", 200),
                    "organic_carbon": params.get("organic_carbon", 0.5)
                }
            )
            
            # Get crop recommendation
            crop_recommendation = self.execute_tool(
                "crop_recommendation",
                {
                    "state": params.get("state", "Andhra Pradesh"),
                    "district": params.get("district", "Visakhapatnam"),
                    "latitude": params.get("latitude", 17.69),
                    "longitude": params.get("longitude", 83.3),
                    "soil_type": params.get("soil_type", "Alluvial"),
                    "ph": params.get("ph", 7.0),
                    "nitrogen": params.get("nitrogen", 200),
                    "phosphorus": params.get("phosphorus", 15),
                    "potassium": params.get("potassium", 200),
                    "temperature": weather_data.get("current", {}).get("temperature", 28),
                    "humidity": weather_data.get("current", {}).get("humidity", 60),
                    "rainfall": weather_data.get("current", {}).get("rainfall", 10)
                }
            )
            
            # Get market prices for recommended crops
            recommended_crop = crop_recommendation.get("recommended_crop", "Rice")
            market_price = self.execute_tool(
                "market_price",
                {"crop_name": recommended_crop}
            )
            
            # Build comprehensive response
            response = self._format_response(
                crop_recommendation,
                soil_analysis,
                weather_data,
                market_price
            )
            
            self.update_metrics("successful_requests", 1)
            self.state = AgentState.COMPLETED
            
            return AgentMessage(
                sender=self.agent_id,
                receiver=message.sender,
                content=response,
                metadata={
                    "recommendation": crop_recommendation,
                    "soil_analysis": soil_analysis,
                    "weather": weather_data,
                    "market_price": market_price
                },
                session_id=context.session_id
            )
            
        except Exception as e:
            self.state = AgentState.ERROR
            self.update_metrics("failed_requests", 1)
            self.log_trace("crop_recommendation_error", {"error": str(e)})
            
            return AgentMessage(
                sender=self.agent_id,
                receiver=message.sender,
                content=f"Error generating crop recommendation: {str(e)}",
                session_id=context.session_id
            )
    
    def _extract_parameters(self, message: AgentMessage, context: AgentContext) -> dict:
        """Extract parameters from message or context state"""
        # Try to get from context state first
        params = context.state.get("crop_params", {})
        
        # Can also parse from message content if needed
        # For now, return context params or defaults
        return params
    
    def _format_response(
        self,
        recommendation: dict,
        soil_analysis: dict,
        weather: dict,
        market_price: dict
    ) -> str:
        """Format comprehensive response"""
        crop = recommendation.get("recommended_crop", "Rice")
        confidence = recommendation.get("confidence", 0.0)
        
        response = f"""🌾 **Crop Recommendation**

**Recommended Crop:** {crop}
**Confidence:** {confidence:.1%}

**Soil Analysis:**
- pH Status: {soil_analysis.get('ph_status', 'N/A')}
- Nitrogen: {soil_analysis.get('nitrogen_status', 'N/A')}
- Phosphorus: {soil_analysis.get('phosphorus_status', 'N/A')}
- Potassium: {soil_analysis.get('potassium_status', 'N/A')}

**Recommendations:**
"""
        for rec in soil_analysis.get("recommendations", []):
            response += f"- {rec}\n"
        
        response += f"""
**Weather Conditions:**
- Temperature: {weather.get('current', {}).get('temperature', 'N/A')}°C
- Humidity: {weather.get('current', {}).get('humidity', 'N/A')}%
- Rainfall: {weather.get('current', {}).get('rainfall', 'N/A')}mm

**Market Price:**
- {market_price.get('crop', 'N/A')}: ₹{market_price.get('price_per_kg', 'N/A')}/kg
"""
        
        return response
