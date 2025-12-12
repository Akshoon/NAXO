# 📡 Cómo probar la API con Postman

Aquí tienes los detalles para probar cada endpoint del Chatbot.

## Base URL
Si estás corriendo localmente (Docker): `http://localhost:5000`

---

## 1. Chat con la IA
El endpoint principal para conversar.

- **Método:** `POST`
- **URL:** `http://localhost:5000/api/chat`
- **Headers:** 
  - `Content-Type`: `application/json`
- **Body (JSON):**
  ```json
  {
    "query": "víctimas dictadura 1973",
    "session_id": "test-session-1"
  }
  ```

---

## 2. Búsqueda por Categoría
Para buscar documentos filtrando por metadatos específicos.

- **Método:** `POST`
- **URL:** `http://localhost:5000/api/search-by-category`
- **Headers:** 
  - `Content-Type`: `application/json`
- **Body (JSON):**
  ```json
  {
    "category_type": "materias", 
    "category_name": "Derechos Humanos"
  }
  ```
  *Nota: `category_type` puede ser: "materias", "autores", o "lugares".*

---

## 3. Obtener Categorías
Lista las categorías disponibles para usar en el endpoint anterior.

- **Método:** `GET`
- **URL:** `http://localhost:5000/api/categories`
- **Body:** Ninguno.

---

## 4. Health Check (Estado)
Verifica que la API esté funcionando correctamente.

- **Método:** `GET`
- **URL:** `http://localhost:5000/api/health`
- **Body:** Ninguno.
