"""
Script para probar el endpoint de normalización de texto
Basado en test_gemini_normalization_v2.py

Requiere que el servidor API esté corriendo en http://localhost:5000
"""

import requests
import json

# URL del endpoint
API_URL = "http://localhost:5000/api/normalize"

# Casos de prueba (del archivo test_gemini_normalization_v2.py)
test_cases = [
    "ant ecedentes",
    "doc umentos",
    "inform  ación",
    "necesito antecedentes para licencia medica",
    "se solicitan ant ecedentes para licencia médica",
    "texto   con   muchos    espacios   innecesarios"
]

def test_normalize_endpoint():
    """Prueba el endpoint /api/normalize con varios casos"""
    print("="*60)
    print("🧪 PROBANDO ENDPOINT /api/normalize")
    print("="*60)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{i}. Caso de prueba:")
        print(f"   Original: '{case}'")
        
        try:
            # Hacer request al endpoint
            response = requests.post(
                API_URL,
                json={"text": case},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"   ✅ Normalizado: '{data['normalized']}'")
                    print(f"   🔧 Cambió: {data['was_normalized']}")
                    print(f"   🤖 Gemini disponible: {data['gemini_available']}")
                else:
                    print(f"   ❌ Error: {data.get('error')}")
            else:
                print(f"   ❌ Error HTTP {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ ERROR: No se pudo conectar al servidor")
            print("   💡 Asegúrate de que el servidor esté corriendo en http://localhost:5000")
            break
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print("\n" + "="*60)
    print("✅ Pruebas completadas")
    print("="*60)

if __name__ == "__main__":
    test_normalize_endpoint()
