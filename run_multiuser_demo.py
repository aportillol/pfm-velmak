#!/usr/bin/env python3
"""
Servidor Web Multiusuario para PFM Velmak Demo
==============================================

Permite que múltiples usuarios accedan a la demo simultáneamente.
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

class PFMHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def end_headers(self):
        # Add CORS headers to allow cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def start_server(port=8000):
    """Iniciar servidor web en el puerto especificado."""
    
    print("🌐 PFM Velmak - Servidor Multiusuario")
    print("=" * 50)
    print(f"📍 Iniciando servidor en puerto {port}")
    print(f"🔗 URL local: http://localhost:{port}")
    print(f"🌍 URL red: http://0.0.0.0:{port}")
    print("👥 Múltiples usuarios pueden conectarse simultáneamente")
    print("⏹️  Presiona Ctrl+C para detener el servidor")
    print("-" * 50)
    
    # Verify demo file exists
    demo_file = Path("demo_web.html")
    if not demo_file.exists():
        print(f"❌ Error: No se encuentra {demo_file}")
        return
    
    try:
        with socketserver.TCPServer(("", port), PFMHTTPRequestHandler) as httpd:
            print(f"✅ Servidor iniciado exitosamente")
            print(f"🚀 Abriendo navegador en http://localhost:{port}")
            
            # Open browser automatically
            webbrowser.open(f"http://localhost:{port}")
            
            # Start server
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n⏹️  Servidor detenido por el usuario")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Error: El puerto {port} ya está en uso")
            print(f"💡 Intenta con otro puerto: python run_multiuser_demo.py --port 8001")
        else:
            print(f"❌ Error iniciando servidor: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Servidor multiusuario para PFM Velmak Demo")
    parser.add_argument("--port", type=int, default=8000, help="Puerto del servidor (default: 8000)")
    args = parser.parse_args()
    
    start_server(args.port)
