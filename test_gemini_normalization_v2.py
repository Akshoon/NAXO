
import os
import sys
from typing import Any
from dotenv import load_dotenv
import google.generativeai as genai

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from chatbot.services.conversation import IntentionDetector

def test_normalization():
    print("Loading environment...")
    load_dotenv()
    
    # Use key from env OR fallback from api_chatbot.py
    api_key = os.getenv("GEMINI_API_KEY", "AIzaSyBnVgg33jVHSypAkDqv-6PFTtqK8-eh3dM")
    
    if api_key:
        print(f"Using API Key: {api_key[:5]}...{api_key[-5:]}")
        genai.configure(api_key=api_key)
    else:
        print("[ERROR] No API Key found.")
        return

    print("Instantiating IntentionDetector with Gemini...")
    try:
        detector = IntentionDetector(genai_client=genai)
        print("IntentionDetector instantiated.")
    except Exception as e:
        print(f"[ERROR] Failed to instantiate: {e}")
        return

    # Complex case that regex might miss or just general testing
    test_cases = [
        "ant ecedentes",
        "doc umentos",
        "inform  ación",
        "necesito antecedentes para licencia medica",
        "se solicitan ant ecedentes para licencia médica",
        "texto   con   muchos    espacios   innecesarios"
    ]
    
    for case in test_cases:
        print(f"\nOriginal: '{case}'")
        try:
            # We want to see if it uses Gemini. 
            # Note: We can't easily spy on the internal call without mocking, 
            # but if it works without error, that's a good sign.
            normalized = detector.normalize_text(case)
            print(f"Normalized: '{normalized}'")
        except Exception as e:
            print(f"[ERROR] Error normalizing: {e}")

if __name__ == "__main__":
    test_normalization()
