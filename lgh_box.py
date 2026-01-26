import os
import time
import json
import re
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from sys import stderr
from colorama import Fore, Style, init
import hashlib
import random
import string
import socket

init(autoreset=True)

# ===================== UI =====================

BANNER = f"""
{Fore.CYAN}██╗      ██████╗ ██╗  ██╗     ██████╗  ██████╗ ██╗  ██╗
██║     ██╔════╝ ██║  ██║     ██╔══██╗██╔═══██╗╚██╗██╔╝
██║     ██║  ███╗███████║     ██████╔╝██║   ██║ ╚███╔╝ 
██║     ██║   ██║██╔══██║     ██╔══██╗██║   ██║ ██╔██╗ 
███████╗╚██████╔╝██║  ██║     ██████╔╝╚██████╔╝██╔╝ ██╗
╚══════╝ ╚═════╝ ╚═╝  ╚═╝     ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
{Fore.YELLOW}                    DE PARTE DEL EQUIPO DE LA GRAN HERMANDAD{Style.DIM}
"""

MENU = f"""
{Fore.GREEN} 1 : BOX Número Telefónico
 2 : BOX Dirección IP
 3 : Mostrar mi IP pública
 4 : Buscar cuentas por nombre (OSINT demo)
 5 : Verificador de contraseñas débiles
 6 : Generador de contraseñas seguras
 7 : Detector de tipo de hash
 8 : Análisis de cabeceras HTTP
 9 : IP pública vs privada
10 : Escáner de puertos (local / seguro)
11 : Análisis de correo electrónico
12 : Metadatos de archivo (básico)
13 : Simulador de phishing (educativo)
14 : Simulador de fuerza bruta (bloqueado)
15 : Checklist de hardening
16 : Modo auditor (reporte simple)
17 : Limpiar pantalla
99 : Salir{Style.RESET_ALL}
"""

last_result = None

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def loading(msg):
    print(Fore.YELLOW + msg, end="", flush=True)
    for _ in range(3):
        time.sleep(0.4)
        print(".", end="", flush=True)
    print("\n")

def pause():
    input(Fore.WHITE + "\nENTER para continuar...")

# ===================== BOX CORE =====================

def box_phone():
    global last_result
    number = input("Número (ej: +5989xxxxxxx): ").strip()
    try:
        parsed = phonenumbers.parse(number, None)
        if not phonenumbers.is_valid_number(parsed):
            print(Fore.RED + "[ERROR] Número inválido")
            return

        loading("[BOX] Analizando número")
        last_result = {
            "Tipo": "Teléfono",
            "Formato": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
            "País": geocoder.description_for_number(parsed, "es"),
            "Operador": carrier.name_for_number(parsed, "es"),
            "Zona Horaria": list(timezone.time_zones_for_number(parsed))
        }
        print(Fore.GREEN + "[RESULTADO]")
        for k, v in last_result.items():
            print(Fore.CYAN + f"{k}: " + Fore.WHITE + f"{v}")
    except Exception as e:
        print(Fore.RED + "[ERROR]", e, file=stderr)

def box_ip():
    global last_result
    ip = input("IP (ej: 8.8.8.8): ").strip()
    try:
        loading("[BOX] Analizando IP")
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        data = r.json()
        if data.get("status") != "success":
            print(Fore.RED + "[ERROR] IP no válida")
            return
        last_result = {
            "Tipo": "IP",
            "IP": data.get("query"),
            "País": data.get("country"),
            "Región": data.get("regionName"),
            "Ciudad": data.get("city"),
            "ISP": data.get("isp"),
            "Latitud": data.get("lat"),
            "Longitud": data.get("lon")
        }
        print(Fore.GREEN + "[RESULTADO]")
        for k, v in last_result.items():
            print(Fore.CYAN + f"{k}: " + Fore.WHITE + f"{v}")
    except Exception as e:
        print(Fore.RED + "[ERROR]", e, file=stderr)

def my_ip():
    loading("[BOX] Obteniendo IP pública")
    r = requests.get("https://api.ipify.org?format=json", timeout=10)
    print(Fore.GREEN + "[RESULTADO]")
    print(Fore.CYAN + "IP Pública: " + Fore.WHITE + r.json().get("ip"))

def search_accounts():
    username = input("Nombre a buscar: ").strip()
    if not username:
        print(Fore.RED + "[ERROR] Nombre vacío")
        return
    loading("[BOX] Buscando coincidencias públicas")
    results = [f"{username}_oficial", f"{username}.dev", f"real_{username}", f"{username}123"]
    print(Fore.GREEN + "[RESULTADO]")
    for i, r in enumerate(results, 1):
        print(Fore.CYAN + f"{i}. " + Fore.WHITE + r)

# ===================== SECURITY TOOLS =====================

