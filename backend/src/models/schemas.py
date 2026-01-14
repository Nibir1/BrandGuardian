"""
schemas.py
----------
Pydantic models for Request and Response objects.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, ConfigDict

# --- Generation Models (Text) ---

class BrandRequest(BaseModel):
    """
    Schema for content generation requests.
    """
    topic: str = Field(..., description="The main subject.", min_length=3)
    content_type: str = Field(..., description="The format required.")
    tone_modifier: Optional[str] = Field("Professional", description="Optional nuance.")
    
    # Modern Pydantic v2 Config
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "topic": "Launch of the new Vaisala Optimus DGA Monitor",
                "content_type": "LinkedIn Post",
                "tone_modifier": "Innovative"
            }
        }
    )

class BrandResponse(BaseModel):
    """
    Schema for the AI's response.
    """
    content: str = Field(..., description="The final generated text.")
    brand_score: int = Field(..., description="Quality score (0-100).", ge=0, le=100)
    reasoning: str = Field(..., description="Explanation of score.")
    used_references: List[str] = Field(default=[], description="Snippets used.")

# --- Vision Models (Image) ---

class ImageValidationRequest(BaseModel):
    """
    Schema for image validation requests.
    """
    image_url: HttpUrl = Field(..., description="Publicly accessible URL.")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "image_url": "https://example.com/uploads/banner.jpg"
            }
        }
    )

class ImageValidationResponse(BaseModel):
    """
    Schema for image analysis results.
    """
    is_compliant: bool = Field(..., description="True if compliant.")
    dominant_colors: List[str] = Field(..., description="Detected Hex codes.")
    violation_reason: Optional[str] = Field(None, description="Explanation.")