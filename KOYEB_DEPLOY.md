# 🚀 Guía de Despliegue en Koyeb

Esta guía te llevará paso a paso para desplegar el **Chatbot API** del Archivo Patrimonial UAH en [Koyeb](https://www.koyeb.com/).

## 📋 Pre-requisitos

Antes de comenzar, asegúrate de tener:

1. ✅ **Cuenta en Koyeb** (gratuita): [Registrarse aquí](https://app.koyeb.com/auth/signup)
2. ✅ **Cuenta en GitHub** con tu proyecto NAXO
3. ✅ **API Key de Google Gemini**: Obtener en [Google AI Studio](https://aistudio.google.com/app/apikey)
4. ✅ **Proyecto en repositorio de GitHub** (público o privado)

---

## 🎯 Paso 1: Preparar tu Repositorio de GitHub

### 1.1 Inicializar Git (si no lo has hecho)

```bash
cd c:\Users\diego\OneDrive\Desktop\NAXO
git init
git add .
git commit -m "Preparar proyecto para Koyeb"
```

### 1.2 Crear repositorio en GitHub

1. Ve a [GitHub](https://github.com/new)
2. Crea un nuevo repositorio llamado `naxo-chatbot`
3. No inicialices con README (ya tienes contenido)

### 1.3 Conectar y subir tu código

```bash
git remote add origin https://github.com/TU_USUARIO/naxo-chatbot.git
git branch -M main
git push -u origin main
```

> **Nota**: Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub.

---

## 🔧 Paso 2: Configurar Servicio en Koyeb

### 2.1 Acceder al Dashboard

1. Inicia sesión en [Koyeb](https://app.koyeb.com/)
2. Haz clic en **"Create App"** o **"New Service"**

### 2.2 Conectar GitHub

1. Selecciona **"GitHub"** como fuente
2. Autoriza a Koyeb para acceder a tus repositorios
3. Selecciona el repositorio `naxo-chatbot`
4. Rama: **main**

### 2.3 Configurar Build

En la sección **Build Configuration**:

- **Builder**: Docker
- **Dockerfile path**: `chatbot/Dockerfile`
- **Docker build context**: `chatbot` *(muy importante)*
- **Docker build args**: Dejar vacío

![Build Configuration](https://i.imgur.com/example.png)

### 2.4 Configurar Variables de Entorno

En la sección **Environment Variables**, agrega:

| Nombre | Valor | Tipo |
|--------|-------|------|
| `GEMINI_API_KEY` | `TU_API_KEY_AQUI` | Secret |
| `FLASK_ENV` | `production` | Plain Text |

> **⚠️ Importante**: Marca `GEMINI_API_KEY` como **Secret** para que no sea visible en los logs.

Para obtener tu API Key de Gemini:
1. Ve a [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Clic en **"Create API Key"**
3. Copia la clave y pégala en Koyeb

### 2.5 Configurar Recursos

En la sección **Instance**:

- **Instance type**: Web Service
- **Regions**: Selecciona la más cercana (ej: `was` para Washington, `fra` para Frankfurt)
- **Instance size**: **Nano** (512 MB RAM) o **Micro** (1 GB RAM)
  - *Nano es suficiente para pruebas*
  - *Micro recomendado para producción*

### 2.6 Configurar Health Check

En la sección **Health checks**:

- **Health check path**: `/health`
- **Port**: `8000` (o el que Koyeb asigne automáticamente)
- **Grace period**: 40 segundos

### 2.7 Configurar Exposición

En la sección **Exposed ports**:

- **Port**: Puerto automático (Koyeb lo detectará del `EXPOSE` en Dockerfile)
- **Protocol**: HTTP
- **Public**: ✅ Habilitado

### 2.8 Nombrar el Servicio

- **Service name**: `naxo-chatbot-api`
- **App name**: `naxo` (o el que prefieras)

---

## 🚀 Paso 3: Desplegar

1. Revisa toda la configuración
2. Haz clic en **"Deploy"**
3. Espera mientras Koyeb:
   - ✅ Clona tu repositorio
   - ✅ Construye la imagen Docker (~3-5 minutos)
   - ✅ Despliega el contenedor
   - ✅ Ejecuta el healthcheck

El build puede tomar **5-10 minutos** la primera vez debido al tamaño de los archivos de datos (embeddings 57MB + documentos 6.5MB).

---

## 📊 Paso 4: Monitorear el Despliegue

### 4.1 Ver Logs en Tiempo Real

En el dashboard de Koyeb:

1. Ve a tu servicio `naxo-chatbot-api`
2. Clic en la pestaña **"Logs"**
3. Deberías ver:

```
🚀 INICIANDO CHATBOT DEL ARCHIVO PATRIMONIAL UAH
======================================================================
📊 Documentos cargados: XXXX
🧠 Embeddings disponibles: XXXX
🤖 Gemini API: ✅ Disponible
🌐 Servidor Flask: http://0.0.0.0:8000
❤️ Health check: GET /health
🌍 Entorno: production
======================================================================
✅ Sistema listo para recibir consultas!
```

### 4.2 Verificar Health Check

Una vez desplegado, ve a la URL de tu servicio (algo como `https://naxo-chatbot-api-TU_ORG.koyeb.app/health`):

Deberías ver una respuesta JSON:

```json
{
  "status": "healthy",
  "service": "chatbot-api",
  "version": "2.0",
  "gemini_available": true,
  "embeddings_ready": true,
  "documents_loaded": 1234,
  "embeddings_count": 1234
}
```

---

## ✅ Paso 5: Probar el Chatbot

### 5.1 Con cURL

```bash
curl -X POST https://naxo-chatbot-api-TU_ORG.koyeb.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Buscar documentos sobre derechos humanos", "session_id": "test-123"}'
```

### 5.2 Con Postman

1. **Method**: POST
2. **URL**: `https://naxo-chatbot-api-TU_ORG.koyeb.app/api/chat`
3. **Headers**:
   - `Content-Type: application/json`
4. **Body** (raw JSON):
   ```json
   {
     "query": "dictadura militar 1973",
     "session_id": "postman-test"
   }
   ```

### 5.3 Desde tu Frontend

Actualiza la URL del API en tu frontend para apuntar a:

```javascript
const API_URL = 'https://naxo-chatbot-api-TU_ORG.koyeb.app';
```

---

## 🔍 Troubleshooting

### ❌ Error: "Build failed - Dockerfile not found"

**Solución**: Verifica que el **Docker build context** esté configurado como `chatbot` (no raíz del proyecto).

---

### ❌ Error: "Health check failed"

**Causas comunes**:

1. **Puerto incorrecto**: Koyeb asigna el puerto dinámicamente via variable `PORT`. Verifica que tu app lo lea correctamente.
   
2. **Archivo de datos falta**: Verifica en logs que los archivos `clean_with_metadata.json`, `embeddings_cache.pkl`, y `search_index.pkl` se hayan copiado correctamente.

**Solución**:
- Revisa los logs en Koyeb
- Asegúrate que el healthcheck apunte a `/health` (no `/api/health`)
- Aumenta el **grace period** a 60 segundos si los archivos son muy grandes

---

### ❌ Error: "Gemini API: ❌ No disponible"

**Solución**: Verifica que la variable `GEMINI_API_KEY` esté configurada correctamente en Koyeb:

1. Ve a **Settings > Environment Variables**
2. Confirma que `GEMINI_API_KEY` existe y es correcta
3. **Redeploy** el servicio para aplicar cambios

---

### ❌ La app se queda "Deploying" indefinidamente

**Causas**:
- El healthcheck nunca pasa (revisa los logs)
- La app falla al iniciar (revisa los logs)

**Solución**:
1. Ve a **Logs** y busca errores
2. Verifica que Python pueda cargar todos los archivos
3. Si el problema persiste, aumenta el tamaño de instancia a **Micro**

---

### ⚠️ La app funciona pero responde lento

**Solución**:
- **Nano instances** tienen recursos limitados
- Considera upgradar a **Micro** (1 GB RAM) para mejor performance
- Los embeddings de 57MB pueden requerir más memoria

---

## 📈 Monitoreo Continuo

### Logs

Accede a logs en tiempo real desde el dashboard:

```
Dashboard > Tu Servicio > Logs
```

### Métricas

Koyeb proporciona métricas automáticas:

- **Request rate**: Requests por minuto
- **Response time**: Tiempo de respuesta promedio
- **Memory usage**: Uso de RAM
- **CPU usage**: Uso de CPU

---

## 🔄 Actualizaciones

Para actualizar tu app tras hacer cambios:

### Método 1: Auto-Deploy (Recomendado)

1. Haz commit y push a GitHub:
   ```bash
   git add .
   git commit -m "Actualización del chatbot"
   git push
   ```

2. Koyeb detectará el cambio y re-desplegará automáticamente ✅

### Método 2: Manual

1. Ve al dashboard de Koyeb
2. Selecciona tu servicio
3. Clic en **"Redeploy"**

---

## 💰 Costos

Koyeb ofrece:

- **Plan Free**: 
  - $5.00 USD de crédito mensual
  - 2 servicios Web activos
  - Suficiente para un chatbot de prueba/desarrollo

- **Plan Hobby** ($5.50/mes por servicio):
  - Para producción ligera
  - Más instancias y recursos

Consulta la [página de pricing](https://www.koyeb.com/pricing) para más detalles.

---

## 🎉 ¡Listo!

Tu chatbot ahora está desplegado en Koyeb y accesible públicamente. La URL será algo como:

```
https://naxo-chatbot-api-TU_ORG.koyeb.app
```

### Próximos Pasos

1. ✅ Integra esta URL en tu frontend
2. ✅ Configura un dominio personalizado (opcional)
3. ✅ Monitorea logs y métricas regularmente
4. ✅ Configura alertas en caso de errores

---

## 📚 Recursos Adicionales

- [Documentación de Koyeb](https://www.koyeb.com/docs)
- [Guía de Docker en Koyeb](https://www.koyeb.com/docs/build-and-deploy/deploy-a-docker-application)
- [Variables de Entorno en Koyeb](https://www.koyeb.com/docs/reference/environment-variables)
- [Dominios Personalizados](https://www.koyeb.com/docs/domains/overview)

---

## 🆘 Soporte

Si tienes problemas no cubiertos en esta guía:

1. Revisa los **logs en el dashboard de Koyeb**
2. Consulta la [documentación oficial](https://www.koyeb.com/docs)
3. Únete al [Discord de Koyeb](https://www.koyeb.com/discord) para soporte comunitario

---

**¡Éxito con tu despliegue! 🚀**