def password_checker():
    pwd = input("Contraseña a evaluar: ")
    score = 0
    rules = [
        (len(pwd) >= 12, "Longitud >= 12"),
        (re.search(r"[A-Z]", pwd), "Mayúsculas"),
        (re.search(r"[a-z]", pwd), "Minúsculas"),
        (re.search(r"\d", pwd), "Números"),
        (re.search(r"[^\w]", pwd), "Símbolos"),
    ]
    print(Fore.GREEN + "[RESULTADO]")
    for ok, name in rules:
        print((Fore.GREEN if ok else Fore.RED) + f"- {name}")
        score += int(bool(ok))
    print(Fore.CYAN + f"Score: {score}/5")

def password_generator():
    length = int(input("Longitud (ej: 16): ") or 16)
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    pwd = "".join(random.choice(chars) for _ in range(length))
    print(Fore.GREEN + "[RESULTADO]")
    print(Fore.WHITE + pwd)

def hash_detector():
    h = input("Hash: ").strip()
    l = len(h)
    guess = {32:"MD5",40:"SHA1",64:"SHA256",128:"SHA512"}.get(l,"Desconocido")
    print(Fore.GREEN + "[RESULTADO]")
    print(Fore.CYAN + "Posible tipo: " + Fore.WHITE + guess)

def http_headers():
    url = input("URL (https://example.com): ").strip()
    loading("[BOX] Analizando cabeceras HTTP")
    r = requests.get(url, timeout=10)
    print(Fore.GREEN + "[RESULTADO]")
    for k, v in r.headers.items():
        print(Fore.CYAN + f"{k}: " + Fore.WHITE + v)

def ip_private_public():
    ip = input("IP a evaluar: ").strip()
    private_ranges = ("10.", "172.", "192.168.")
    is_private = ip.startswith(private_ranges)
    print(Fore.GREEN + "[RESULTADO]")
    print(Fore.CYAN + "Tipo: " + Fore.WHITE + ("Privada" if is_private else "Pública"))

def port_scan_local():
    host = input("Host (localhost o IP propia): ").strip()
    ports = [22, 80, 443, 8080]
    print(Fore.YELLOW + "[INFO] Escaneo limitado y seguro")
    for p in ports:
        s = socket.socket()
        s.settimeout(0.5)
        try:
            s.connect((host, p))
            print(Fore.GREEN + f"Puerto {p}: ABIERTO")
        except:
            print(Fore.RED + f"Puerto {p}: CERRADO")
        finally:
            s.close()

def email_analysis():
    email = input("Email: ").strip()
    print(Fore.GREEN + "[RESULTADO]")
    print(Fore.CYAN + "Formato válido: " + Fore.WHITE + str(bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))))
    domain = email.split("@")[-1] if "@" in email else ""
    print(Fore.CYAN + "Dominio: " + Fore.WHITE + domain)

def file_metadata():
    path = input("Ruta del archivo: ").strip()
    if not os.path.exists(path):
        print(Fore.RED + "[ERROR] No existe")
        return
    st = os.stat(path)
    print(Fore.GREEN + "[RESULTADO]")
    print(Fore.CYAN + f"Tamaño: {st.st_size} bytes")
    print(Fore.CYAN + f"Modificado: {time.ctime(st.st_mtime)}")

def phishing_sim():
    print(Fore.YELLOW + "[SIMULACIÓN EDUCATIVA]")
    print("Indicadores comunes: urgencia, links acortados, remitente extraño.")

def brute_force_sim():
    print(Fore.RED + "[BLOQUEADO]")
    print("Solo explicación teórica. No se ejecuta fuerza bruta.")

def hardening_checklist():
    items = [
        "2FA activado",
        "Contraseñas únicas",
        "Actualizaciones al día",
        "Backups",
        "Firewall activo"
    ]
    print(Fore.GREEN + "[CHECKLIST]")
    for i in items:
        print(Fore.CYAN + "- " + Fore.WHITE + i)

def auditor_mode():
    print(Fore.GREEN + "[REPORTE]")
    print("Riesgos comunes detectables: contraseñas débiles, falta de 2FA, headers inseguros.")

# ===================== MAIN =====================

def main():
    while True:
        clear()
        print(BANNER)
        print(MENU)
        c = input("Choice > ").strip()
        if c == "1": box_phone()
        elif c == "2": box_ip()
        elif c == "3": my_ip()
        elif c == "4": search_accounts()
        elif c == "5": password_checker()
        elif c == "6": password_generator()
        elif c == "7": hash_detector()
        elif c == "8": http_headers()
        elif c == "9": ip_private_public()
        elif c == "10": port_scan_local()
        elif c == "11": email_analysis()
        elif c == "12": file_metadata()
        elif c == "13": phishing_sim()
        elif c == "14": brute_force_sim()
        elif c == "15": hardening_checklist()
        elif c == "16": auditor_mode()
        elif c == "17": clear()
        elif c == "99": break
        else: print(Fore.RED + "[ERROR] Opción inválida")
        pause()

if __name__ == "__main__":
    main()