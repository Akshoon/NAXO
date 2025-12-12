# 🚂 Guía de Despliegue en Railway.app

Esta guía te llevará paso a paso para desplegar **TODO el stack** del proyecto NAXO (AtoM + MySQL + Elasticsearch + Chatbot) en [Railway.app](https://railway.app/).

---

## ⚠️ Importante: Limitaciones de Railway

Railway tiene **limitaciones importantes** con tu stack actual:

### 🔴 Problemas con tu docker-compose.yml:

1. **Elasticsearch 5.6.16**: Versión muy antigua, no soportada bien en Railway
2. **AtoM 2.8/2.9**: Aplicación PHP compleja con muchas dependencias
3. **Múltiples contenedores**: 7 servicios es mucho para Railway Free
4. **Volúmenes**: Railway maneja volúmenes de forma diferente

### 💰 Costos Estimados

Railway Free Plan:
- ❌ **NO es suficiente** para 7 servicios
- Límite: $5 USD de crédito mensual
- Tu stack consumiría ~$20-30/mes

**Recomendación:** Usar Railway solo para el **Chatbot API** y desplegar AtoM localmente o en un VPS.

---

## 🎯 Opción Recomendada: Despliegue Híbrido

### Arquitectura Sugerida:

```
┌─────────────────────────────────────────┐
│  Railway.app (Nube)                     │
│  ├── Chatbot API (Flask)                │
│  └── PostgreSQL (para chatbot sessions) │
└─────────────────────────────────────────┘
                  ↕
┌─────────────────────────────────────────┐
│  Local o VPS                            │
│  ├── AtoM (PHP)                         │
│  ├── MySQL                              │
│  ├── Elasticsearch                      │
│  ├── Gearman                            │
│  └── Nginx                              │
└─────────────────────────────────────────┘
```

---

## 📋 Opción 1: Solo Chatbot en Railway (Recomendado)

### Paso 1: Crear cuenta en Railway

1. Ve a [railway.app](https://railway.app/)
2. **Sign up with GitHub**
3. Autoriza Railway a acceder a tus repositorios

### Paso 2: Crear nuevo proyecto

1. Dashboard de Railway → **New Project**
2. Selecciona **Deploy from GitHub repo**
3. Conecta tu repositorio `Akshoon/NAXO`
4. Railway detectará automáticamente el `Dockerfile`

### Paso 3: Configurar el servicio

**Root Directory:** `chatbot`

Esto le dice a Railway que use solo el subdirectorio del chatbot.

### Paso 4: Variables de Entorno

Agrega en **Variables**:

```env
GEMINI_API_KEY=tu_api_key_aqui
FLASK_ENV=production
PORT=8000
```

### Paso 5: Exponer Puerto

Railway debería detectar automáticamente el puerto 8000. Si no:

**Settings → Networking → Public Domain → Generate Domain**

### Paso 6: Deploy

Haz clic en **Deploy**. Railway:
- ✅ Clonará tu repositorio
- ✅ Construirá la imagen Docker
- ✅ Desplegará el contenedor
- ✅ Asignará una URL pública

---

## 📋 Opción 2: Todo el Stack en Railway (Costoso)

> ⚠️ **Advertencia:** Esta opción costará ~$20-30/mes y puede tener problemas de compatibilidad.

### Arquitectura Adaptada para Railway

Railway **NO soporta docker-compose directamente**, así que necesitas:

1. **Crear servicios separados** para cada componente
2. **Usar bases de datos managed** de Railway (PostgreSQL, no MySQL)
3. **Adaptar AtoM** para PostgreSQL (requiere modificaciones)
4. **Reemplazar Elasticsearch** con alternativa compatible

### Servicios Necesarios:

#### 1. Base de Datos
- **Railway PostgreSQL** (no MySQL nativo)
- Problema: AtoM requiere MySQL, necesitas migrar

#### 2. Chatbot API
- Root Directory: `chatbot`
- Dockerfile: `chatbot/Dockerfile`
- Variables: `GEMINI_API_KEY`, `FLASK_ENV`

#### 3. AtoM
- Root Directory: `.` (raíz)
- Dockerfile: `Dockerfile` (el de PHP)
- **Problema:** Requiere MySQL, no PostgreSQL

#### 4. Elasticsearch
- **Problema:** Railway no tiene Elasticsearch managed
- Alternativas:
  - Usar servicio externo (Elastic Cloud - $$$)
  - Omitir (limita búsqueda de AtoM)

#### 5. Nginx
- Root Directory: `docker/nginx`
- **Problema:** Configuración compleja

### Conclusión

❌ **No es viable** desplegar todo el stack AtoM en Railway sin modificaciones mayores.

---

## ✅ Opción 3: Solución Práctica Recomendada

### Para Chatbot (Producción):
- **Railway.app**: Chatbot API ✅
- **Koyeb**: Alternativa al chatbot (ya configurado)

### Para AtoM (Sistema completo):

#### **A) Local con Docker Compose**
```bash
cd c:\Users\diego\OneDrive\Desktop\NAXO
docker compose up
```
Accede en: `http://localhost:8080`

#### **B) VPS con Docker Compose** (Producción)

**Proveedores recomendados:**

| Proveedor | Precio | RAM | Disco |
|-----------|--------|-----|-------|
| **DigitalOcean** | $6/mes | 1 GB | 25 GB SSD |
| **Linode** | $5/mes | 1 GB | 25 GB SSD |
| **Vultr** | $6/mes | 1 GB | 25 GB SSD |
| **Hetzner** | €4/mes | 2 GB | 40 GB SSD |

**Pasos en VPS:**

1. Crear VPS con Ubuntu 22.04
2. Instalar Docker:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```
3. Clonar tu repo:
   ```bash
   git clone https://github.com/Akshoon/NAXO.git
   cd NAXO
   ```
4. Configurar variables:
   ```bash
   echo "GEMINI_API_KEY=tu_key" > .env
   ```
5. Levantar stack:
   ```bash
   docker compose up -d
   ```
6. Acceder via IP pública del VPS

---

## 🚀 Pasos Inmediatos Recomendados

### 1. Desplegar Chatbot en Railway (5 minutos)

```bash
# Ya tienes el código en GitHub
# Solo necesitas conectar Railway
```

1. [railway.app](https://railway.app/) → Sign up
2. New Project → Deploy from GitHub
3. Selecciona `Akshoon/NAXO`
4. Root Directory: `chatbot`
5. Variables: `GEMINI_API_KEY`
6. Deploy ✅

### 2. Probar AtoM Localmente

```bash
cd c:\Users\diego\OneDrive\Desktop\NAXO
docker compose up
```

Verifica que funcione antes de pensar en producción.

### 3. Evaluar VPS para Producción

Si necesitas AtoM en producción:
- Contrata VPS (DigitalOcean $6/mes)
- Despliega con docker-compose
- Configura dominio

---

## 📊 Comparación de Opciones

| Aspecto | Railway Solo Chatbot | Railway Todo | VPS + Docker Compose |
|---------|---------------------|--------------|---------------------|
| **Costo** | $0-5/mes | $20-30/mes | $6/mes |
| **Complejidad** | ⭐ Fácil | ⭐⭐⭐⭐⭐ Muy difícil | ⭐⭐⭐ Moderado |
| **AtoM Funcional** | ❌ No | ⚠️ Requiere migración | ✅ Sí |
| **Chatbot Funcional** | ✅ Sí | ✅ Sí | ✅ Sí |
| **Mantenimiento** | Bajo | Alto | Medio |
| **Escalabilidad** | Alta | Baja | Media |

---

## 🎯 Mi Recomendación Final

### Para Empezar (Ahora):

1. ✅ **Chatbot en Railway** (gratis, 5 minutos)
2. ✅ **AtoM local** con docker-compose (desarrollo)

### Para Producción (Cuando estés listo):

1. ✅ **Chatbot en Railway o Koyeb** (gratis)
2. ✅ **AtoM en VPS** con docker-compose ($6/mes)
3. ✅ **Dominio** apuntando al VPS

---

## 📚 Recursos

- [Railway Docs](https://docs.railway.app/)
- [Railway Pricing](https://railway.app/pricing)
- [DigitalOcean Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-22-04)
- [AtoM Documentation](https://www.accesstomemory.org/docs/)

---

## 🆘 ¿Necesitas Ayuda?

Si decides ir por la opción del VPS, puedo ayudarte con:
1. Seleccionar proveedor
2. Configurar el servidor
3. Desplegar docker-compose
4. Configurar dominio y SSL

¿Quieres que te ayude a desplegar el chatbot en Railway ahora? 🚀
