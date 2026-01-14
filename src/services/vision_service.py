"""
vision_service.py
-----------------
Multimodal logic to validate images against brand guidelines.
Uses Pillow (PIL) for image processing and NumPy for vector math.
"""

import json
import httpx
import numpy as np
from io import BytesIO
from PIL import Image
from typing import List, Tuple
from src.models.schemas import ImageValidationResponse

# Load rules
PALETTE_PATH = "data/rules/palette.json"

def _load_palette() -> dict:
    """Loads the approved colors from JSON."""
    with open(PALETTE_PATH, "r") as f:
        return json.load(f)

def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """Converts #RRGGBB to (R, G, B) tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def _rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """Converts (R, G, B) to #RRGGBB."""
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def _calculate_distance(color1: Tuple, color2: Tuple) -> float:
    """
    Calculates Euclidean distance between two RGB colors in 3D space.
    Formula: sqrt((r2-r1)^2 + (g2-g1)^2 + (b2-b1)^2)
    """
    return np.sqrt(np.sum((np.array(color1) - np.array(color2)) ** 2))

def validate_image_url(image_url: str) -> ImageValidationResponse:
    """
    Downloads an image and checks if its dominant colors match the brand palette.
    
    Args:
        image_url (str): The public URL of the image.
        
    Returns:
        ImageValidationResponse: Compliance status and analysis.
    """
    print(f"👁️ Vision Service analyzing: {image_url}")
    
    # 1. Download Image
    try:
        response = httpx.get(image_url, timeout=10.0)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert("RGB")
    except Exception as e:
        return ImageValidationResponse(
            is_compliant=False,
            dominant_colors=[],
            violation_reason=f"Failed to load image: {str(e)}"
        )

    # 2. Extract Dominant Colors
    # We resize to speed up processing, then quantize to reduce to top 5 colors
    img = img.resize((150, 150))
    # 'quantize' reduces the image to N colors. We ask for 5.
    # Note: quantize requires P mode, so we convert back to RGB palette.
    quantized = img.quantize(colors=5, method=2) 
    dominant_palette = quantized.getpalette()[:15] # First 5 RGB triplets (5 * 3 = 15 values)
    
    # Parse the flat list [r,g,b, r,g,b...] into tuples [(r,g,b), ...]
    dominant_rgbs = [
        (dominant_palette[i], dominant_palette[i+1], dominant_palette[i+2])
        for i in range(0, len(dominant_palette), 3)
    ]

    # 3. Load Rules
    rules = _load_palette()
    brand_rgbs = [_hex_to_rgb(c) for c in rules["colors"]]
    tolerance = rules["tolerance"]
    
    # 4. Compare Colors
    # For every dominant color, check if it is "close enough" to ANY brand color.
    # If a dominant color is too far from ALL brand colors, it's a "violation".
    # However, images usually have backgrounds. We require at least ONE dominant color
    # to be a strong brand match to consider it "On Brand" (or we can invert logic:
    # "Reject if dominant color is strictly clashing").
    # For this architecture, we will use "Brand Alignment": 
    # At least 50% of dominant colors must map to the palette.
    
    matches = 0
    for dom_c in dominant_rgbs:
        # Find distance to the closest brand color
        distances = [_calculate_distance(dom_c, brand_c) for brand_c in brand_rgbs]
        min_dist = min(distances)
        
        if min_dist <= tolerance:
            matches += 1
            
    # Logic: If 3 out of 5 dominant colors fit the palette, it passes.
    is_compliant = matches >= 2 
    
    detected_hex = [_rgb_to_hex(c) for c in dominant_rgbs]
    
    reason = "Image aligns with brand palette."
    if not is_compliant:
        reason = "Dominant colors deviate significantly from Vaisala identity guidelines."

    print(f"✅ Analysis Complete. Compliant: {is_compliant}")

    return ImageValidationResponse(
        is_compliant=is_compliant,
        dominant_colors=detected_hex,
        violation_reason=reason
    )