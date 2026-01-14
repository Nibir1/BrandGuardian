"""
app.py
------
Main FastAPI Application Entrypoint.
Exposes endpoints for Text Generation and Image Validation.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.models.schemas import (
    BrandRequest, BrandResponse, 
    ImageValidationRequest, ImageValidationResponse
)
from src.core.agent import brand_agent
from src.core.guardrails import brand_guard
from src.services.vision_service import validate_image_url

app = FastAPI(
    title="BrandGuardian API",
    description="Vaisala AI Brand Assistant Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS (Allow Frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    """Health check endpoint to verify system status."""
    return {"status": "operational", "env": settings.ENV}

@app.post(f"{settings.API_V1_STR}/generate", response_model=BrandResponse)
def generate_content(request: BrandRequest):
    """
    Generates marketing copy using RAG and scores it against brand guidelines.
    """
    try:
        # 1. Generate Content (Agent)
        agent_result = brand_agent.generate(request)
        raw_text = agent_result["content"]
        
        # 2. Evaluate Content (Guardrails)
        # We run this BEFORE sending back to user (Quality Control)
        grading = brand_guard.evaluate(raw_text)
        
        # 3. Return Combined Response
        return BrandResponse(
            content=raw_text,
            brand_score=grading["score"],
            reasoning=grading["reasoning"],
            used_references=agent_result["used_references"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(f"{settings.API_V1_STR}/validate-image", response_model=ImageValidationResponse)
def validate_image(request: ImageValidationRequest):
    """
    Analyzes an image URL for Vaisala brand color compliance.
    """
    try:
        return validate_image_url(request.image_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)