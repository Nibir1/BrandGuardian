"""
test_vision.py
--------------
Verifies Phase 4 Vision Logic.
"""
from src.services.vision_service import validate_image_url

def test_vision():
    # 1. Test Good Image (Blue/Tech abstract)
    good_url = "https://placehold.co/600x400/00A3E0/FFFFFF.png" # Mock Vaisala Blue
    print(f"\n🧪 Testing Compliant Image: {good_url}")
    res1 = validate_image_url(good_url)
    print(f"   Result: {res1.is_compliant}")
    print(f"   Colors Found: {res1.dominant_colors}")
    
    # 2. Test Bad Image (Bright Red)
    bad_url = "https://placehold.co/600x400/FF0000/000000.png" # Bright Red
    print(f"\n🧪 Testing Non-Compliant Image: {bad_url}")
    res2 = validate_image_url(bad_url)
    print(f"   Result: {res2.is_compliant}")
    print(f"   Colors Found: {res2.dominant_colors}")

if __name__ == "__main__":
    test_vision()