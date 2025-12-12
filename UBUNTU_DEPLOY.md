# ☁️ Guía de Despliegue en Ubuntu VPS

Esta es la forma **más robusta y recomendada** de desplegar tu proyecto completo (AtoM + Chatbot + Bases de Datos).

---

## Paso 1: Consigue un Servidor (VPS)

Puedes usar cualquier proveedor. Recomendaciones económicas:
- **DigitalOcean** (Basic Droplet)
- **Hetzner** (Cloud)
- **Vultr**
- **Linode**

**Requisitos mínimos:**
- Sistema Operativo: **Ubuntu 22.04 LTS** (o 24.04)
- RAM: **2 GB** (recomendado 4 GB si es posible, ya que Elasticsearch consume bastante)
- Disco: 20 GB+

---

## Paso 2: Conéctate al Servidor

Usa una terminal (PowerShell en Windows o Terminal en Mac/Linux):

```bash
ssh root@TU_IP_DEL_SERVIDOR
```
*(Reemplaza `TU_IP_DEL_SERVIDOR` con la IP que te dio tu proveedor, ej: 143.20.10.5)*

---

## Paso 3: Ejecuta el Despliegue Automático

Una vez dentro del servidor, simplemente **copia y pega** este bloque de código y presiona Enter:

```bash
wget https://raw.githubusercontent.com/Akshoon/NAXO/main/deploy_ubuntu.sh
chmod +x deploy_ubuntu.sh
./deploy_ubuntu.sh
```

> **Nota:** El script te pedirá tu `GEMINI_API_KEY` durante el proceso. Tenla a mano.

---

## Paso 4: ¡Listo!

El script hará todo el trabajo sucio:
1. Instalará Docker y Docker Compose
2. Descargará tu código
3. Configurará las variables
4. Levantará todos los servicios (AtoM, MySQL, Chatbot, etc.)

Al terminar, te mostrará la URL donde puedes ver tu proyecto:
`http://TU_IP:8080`

---

## Comandos Útiles de Mantenimiento

Si necesitas gestionar tu servidor en el futuro:

**Ver logs (qué está pasando):**
```bash
cd NAXO
docker compose logs -f
```

**Reiniciar el servidor:**
```bash
cd NAXO
docker compose restart
```

**Actualizar con cambios de GitHub:**
```bash
cd NAXO
git pull
docker compose up -d --build
```
