# 🔴 LGH BOX

LGH BOX es una herramienta de **OSINT ético** escrita en Python.  
Está diseñada para **análisis pasivo** de información pública con fines educativos y de investigación, **sin intrusión**, **sin automatización abusiva** y **sin interacción con cuentas privadas**.

---

## ⚠️ ADVERTENCIA ÉTICA Y DE SUPERVISIÓN

- Este proyecto debe usarse **únicamente con fines éticos y educativos**.
- Usalo **bajo tu propia supervisión y responsabilidad**.
- No incluye ni permite ataques, spam, flooding, fuerza bruta, bypass de seguridad ni envío de mensajes a servicios externos.
- Cualquier uso fuera de este marco es responsabilidad exclusiva del usuario.

---

## 📌 Herramientas incluidas (permitidas)


### 🌐 IP Intelligence (multi-fuente)
Consulta pasiva de IP usando **APIs públicas**:
- País, región, ciudad (aproximado)
- ISP / ASN
- Coordenadas aproximadas
- Indicadores de proxy/VPN cuando la fuente lo permite  
Nota: **no existe** precisión a nivel domicilio con IP pública.

### 👤 OSINT pasivo por plataforma
Verificación **pasiva** de existencia pública de usernames (sin login):
- Facebook
- Instagram
- X (Twitter)
- TikTok
- GitHub  
Método: comprobación HTTP/URLs públicas. No accede a datos privados.

### 📡 Ver mi IP
Obtención de IP pública mediante servicio público.

---

## 🚫 Herramientas NO incluidas (bloqueadas por ética)
Estas ideas **no están implementadas** y se dejan explícitamente deshabilitadas:
- Envío de mensajes masivos o “mensajes bomba”
- Automatización de interacción con redes sociales
- Uso de APIs privadas o evasión de límites
- Cualquier acción activa sobre cuentas reales

---

## 📁 Project Structure
LGH-BOX/
├─ main.py
├─ requirements.txt
└─ README.md

---

## ⚙️ Installation on Linux (deb)
```
sudo apt-get update
sudo apt-get install git
sudo apt-get install python3 python3-pip
```

---

## ⚙️ Installation on Termux
```
pkg update
pkg install git
pkg install python
```

---

## ▶️ Usage Tool
```
git clone https://github.com/cycles-R/LGHBOX
cd LGHBOX
pip3 install -r requirements.txt
python3 lgh_box.py
```

---

## 📦 Requirements
- Python **3.8 o superior**
- pip / pip3
- Git
- Conexión a Internet (APIs públicas)

---

## 🧪 How it works
1. Ejecutás la herramienta
2. Elegís una opción del menú
3. Ingresás el dato solicitado (IP, texto, username)
4. LGH BOX realiza **análisis pasivo** y muestra resultados


---

## ⚖️ Legal Notice
LGH BOX es una herramienta de **OSINT ético**.  
El desarrollador no se responsabiliza por usos indebidos.

---
