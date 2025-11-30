"""
Custom Agricultural Tools for Agents
"""
from typing import Dict, Any, Optional
import pandas as pd
import numpy as np
from datetime import datetime
import logging


class BaseTool:
    """Base class for all tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = logging.getLogger(f"tool.{name}")
    
    def execute(self, **kwargs) -> Any:
        """Execute the tool - must be implemented by subclasses"""
        raise NotImplementedError


class CropRecommendationTool(BaseTool):
    """Tool for crop recommendation based on soil and weather data"""
    
    def __init__(self, model_path: str = None):
        super().__init__(
            name="crop_recommendation",
            description="Recommends suitable crops based on soil, weather, and location data"
        )
        self.model_path = model_path
        self.model = None
        # Load model if path provided
        if model_path:
            try:
                from simple_model import SimpleCropRecommendationModel
                self.model = SimpleCropRecommendationModel()
                self.model.load_model()
            except Exception as e:
                self.logger.warning(f"Could not load model: {e}")
    
    def execute(
        self,
        state: str,
        district: str,
        latitude: float,
        longitude: float,
        soil_type: str,
        ph: float,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        temperature: float,
        humidity: float,
        rainfall: float,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute crop recommendation"""
        try:
            if self.model:
                input_data = {
                    'State': state,
                    'District': district,
                    'Latitude': latitude,
                    'Longitude': longitude,
                    'Soil_Type': soil_type,
                    'pH': ph,
                    'Nitrogen': nitrogen,
                    'Phosphorus': phosphorus,
                    'Potassium': potassium,
                    'Temperature': temperature,
                    'Humidity': humidity,
                    'Rainfall': rainfall,
                    **kwargs
                }
                crop, confidence, all_predictions = self.model.predict(pd.DataFrame([input_data]))
                return {
                    "recommended_crop": crop,
                    "confidence": float(confidence),
                    "all_predictions": [(c, float(p)) for c, p in all_predictions[:5]],
                    "timestamp": datetime.now().isoformat()
                }
            else:
                # Fallback logic
                return self._fallback_recommendation(soil_type, temperature, rainfall)
        except Exception as e:
            self.logger.error(f"Error in crop recommendation: {e}")
            return {"error": str(e)}
    
    def _fallback_recommendation(self, soil_type: str, temperature: float, rainfall: float) -> Dict[str, Any]:
        """Fallback recommendation logic"""
        recommendations = {
            "Alluvial": ["Rice", "Wheat", "Sugarcane"],
            "Black": ["Cotton", "Soybean", "Wheat"],
            "Red": ["Groundnut", "Maize", "Millets"],
            "Laterite": ["Tea", "Coffee", "Cashew"]
        }
        
        suitable_crops = recommendations.get(soil_type, ["Rice", "Wheat", "Maize"])
        return {
            "recommended_crop": suitable_crops[0],
            "confidence": 0.75,
            "all_predictions": [(c, 0.25) for c in suitable_crops],
            "method": "fallback"
        }


class WeatherDataTool(BaseTool):
    """Tool for fetching weather data"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(
            name="weather_data",
            description="Fetches current and forecasted weather data for a location"
        )
        self.api_key = api_key
    
    def execute(
        self,
        latitude: float,
        longitude: float,
        days: int = 7,
        **kwargs
    ) -> Dict[str, Any]:
        """Fetch weather data"""
        try:
            # In production, this would call a real weather API
            # For now, return mock data based on location
            return {
                "location": {"lat": latitude, "lon": longitude},
                "current": {
                    "temperature": 28.5,
                    "humidity": 65,
                    "rainfall": 12.5,
                    "wind_speed": 8.2
                },
                "forecast": [
                    {
                        "date": datetime.now().isoformat(),
                        "temperature": 28.5,
                        "rainfall": 12.5
                    }
                ],
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error fetching weather: {e}")
            return {"error": str(e)}


class MarketPriceTool(BaseTool):
    """Tool for fetching market prices of crops"""
    
    def __init__(self):
        super().__init__(
            name="market_price",
            description="Fetches current market prices for agricultural commodities"
        )
        # Load price data
        self.price_data = {
            "Rice": {"price_kg": 20, "unit": "kg"},
            "Wheat": {"price_kg": 22, "unit": "kg"},
            "Cotton": {"price_kg": 65, "unit": "kg"},
            "Sugarcane": {"price_kg": 3.5, "unit": "kg"},
            "Maize": {"price_kg": 18, "unit": "kg"},
            "Groundnut": {"price_kg": 45, "unit": "kg"},
        }
    
    def execute(
        self,
        crop_name: str,
        region: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Fetch market price for a crop"""
        try:
            crop_lower = crop_name.lower()
            for crop, data in self.price_data.items():
                if crop.lower() == crop_lower:
                    return {
                        "crop": crop,
                        "price_per_kg": data["price_kg"],
                        "unit": data["unit"],
                        "region": region or "National Average",
                        "timestamp": datetime.now().isoformat()
                    }
            return {"error": f"Price data not available for {crop_name}"}
        except Exception as e:
            self.logger.error(f"Error fetching price: {e}")
            return {"error": str(e)}


