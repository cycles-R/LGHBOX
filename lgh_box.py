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
    ip = input(f"{Wh}\nIP objetivo: {Gr}")
    print(f'\n {Wh}============= {Gr}INFORMACIÓN DE LA IP {Wh}=============')

    try:
        req = requests.get(f"http://ipwho.is/{ip}", timeout=10)
        data = json.loads(req.text)

        print(f"{Wh}IP                :{Gr} {ip}")
        print(f"{Wh}Tipo              :{Gr} {data['type']}")
        print(f"{Wh}País              :{Gr} {data['country']}")
        print(f"{Wh}Código país       :{Gr} {data['country_code']}")
        print(f"{Wh}Ciudad            :{Gr} {data['city']}")
        print(f"{Wh}Región            :{Gr} {data['region']}")
        print(f"{Wh}Latitud           :{Gr} {data['latitude']}")
        print(f"{Wh}Longitud          :{Gr} {data['longitude']}")
        print(f"{Wh}Mapa              :{Gr} https://www.google.com/maps/@{data['latitude']},{data['longitude']},8z")
        print(f"{Wh}ISP               :{Gr} {data['connection']['isp']}")
        print(f"{Wh}ORG               :{Gr} {data['connection']['org']}")
        print(f"{Wh}ASN               :{Gr} {data['connection']['asn']}")
        print(f"{Wh}Zona horaria      :{Gr} {data['timezone']['id']}")
        print(f"{Wh}Hora actual       :{Gr} {data['timezone']['current_time']}")
    except:
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