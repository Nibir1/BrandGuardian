"""
test_vision.py
--------------
Unit tests for the Visual Gatekeeper.
Mocks 'httpx' and Pillow image processing to ensure deterministic testing.
"""

import pytest
from unittest.mock import patch, MagicMock
from src.services.vision_service import validate_image_url

# Standard Vaisala Palette for testing
TEST_PALETTE = {
    "colors": ["#00A3E0", "#FFFFFF", "#000000"], 
    "tolerance": 60
}

@patch("src.services.vision_service._load_palette", return_value=TEST_PALETTE)
@patch("src.services.vision_service.httpx.get")
@patch("src.services.vision_service.Image.open")
def test_validate_image_compliant(mock_img_open, mock_get, mock_palette):
    """Test that a Vaisala Blue image passes."""
    
    # 1. Mock HTTP Response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"fake-image-bytes"
    mock_get.return_value = mock_response

    # 2. Mock Pillow Image Processing Chain
    # We need to mock: Image.open() -> .convert() -> .resize() -> .quantize() -> .getpalette()
    
    # Create the mock image object that will be returned by resize()
    mock_quantized_img = MagicMock()
    # Return a palette that is ALL BLUE (R=0, G=163, B=224)
    # 5 colors * 3 values (RGB) = 15 integers
    mock_quantized_img.getpalette.return_value = [0, 163, 224] * 5 
    
    # Chain the mocks
    mock_img = MagicMock()
    mock_img.resize.return_value.quantize.return_value = mock_quantized_img
    
    mock_img_open.return_value.convert.return_value = mock_img

    # 3. Execution
    result = validate_image_url("http://test.com/blue.png")

    # 4. Assertion
    assert result.is_compliant is True
    assert result.dominant_colors[0] == "#00a3e0"

@patch("src.services.vision_service._load_palette", return_value=TEST_PALETTE)
@patch("src.services.vision_service.httpx.get")
@patch("src.services.vision_service.Image.open")
def test_validate_image_violation(mock_img_open, mock_get, mock_palette):
    """Test that a Red image fails."""
    
    # 1. Mock HTTP Response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"fake-image-bytes"
    mock_get.return_value = mock_response

    # 2. Mock Pillow to return RED
    mock_quantized_img = MagicMock()
    # Return a palette that is ALL RED (R=255, G=0, B=0)
    mock_quantized_img.getpalette.return_value = [255, 0, 0] * 5 
    
    mock_img = MagicMock()
    mock_img.resize.return_value.quantize.return_value = mock_quantized_img
    mock_img_open.return_value.convert.return_value = mock_img

    # 3. Execution
    result = validate_image_url("http://test.com/red.png")

    # 4. Assertion
    assert result.is_compliant is False
    assert result.dominant_colors[0] == "#ff0000"

@patch("src.services.vision_service.httpx.get")
def test_image_download_failure(mock_get):
    """Test error handling when URL is broken."""
    mock_get.side_effect = Exception("404 Not Found")

    result = validate_image_url("http://broken.com/img.png")
    
    assert result.is_compliant is False
    assert "Failed to load image" in result.violation_reason