class GovernmentSchemeTool(BaseTool):
    """Tool for fetching government schemes information"""
    
    def __init__(self):
        super().__init__(
            name="government_schemes",
            description="Provides information about government agricultural schemes and subsidies"
        )
        self.schemes = {
            "PM-KISAN": {
                "benefit": 6000,
                "eligibility": "Small & Marginal Farmers",
                "application": "pm-kisan.gov.in"
            },
            "PMFBY": {
                "benefit": "Crop Insurance",
                "eligibility": "All Farmers",
                "application": "pmfby.gov.in"
            },
            "KCC": {
                "benefit": "Credit up to ₹3 Lakh",
                "eligibility": "Landowner Farmers",
                "application": "Banks/CSCs"
            }
        }
    
    def execute(
        self,
        scheme_name: Optional[str] = None,
        query: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Fetch government scheme information"""
        try:
            if scheme_name:
                scheme = self.schemes.get(scheme_name)
                if scheme:
                    return {
                        "scheme": scheme_name,
                        **scheme,
                        "timestamp": datetime.now().isoformat()
                    }
                return {"error": f"Scheme '{scheme_name}' not found"}
            
            # Return all schemes if no specific scheme requested
            return {
                "schemes": self.schemes,
                "count": len(self.schemes),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error fetching schemes: {e}")
            return {"error": str(e)}


class SoilAnalysisTool(BaseTool):
    """Tool for analyzing soil parameters"""
    
    def __init__(self):
        super().__init__(
            name="soil_analysis",
            description="Analyzes soil parameters and provides recommendations"
        )
    
    def execute(
        self,
        ph: float,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        organic_carbon: float,
        **kwargs
    ) -> Dict[str, Any]:
        """Analyze soil parameters"""
        try:
            analysis = {
                "ph_status": "neutral" if 6.5 <= ph <= 7.5 else ("acidic" if ph < 6.5 else "alkaline"),
                "nitrogen_status": "high" if nitrogen > 300 else ("medium" if nitrogen > 150 else "low"),
                "phosphorus_status": "high" if phosphorus > 25 else ("medium" if phosphorus > 10 else "low"),
                "potassium_status": "high" if potassium > 250 else ("medium" if potassium > 100 else "low"),
                "organic_carbon_status": "good" if organic_carbon > 0.5 else "low",
                "recommendations": []
            }
            
            # Generate recommendations
            if ph < 6.5:
                analysis["recommendations"].append("Add lime to increase pH")
            elif ph > 7.5:
                analysis["recommendations"].append("Add sulfur to decrease pH")
            
            if nitrogen < 150:
                analysis["recommendations"].append("Apply nitrogen-rich fertilizers")
            
            if phosphorus < 10:
                analysis["recommendations"].append("Apply phosphorus fertilizers")
            
            if potassium < 100:
                analysis["recommendations"].append("Apply potash fertilizers")
            
            if organic_carbon < 0.5:
                analysis["recommendations"].append("Add organic matter/compost")
            
            analysis["timestamp"] = datetime.now().isoformat()
            return analysis
        except Exception as e:
            self.logger.error(f"Error in soil analysis: {e}")
            return {"error": str(e)}
