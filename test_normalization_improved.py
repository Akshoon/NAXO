"""
Script de prueba mejorado para verificar la normalización
"""

import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__))))

from chatbot.services.conversation import IntentionDetector

def test_normalization_improved():
    print("="*70)
    print("PRUEBA DE NORMALIZACION MEJORADA")
    print("="*70)
    
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY", "AIzaSyBnVgg33jVHSypAkDqv-6PFTtqK8-eh3dM")
    
    if api_key:
        print("OK - API Key configurada\n")
        genai.configure(api_key=api_key)
    else:
        print("ERROR - No API Key\n")
        return
    
    # Crear detector con Gemini
    detector = IntentionDetector(genai_client=genai)
    
    # Casos de prueba mejorados
    test_cases = [
        {
            "input": "ant ecedentes",
            "expected_behavior": "DEBE CORREGIR",
            "reason": "Palabra partida"
        },
        {
            "input": "doc umentos",
            "expected_behavior": "DEBE CORREGIR",
            "reason": "Palabra partida"
        },
        {
            "input": "texto   con   muchos    espacios",
            "expected_behavior": "DEBE CORREGIR",
            "reason": "Espacios múltiples"
        },
        {
            "input": "se solicitan ant ecedentes para licencia medica",
            "expected_behavior": "DEBE CORREGIR",
            "reason": "Tiene 'ant ecedentes' partido"
        },
        {
            "input": "antecedentes",
            "expected_behavior": "NO DEBE CAMBIAR",
            "reason": "Ya está correcto"
        },
        {
            "input": "solicitan antecedentes para licencia medica",
            "expected_behavior": "NO DEBE CAMBIAR",
            "reason": "Ya está correcto, sin palabras partidas"
        },
        {
            "input": "necesito documentos sobre derechos humanos",
            "expected_behavior": "NO DEBE CAMBIAR",
            "reason": "Ya está correcto"
        },
    ]
    
    print("CASOS DE PRUEBA:")
    print("-"*70)
    
    passed = 0
    failed = 0
    
    for i, case in enumerate(test_cases, 1):
        original = case["input"]
        expected = case["expected_behavior"]
        reason = case["reason"]
        
        normalized = detector.normalize_text(original)
        changed = (normalized != original)
        
        # Evaluar si pasó el test
        if expected == "DEBE CORREGIR":
            test_passed = changed
        else:  # "NO DEBE CAMBIAR"
            test_passed = not changed
        
        status = "[PASS]" if test_passed else "[FAIL]"
        if test_passed:
            passed += 1
        else:
            failed += 1
        
        print(f"\n{i}. {status} - {expected} ({reason})")
        print(f"   Original:    '{original}'")
        print(f"   Normalizado: '{normalized}'")
        if changed:
            print(f"   >>> Texto CAMBIO")
        else:
            print(f"   >>> Texto NO CAMBIO")
    
    print("\n" + "="*70)
    print(f"RESULTADOS: {passed} PASS, {failed} FAIL de {len(test_cases)} tests")
    print("="*70)
    
    if failed == 0:
        print("\nTODOS LOS TESTS PASARON")
    else:
        print(f"\nALERTA: {failed} test(s) fallaron")

if __name__ == "__main__":
    test_normalization_improved()
