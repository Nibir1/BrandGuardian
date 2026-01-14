"""
schemas.py
----------
Pydantic models for Request and Response objects.
Defines the contract between the API and the Client.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl

# --- Generation Models (Text) ---

class BrandRequest(BaseModel):
    """
    Schema for content generation requests.
    """
    topic: str = Field(..., description="The main subject of the content to be generated.", min_length=3)
    content_type: str = Field(..., description="The format required (e.g., 'Email', 'LinkedIn Post', 'Press Release').")
    tone_modifier: Optional[str] = Field("Professional", description="Optional nuance override (e.g., 'Urgent', 'Celebratory').")
    
    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Launch of the new Vaisala Optimus DGA Monitor",
                "content_type": "LinkedIn Post",
                "tone_modifier": "Innovative"
            }
        }

class BrandResponse(BaseModel):
    """
    Schema for the AI's response.
    Includes the content and the governance metadata.
    """
    content: str = Field(..., description="The final generated text.")
    brand_score: int = Field(..., description="Quality score (0-100) based on Vaisala guidelines.", ge=0, le=100)
    reasoning: str = Field(..., description="Explanation of why the content met or failed the guidelines.")
    used_references: List[str] = Field(default=[], description="Snippets of internal documents used for style transfer.")

# --- Vision Models (Image) ---

class ImageValidationRequest(BaseModel):
    """
    Schema for image validation requests.
    """
    image_url: HttpUrl = Field(..., description="Publicly accessible URL of the image to analyze.")
    
    class Config:
        json_schema_extra = {
            "example": {
                "image_url": "https://example.com/uploads/banner.jpg"
            }
        }

class ImageValidationResponse(BaseModel):
    """
    Schema for image analysis results.
    """
    is_compliant: bool = Field(..., description="True if the image matches Vaisala's visual identity.")
    dominant_colors: List[str] = Field(..., description="List of Hex codes detected in the image.")
    violation_reason: Optional[str] = Field(None, description="Explanation if compliance failed.")