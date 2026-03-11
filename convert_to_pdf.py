"""
Script para convertir el documento PFM Velmak a PDF
Requiere: pip install markdown pdfkit wkhtmltopdf
"""

import os
import sys
from pathlib import Path

def check_dependencies():
    """Verificar dependencias necesarias"""
    try:
        import markdown
        print("✅ markdown disponible")
    except ImportError:
        print("❌ markdown no encontrado. Instalar con: pip install markdown")
        return False
    
    try:
        import pdfkit
        print("✅ pdfkit disponible")
    except ImportError:
        print("❌ pdfkit no encontrado. Instalar con: pip install pdfkit")
        return False
    
    # Verificar wkhtmltopdf
    try:
        import subprocess
        result = subprocess.run(['wkhtmltopdf', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ wkhtmltopdf disponible")
            return True
        else:
            print("❌ wkhtmltopdf no encontrado. Descargar desde: https://wkhtmltopdf.org/")
            return False
    except FileNotFoundError:
        print("❌ wkhtmltopdf no encontrado. Descargar desde: https://wkhtmltopdf.org/")
        return False

def convert_markdown_to_pdf():
    """Convertir archivo markdown a PDF"""
    
    # Verificar dependencias
    if not check_dependencies():
        return False
    
    # Rutas de archivos
    md_file = Path("PFM_VELMAK_DOCUMENTO_COMPLETO.md")
    pdf_file = Path("PFM_VELMAK_DOCUMENTO_COMPLETO.pdf")
    
    if not md_file.exists():
        print(f"❌ Archivo no encontrado: {md_file}")
        return False
    
    try:
        import markdown
        import pdfkit
        
        # Leer archivo markdown
        print(f"📖 Leyendo archivo: {md_file}")
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convertir markdown a HTML
        print("🔄 Convirtiendo Markdown a HTML...")
        html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])
        
        # Agregar estilos CSS para formato académico
        css_styles = """
        <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            font-size: 11pt;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-top: 24px;
            margin-bottom: 16px;
        }
        h1 {
            font-size: 24pt;
            text-align: center;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            font-size: 18pt;
            border-bottom: 1px solid #3498db;
            padding-bottom: 5px;
        }
        h3 {
            font-size: 14pt;
        }
        p {
            margin-bottom: 12px;
            text-align: justify;
        }
        code {
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background-color: #f8f9fa;
            padding: 16px;
            border-radius: 5px;
            overflow-x: auto;
        }
        blockquote {
            border-left: 4px solid #3498db;
            margin-left: 0;
            padding-left: 16px;
            font-style: italic;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 16px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            font-weight: bold;
        }
        ul, ol {
            margin-left: 20px;
            margin-bottom: 12px;
        }
        li {
            margin-bottom: 4px;
        }
        .page-break {
            page-break-before: always;
        }
        </style>
        """
        
        # Crear HTML completo
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>PFM VELMAK - Proyecto Fin de Máster</title>
            {css_styles}
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Configuración de PDF
        options = {
            'page-size': 'A4',
            'margin-top': '2.5cm',
            'margin-right': '3cm',
            'margin-bottom': '2.5cm',
            'margin-left': '3cm',
            'encoding': 'UTF-8',
            'no-outline': None,
            'enable-local-file-access': None,
            'quiet': '',
            'javascript-delay': 1000,
        }
        
        # Convertir HTML a PDF
        print("🔄 Convirtiendo HTML a PDF...")
        pdfkit.from_string(full_html, str(pdf_file), options=options)
        
        print(f"✅ PDF generado exitosamente: {pdf_file}")
        print(f"📊 Tamaño del archivo: {pdf_file.stat().st_size / 1024:.1f} KB")
        
        # Intentar abrir el PDF
        try:
            os.startfile(pdf_file)
            print("📂 Abriendo PDF en visor predeterminado...")
        except:
            print(f"📂 PDF guardado en: {pdf_file.absolute()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la conversión: {e}")
        return False

def main():
    """Función principal"""
    print("🔄 Iniciando conversión de PFM Velmak a PDF")
    print("=" * 50)
    
    success = convert_markdown_to_pdf()
    
    if success:
        print("\n✅ Proceso completado exitosamente")
        print("📚 El documento PFM Velmak está disponible en formato PDF")
    else:
        print("\n❌ No se pudo completar la conversión")
        print("💡 Por favor, instale las dependencias necesarias:")
        print("   pip install markdown pdfkit")
        print("   Descargar wkhtmltopdf desde: https://wkhtmltopdf.org/")

if __name__ == "__main__":
    main()
