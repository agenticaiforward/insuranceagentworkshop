from provider import Provider
import os

def test_provider():
    print("Testing Provider class...")
    try:
        provider = Provider()
        provider.configure()
        model = provider.get_model()
        print(f"✅ Model obtained: {model}")
        
        # Try to generate content
        response = model.generate_content("Hello")
        print(f"✅ Response: {response.text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_provider()
