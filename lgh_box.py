#!/usr/bin/env python3
# LGH BOX - Ethical OSINT Toolkit

import os
import sys
import time
import json
import hashlib
import requests
from colorama import Fore, Style, init

init(autoreset=True)

# =========================
# UTILIDADES
# =========================
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input(Fore.YELLOW + "\nPresiona ENTER para continuar...")

def red(text):
    return Fore.RED + text + Style.RESET_ALL

def green(text):
    return Fore.GREEN + text + Style.RESET_ALL

def cyan(text):
    return Fore.CYAN + text + Style.RESET_ALL

def yellow(text):
    return Fore.YELLOW + text + Style.RESET_ALL

# =========================
# BANNER
# =========================
def banner():
    clear()
    print(red(r"""
██╗     ██████╗ ██╗  ██╗    ██████╗  ██████╗ ██╗  ██╗
██║     ██╔════╝ ██║  ██║    ██╔══██╗██╔═══██╗╚██╗██╔╝
██║     ██║  ███╗███████║    ██████╔╝██║   ██║ ╚███╔╝ 
██║     ██║   ██║██╔══██║    ██╔══██╗██║   ██║ ██╔██╗ 
███████╗╚██████╔╝██║  ██║    ██████╔╝╚██████╔╝██╔╝ ██╗
╚══════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝
    """))
    print(yellow("Ethical OSINT Toolkit | Read-only | No intrusion\n"))

# =========================
# HASH TOOLS
# =========================
def hash_tools():
    clear()
    print(cyan("== HASH TOOLS =="))
    text = input("Texto a hashear: ").encode("utf-8")

    hashes = {
        "MD5": hashlib.md5(text).hexdigest(),
        "SHA1": hashlib.sha1(text).hexdigest(),
        "SHA256": hashlib.sha256(text).hexdigest(),
        "SHA512": hashlib.sha512(text).hexdigest(),
    }

    print()
    for k, v in hashes.items():
        print(green(f"{k}: ") + v)

    pause()

# =========================
# IP INTELLIGENCE (MULTI-FUENTE)
# =========================
def ip_intel():
    clear()
    print(cyan("== IP INTELLIGENCE =="))
    ip = input("IP (deja vacío para tu IP): ").strip()

    results = {}

    # Fuente 1: ipwho.is
    try:
        r = requests.get(f"https://ipwho.is/{ip}", timeout=10).json()
        if r.get("success", True):
            results["ipwho.is"] = {
                "ip": r.get("ip"),
                "country": r.get("country"),
                "region": r.get("region"),
                "city": r.get("city"),
                "lat": r.get("latitude"),
                "lon": r.get("longitude"),
                "isp": r.get("isp"),
                "asn": r.get("asn"),
                "proxy": r.get("proxy"),
            }
    except Exception:
        pass

    # Fuente 2: ipapi.co
    try:
        r = requests.get(f"https://ipapi.co/{ip}/json/", timeout=10).json()
        results["ipapi.co"] = {
            "ip": r.get("ip"),
            "country": r.get("country_name"),
            "region": r.get("region"),
            "city": r.get("city"),
            "lat": r.get("latitude"),
            "lon": r.get("longitude"),
            "org": r.get("org"),
        }
    except Exception:
        pass

    # Fuente 3: ipinfo.io
    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10).json()
        loc = r.get("loc", "")
        lat, lon = (loc.split(",") + ["", ""])[:2]
        results["ipinfo.io"] = {
            "ip": r.get("ip"),
            "country": r.get("country"),
            "region": r.get("region"),
            "city": r.get("city"),
            "lat": lat,
            "lon": lon,
            "org": r.get("org"),
        }
    except Exception:
        pass

    if not results:
        print(red("No se pudo obtener información."))
        pause()
        return

    print()
    for src, data in results.items():
        print(yellow(f"[{src}]"))
        for k, v in data.items():
            print(f"  {k}: {v}")
        print()

    pause()

# =========================
# OSINT DE USUARIOS (PASIVO)
# =========================
PLATFORMS = {
    "Facebook": "https://www.facebook.com/{}",
    "Instagram": "https://www.instagram.com/{}/",
    "X/Twitter": "https://x.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "GitHub": "https://github.com/{}",
}

def osint_users():
    clear()
    print(cyan("== OSINT USUARIOS (PASIVO) =="))
    username = input("Username a analizar: ").strip()
    if not username:
        return

    print()
    for name, url in PLATFORMS.items():
        link = url.format(username)
        try:
            r = requests.head(link, allow_redirects=True, timeout=10)
            status = "EXISTE" if r.status_code in (200, 301, 302) else "NO ENCONTRADO"
        except Exception:
            status = "ERROR"

        color = green if status == "EXISTE" else yellow
        print(color(f"{name}: {status}") + f" -> {link}")

    print(yellow("\nNota: verificación pasiva basada en respuesta HTTP."))
    pause()

# =========================
# MI IP
# =========================
def my_ip():
    clear()
    print(cyan("== MI IP =="))
    try:
        r = requests.get("https://api.ipify.org?format=json", timeout=10).json()
        print(green("Tu IP pública: ") + r.get("ip"))
    except Exception:
        print(red("No se pudo obtener tu IP."))
    pause()

# =========================
# MENÚ
# =========================
def menu():
    while True:
        banner()
        print(cyan("1) Hash Tools"))
        print(cyan("2) IP Intelligence"))
        print(cyan("3) OSINT Usuarios (Facebook / Instagram / X / TikTok / GitHub)"))
        print(cyan("4) Ver mi IP"))
        print(cyan("0) Salir"))

        opt = input("\nSelecciona una opción: ").strip()

        if opt == "1":
            hash_tools()
        elif opt == "2":
            ip_intel()
        elif opt == "3":
            osint_users()
        elif opt == "4":
            my_ip()
        elif opt == "0":
            print(yellow("Saliendo..."))
            time.sleep(0.5)
            sys.exit(0)
        else:
            print(red("Opción inválida."))
            time.sleep(0.8)

if __name__ == "__main__":
    menu()