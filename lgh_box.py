#!/usr/bin/env python3
# =========================================
# LGHBOX · Ethical OSINT Toolkit
# de parte del equipo de LA GRAN HERMANDAD
# =========================================

import json
import requests
import time
import os
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from sys import stderr

# ===== COLORES =====
Bl = '\033[30m'
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'
End = '\033[0m'

# ===== UTILIDADES =====
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input(f"\n{Wh}[ {Gr}+ {Wh}] Presiona Enter para continuar")

def is_option(func):
    def wrapper(*args, **kwargs):
        run_banner()
        func(*args, **kwargs)
    return wrapper

# ===== FUNCIONES =====
@is_option
def IP_Track():
    ip = input(f"{Wh}\n Enter IP target : {Gr}")  # INPUT IP ADDRESS
    print()
    print(f' {Wh}============= {Gr}SHOW INFORMATION IP ADDRESS {Wh}=============')
    req_api = requests.get(f"http://ipwho.is/{ip}")  # API IPWHOIS.IS
    ip_data = json.loads(req_api.text)
    time.sleep(2)
    print(f"{Wh}\n IP target       :{Gr}", ip)
    print(f"{Wh} Type IP         :{Gr}", ip_data["type"])
    print(f"{Wh} Country         :{Gr}", ip_data["country"])
    print(f"{Wh} Country Code    :{Gr}", ip_data["country_code"])
    print(f"{Wh} City            :{Gr}", ip_data["city"])
    print(f"{Wh} Continent       :{Gr}", ip_data["continent"])
    print(f"{Wh} Continent Code  :{Gr}", ip_data["continent_code"])
    print(f"{Wh} Region          :{Gr}", ip_data["region"])
    print(f"{Wh} Region Code     :{Gr}", ip_data["region_code"])
    print(f"{Wh} Latitude        :{Gr}", ip_data["latitude"])
    print(f"{Wh} Longitude       :{Gr}", ip_data["longitude"])
    lat = int(ip_data['latitude'])
    lon = int(ip_data['longitude'])
    print(f"{Wh} Maps            :{Gr}", f"https://www.google.com/maps/@{lat},{lon},8z")
    print(f"{Wh} EU              :{Gr}", ip_data["is_eu"])
    print(f"{Wh} Postal          :{Gr}", ip_data["postal"])
    print(f"{Wh} Calling Code    :{Gr}", ip_data["calling_code"])
    print(f"{Wh} Capital         :{Gr}", ip_data["capital"])
    print(f"{Wh} Borders         :{Gr}", ip_data["borders"])
    print(f"{Wh} Country Flag    :{Gr}", ip_data["flag"]["emoji"])
    print(f"{Wh} ASN             :{Gr}", ip_data["connection"]["asn"])
    print(f"{Wh} ORG             :{Gr}", ip_data["connection"]["org"])
    print(f"{Wh} ISP             :{Gr}", ip_data["connection"]["isp"])
    print(f"{Wh} Domain          :{Gr}", ip_data["connection"]["domain"])
    print(f"{Wh} ID              :{Gr}", ip_data["timezone"]["id"])
    print(f"{Wh} ABBR            :{Gr}", ip_data["timezone"]["abbr"])
    print(f"{Wh} DST             :{Gr}", ip_data["timezone"]["is_dst"])
    print(f"{Wh} Offset          :{Gr}", ip_data["timezone"]["offset"])
    print(f"{Wh} UTC             :{Gr}", ip_data["timezone"]["utc"])
    print(f"{Wh} Current Time    :{Gr}", ip_data["timezone"]["current_time"])
    
    except Exception as e:
        print(f"{Re}Error al obtener datos de la IP")

    pause()

