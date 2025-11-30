"""
Disease Detection Agent - Specialized agent for leaf disease detection
"""
from typing import Any
from agents.base_agent import BaseAgent, AgentMessage, AgentContext, AgentState


class DiseaseDetectionAgent(BaseAgent):
    """
    Specialized agent for detecting leaf diseases
    Can integrate with Leafine model
    """
    
    def __init__(
        self,
        agent_id: str = "disease_agent",
        model_path: str = None,
        tools: list = None
    ):
        super().__init__(
            agent_id=agent_id,
            agent_name="Disease Detection Specialist",
            tools=tools or []
        )
        self.model_path = model_path
    
    def process(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        """Process disease detection request"""
        self.state = AgentState.RUNNING
        self.update_metrics("total_requests", 1)
        
        try:
            self.log_trace("disease_detection_start", {
                "message": message.content[:100]
            })
            
            # Check if image is provided in metadata
            image_data = message.metadata.get("image")
            
            if image_data:
                # Process image for disease detection
                # In production, this would call the Leafine model
                result = self._detect_disease(image_data)
            else:
                # Provide general disease information
                result = self._get_disease_info(message.content)
            
            self.update_metrics("successful_requests", 1)
            self.state = AgentState.COMPLETED
            
            return AgentMessage(
                sender=self.agent_id,
                receiver=message.sender,
                content=result,
                metadata={"detection_result": result},
                session_id=context.session_id
            )
            
        except Exception as e:
            self.state = AgentState.ERROR
            self.update_metrics("failed_requests", 1)
            self.log_trace("disease_detection_error", {"error": str(e)})
            
            return AgentMessage(
                sender=self.agent_id,
                receiver=message.sender,
                content=f"Error in disease detection: {str(e)}",
                session_id=context.session_id
            )
    
    def _detect_disease(self, image_data: Any) -> str:
        """Detect disease from image"""
        # In production, this would use the actual Leafine model
        # For now, return mock response
        return """🍃 **Leaf Disease Detection Result**

**Detected Disease:** Leaf Blight
**Confidence:** 85%
**Severity:** Moderate

**Treatment Recommendations:**
- Apply fungicide (Copper-based)
- Remove affected leaves
- Improve air circulation
- Monitor for 7-10 days

**Prevention:**
- Avoid overhead watering
- Maintain proper spacing
- Use disease-resistant varieties
"""
    
    def _get_disease_info(self, query: str) -> str:
        """Get general disease information"""
        return """🍃 **Disease Information**

Common agricultural diseases:
- Leaf Blight: Fungal disease, treat with fungicides
- Powdery Mildew: White powdery growth, use sulfur-based treatments
- Rust: Orange/brown spots, remove affected parts
- Bacterial Blight: Water-soaked lesions, use copper sprays

For accurate detection, please upload an image of the affected leaf.
"""
