"""
Script de depuración para probar la normalización
"""

import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from chatbot.services.conversation import IntentionDetector

def debug_normalization():
    print("="*60)
    print("DEPURACION DE NORMALIZACION")
    print("="*60)
    
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY", "AIzaSyBnVgg33jVHSypAkDqv-6PFTtqK8-eh3dM")
    
    if api_key:
        print("OK - API Key configurada")
        genai.configure(api_key=api_key)
    else:
        print("ERROR - No API Key")
        return
    
    # Crear detector con Gemini
    detector = IntentionDetector(genai_client=genai)
    
    # Caso problemático
    test_text = "solicitan antecedentes para licencia medica"
    
    print(f"\nTexto original: '{test_text}'")
    
    # Probar normalización
    normalized = detector.normalize_text(test_text)
    print(f"Texto normalizado: '{normalized}'")
    
    # Verificar si cambió
    if normalized != test_text:
        print(f"ADVERTENCIA - El texto cambio (no deberia cambiar si ya esta correcto)")
        print(f"   Original:    '{test_text}'")
        print(f"   Normalizado: '{normalized}'")
        
        # Mostrar diferencias carácter por carácter
        print(f"\n   Longitud original: {len(test_text)}")
        print(f"   Longitud normalizado: {len(normalized)}")
    else:
        print(f"OK - El texto no cambio (correcto)")
    
    # Probar varios casos
    print("\n" + "="*60)
    print("CASOS DE PRUEBA")
    print("="*60)
    
    cases = [
        "ant ecedentes",  # Debería corregirse
        "antecedentes",   # NO debería cambiar
        "solicitan antecedentes para licencia medica",  # NO debería cambiar
        "se solicitan ant ecedentes para licencia medica",  # Debería corregirse
    ]
    
    for i, case in enumerate(cases, 1):
        result = detector.normalize_text(case)
        changed = "[CAMBIO]" if case != result else "[SIN CAMBIOS]"
        print(f"\n{i}. {changed}")
        print(f"  Original:    '{case}'")
        print(f"  Normalizado: '{result}'")

if __name__ == "__main__":
    debug_normalization()
