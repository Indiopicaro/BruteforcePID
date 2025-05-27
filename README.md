# PID Bruteforcer

Herramienta para descubrir procesos en sistemas Linux mediante fuerza bruta sobre el endpoint `/proc/[PID]/cmdline`.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

## 📌 Descripción

Este script realiza fuerza bruta sobre PIDs (Process IDs) accediendo a `/proc/[PID]/cmdline` para descubrir procesos en ejecución en sistemas Linux vulnerables que exponen este endpoint.

## ✨ Características

- Escaneo acelerado con multihilo (20 hilos concurrentes)
- Detección de procesos con respuesta de contenido significativo (>82 bytes)
- Soporte para guardar resultados en archivo

## 📦 Requisitos

- Python 3.x
- Bibliotecas: `requests`, `tqdm`

## 🛠 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/Indiopicaro/BruteforcePID.git
cd BruteforcePID
```

## 🚀 Uso
```bash
python3 BruteForcePID.py -u http://objetivo.com/ruta?param=/proc/PID/cmdline [-o output.txt]
```

Argumentos:
-u/--url: URL objetivo (debe contener el marcador PID)

-o/--output (opcional): Archivo para guardar resultados

