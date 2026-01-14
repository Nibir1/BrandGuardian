"""
test_agent.py
-------------
A quick script to verify Phase 3 logic.
"""
from src.models.schemas import BrandRequest
from src.core.agent import brand_agent

def test_generation():
    # 1. Create a dummy request
    req = BrandRequest(
        topic="A new sensor for measuring humidity on Mars",
        content_type="LinkedIn Post",
        tone_modifier="Excited but Scientific"
    )
    
    print("\n📝 Requesting generation...")
    print(f"   Topic: {req.topic}")
    
    # 2. Run Agent
    result = brand_agent.generate(req)
    
    # 3. Print Results
    print("\n" + "="*50)
    print("🤖 GENERATED CONTENT:")
    print("="*50)
    print(result["content"])
    
    print("\n" + "="*50)
    print("📚 REFERENCES USED:")
    print("="*50)
    for ref in result["used_references"]:
        print(f" - {ref}")

if __name__ == "__main__":
    test_generation()