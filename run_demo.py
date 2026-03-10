#!/usr/bin/env python3
"""
Lanzador de Demo para PFM Velmak
=================================

Script para iniciar la aplicación de demostración.

Autor: PFM Velmak Team
Fecha: Marzo 2026
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Instalar dependencias para la demo."""
    print("📦 Instalando dependencias para la demo...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements_demo.txt"
        ])
        print("✅ Dependencias instaladas exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def start_demo():
    """Iniciar la aplicación de demostración."""
    print("🚀 Iniciando aplicación de demostración...")
    print("📍 La aplicación se abrirá en tu navegador")
    print("🌐 URL: http://localhost:8501")
    print("⏹️  Presiona Ctrl+C para detener la aplicación")
    print("-" * 50)
    
    try:
        # Iniciar Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "demo_app.py", "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n⏹️  Aplicación detenida por el usuario")
    except Exception as e:
        print(f"❌ Error iniciando aplicación: {e}")

def main():
    """Función principal."""
    print("🏦 PFM Velmak - Demo Launcher")
    print("=" * 50)
    
    # Verificar si el archivo de demo existe
    demo_file = Path("demo_app.py")
    if not demo_file.exists():
        print("❌ No se encontró el archivo demo_app.py")
        return
    
    # Verificar si las dependencias están instaladas
    try:
        import streamlit
        import plotly
        print("✅ Dependencias ya instaladas")
    except ImportError:
        print("⚠️  Dependencias no encontradas, instalando...")
        if not install_requirements():
            print("❌ No se pudieron instalar las dependencias")
            return
    
    # Iniciar demo
    start_demo()

if __name__ == "__main__":
    main()