@is_option
def phoneGW():
    phone = input(f"\n{Wh}Número objetivo (Ej +598XXXXXXXX): {Gr}")

    try:
        parsed = phonenumbers.parse(phone)
        region = phonenumbers.region_code_for_number(parsed)
        operador = carrier.name_for_number(parsed, "es")
        location = geocoder.description_for_number(parsed, "es")
        valid = phonenumbers.is_valid_number(parsed)
        possible = phonenumbers.is_possible_number(parsed)
        tz = ", ".join(timezone.time_zones_for_number(parsed))

        print(f"\n {Wh}========== {Gr}INFORMACIÓN DEL NÚMERO {Wh}==========")
        print(f"{Wh}Ubicación         :{Gr} {location}")
        print(f"{Wh}Región            :{Gr} {region}")
        print(f"{Wh}Operador          :{Gr} {operador}")
        print(f"{Wh}Zona horaria      :{Gr} {tz}")
        print(f"{Wh}Válido            :{Gr} {valid}")
        print(f"{Wh}Posible           :{Gr} {possible}")
        print(f"{Wh}Formato internacional:{Gr} {phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
    except:
        print(f"{Re}Número inválido")

    pause()

@is_option
def TrackLu():
    username = input(f"\n{Wh}Username a buscar: {Gr}")

    redes = [
        ("Facebook", "https://www.facebook.com/{}"),
        ("Twitter/X", "https://twitter.com/{}"),
        ("Instagram", "https://www.instagram.com/{}"),
        ("GitHub", "https://github.com/{}"),
        ("TikTok", "https://www.tiktok.com/@{}"),
        ("LinkedIn", "https://www.linkedin.com/in/{}"),
        ("YouTube", "https://www.youtube.com/{}"),
        ("Pinterest", "https://www.pinterest.com/{}"),
        ("Telegram", "https://t.me/{}")
    ]

    print(f"\n {Wh}========== {Gr}RESULTADOS OSINT DE USERNAME {Wh}==========\n")
    for nombre, url in redes:
        link = url.format(username)
        try:
            r = requests.get(link, timeout=10)
            if r.status_code == 200:
                print(f"{Wh}[ {Gr}+ {Wh}] {nombre}: {Gr}{link}")
            else:
                print(f"{Wh}[ {Ye}! {Wh}] {nombre}: {Ye}No encontrado")
        except:
            print(f"{Wh}[ {Re}! {Wh}] {nombre}: Error")

    pause()

@is_option
def showIP():
    try:
        ip = requests.get("https://api.ipify.org").text
        print(f"\n {Wh}========== {Gr}TU IP PÚBLICA {Wh}==========")
        print(f"{Wh}IP:{Gr} {ip}")
    except:
        print(f"{Re}No se pudo obtener tu IP")

    pause()

# ===== MENÚ =====
options = {
    1: ("IP Tracker", IP_Track),
    2: ("Mostrar mi IP", showIP),
    3: ("Información de número telefónico", phoneGW),
    4: ("OSINT de Username", TrackLu),
    0: ("Salir", exit)
}

def menu():
    clear()
    run_banner()
    print()
    for k, v in options.items():
        print(f"{Wh}[ {k} ] {Gr}{v[0]}")

def run_banner():
    stderr.writelines(f"""{Re}
██╗     ██████╗ ██╗  ██╗██████╗  ██████╗ ██╗  ██╗
██║    ██╔════╝ ██║  ██║██╔══██╗██╔═══██╗╚██╗██╔╝
██║    ██║  ███╗███████║██████╔╝██║   ██║ ╚███╔╝ 
██║    ██║   ██║██╔══██║██╔══██╗██║   ██║ ██╔██╗ 
███████╗╚██████╔╝██║  ██║██████╔╝╚██████╔╝██╔╝ ██╗
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝
{Wh}LGHBOX · Ethical OSINT Toolkit
{Re}de parte del equipo de LA GRAN HERMANDAD
{End}
""")

def main():
    while True:
        menu()
        try:
            opt = int(input(f"\n{Wh}Selecciona una opción: {Gr}"))
            if opt in options:
                options[opt][1]()
            else:
                print(f"{Ye}Opción inválida")
                time.sleep(1)
        except KeyboardInterrupt:
            break
        except:
            print(f"{Re}Error")
            time.sleep(1)

if __name__ == "__main__":
    main()