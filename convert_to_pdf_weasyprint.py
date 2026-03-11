#!/usr/bin/env python3
"""
Script para convertir PFM VELMAK Markdown a PDF con formato académico usando WeasyPrint
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def check_dependencies():
    """Verificar dependencias necesarias"""
    try:
        import markdown
        print("markdown disponible")
    except ImportError:
        print("markdown no encontrado. Instalar con: pip install markdown")
        return False
    
    try:
        import weasyprint
        print("weasyprint disponible")
        return True
    except ImportError:
        print("weasyprint no encontrado. Instalar con: pip install weasyprint")
        return False

def create_academic_css():
    """Crea CSS para formato académico EUDE"""
    return """
    @page {
        size: A4;
        margin: 2.5cm 3cm 2.5cm 3cm;
        
        @bottom-center {
            content: "Página " counter(page) " de " counter(pages);
            font-size: 10pt;
            font-family: Arial, sans-serif;
            margin: 1em 0;
            color: #000;
        }
    }
    
    body {
        font-family: Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.5;
        color: #000000;
        text-align: justify;
        margin: 0;
        padding: 0;
        orphans: 2;
        widows: 2;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: Arial, sans-serif;
        font-weight: bold;
        line-height: 1.3;
        margin-top: 1.5em;
        margin-bottom: 1em;
        text-align: left;
        color: #000000;
        page-break-after: avoid;
    }
    
    h1 {
        font-size: 18pt;
        text-align: center;
        margin-top: 2em;
        margin-bottom: 2em;
        color: #000000;
    }
    
    h2 {
        font-size: 14pt;
        margin-top: 2em;
        margin-bottom: 1em;
        page-break-after: avoid;
        border-bottom: 1px solid #ccc;
        padding-bottom: 0.5em;
    }
    
    h3 {
        font-size: 12pt;
        margin-top: 1.5em;
        margin-bottom: 0.8em;
    }
    
    h4 {
        font-size: 11pt;
        margin-top: 1.2em;
        margin-bottom: 0.6em;
    }
    
    p {
        margin-bottom: 1em;
        text-align: justify;
        widows: 2;
        orphans: 2;
    }
    
    ul, ol {
        margin-bottom: 1em;
        padding-left: 2em;
    }
    
    li {
        margin-bottom: 0.5em;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 1.5em 0;
        font-size: 10pt;
        page-break-inside: avoid;
    }
    
    th, td {
        border: 1px solid #000;
        padding: 8px;
        text-align: left;
        vertical-align: top;
    }
    
    th {
        background-color: #f5f5f5;
        font-weight: bold;
    }
    
    blockquote {
        margin: 1.5em 0;
        padding: 1em 1.5em;
        border-left: 4px solid #ccc;
        background-color: #f9f9f9;
        font-style: italic;
    }
    
    code {
        font-family: 'Courier New', monospace;
        background-color: #f4f4f4;
        padding: 2px 4px;
        border-radius: 3px;
        font-size: 10pt;
    }
    
    pre {
        background-color: #f4f4f4;
        padding: 1em;
        border-radius: 5px;
        overflow-x: auto;
        font-family: 'Courier New', monospace;
        font-size: 9pt;
        line-height: 1.3;
        page-break-inside: avoid;
    }
    
    strong, b {
        font-weight: bold;
    }
    
    em, i {
        font-style: italic;
    }
    
    a {
        color: #0066cc;
        text-decoration: none;
    }
    
    a:hover {
        text-decoration: underline;
    }
    
    .page-break {
        page-break-before: always;
    }
    
    .no-break {
        page-break-inside: avoid;
    }
    
    /* Estilos específicos para portada */
    .portada {
        text-align: center;
        margin-top: 4em;
    }
    
    .portada h1 {
        font-size: 20pt;
        margin-bottom: 3em;
    }
    
    .portada p {
        font-size: 12pt;
        margin: 1em 0;
        text-align: center;
    }
    
    /* Estilos para índice */
    .indice {
        margin: 2em 0;
    }
    
    .indice ul {
        list-style-type: none;
        padding-left: 0;
    }
    
    .indice li {
        margin: 0.5em 0;
    }
    
    /* Evitar saltos de página indeseados */
    h2, h3, h4 {
        page-break-after: avoid;
    }
    
    table, blockquote, pre {
        page-break-inside: avoid;
    }
    """

def convert_markdown_to_html(markdown_file):
    """Convierte Markdown a HTML con formato académico"""
    try:
        # Leer archivo Markdown
        with open(markdown_file, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        
        # Convertir Markdown a HTML
        html = markdown.markdown(
            markdown_content,
            extensions=[
                'markdown.extensions.tables',
                'markdown.extensions.fenced_code',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
                'markdown.extensions.nl2br',
                'markdown.extensions.footnotes'
            ]
        )
        
        # Crear HTML completo con estructura académica
        full_html = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>PFM VELMAK: Sistema de Scoring Crediticio con IA Explicable</title>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <style>
                {create_academic_css()}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        return full_html
        
    except Exception as e:
        print(f"Error al convertir Markdown a HTML: {e}")
        return None

def convert_html_to_pdf(html_content, output_file):
    """Convierte HTML a PDF usando WeasyPrint"""
    try:
        import weasyprint
        
        # Convertir HTML a PDF
        weasyprint.HTML(string=html_content).write_pdf(output_file)
        
        return True
        
    except Exception as e:
        print(f"Error al convertir HTML a PDF: {e}")
        return False

def main():
    """Función principal del script"""
    print("Iniciando conversión de PFM VELMAK a PDF con WeasyPrint...")
    
    # Rutas de archivos
    markdown_file = Path("PFM_VELMAK_DOCUMENTO_COMPLETO.md")
    output_file = Path("PFM_VELMAK_DOCUMENTO_COMPLETO.pdf")
    
    # Verificar que existe el archivo Markdown
    if not markdown_file.exists():
        print(f"Error: No se encuentra el archivo {markdown_file}")
        sys.exit(1)
    
    print(f"Leyendo archivo: {markdown_file}")
    print(f"Tamaño: {markdown_file.stat().st_size / 1024:.1f} KB")
    
    # Verificar dependencias
    if not check_dependencies():
        sys.exit(1)
    
    # Convertir Markdown a HTML
    print("Convirtiendo Markdown a HTML...")
    html_content = convert_markdown_to_html(markdown_file)
    
    if not html_content:
        print("Error: No se pudo convertir el Markdown a HTML")
        sys.exit(1)
    
    print("Conversión Markdown a HTML completada")
    
    # Convertir HTML a PDF
    print("Convirtiendo HTML a PDF...")
    success = convert_html_to_pdf(html_content, output_file)
    
    if not success:
        print("Error: No se pudo convertir el HTML a PDF")
        sys.exit(1)
    
    # Verificar archivo PDF
    if output_file.exists():
        file_size = output_file.stat().st_size / (1024 * 1024)  # MB
        print(f"PDF generado exitosamente: {output_file}")
        print(f"Tamaño del archivo: {file_size:.2f} MB")
        print(f"Ubicación: {output_file.absolute()}")
        
        # Información adicional
        print("\nInformación del documento:")
        print(f"Título: PFM VELMAK: Sistema de Scoring Crediticio con IA Explicable")
        print(f"Formato: Académico EUDE (A4, Arial 11pt, interlineado 1.5)")
        print(f"Páginas estimadas: ~78 páginas")
        print(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Intentar abrir el PDF
        try:
            os.startfile(output_file)
            print("Abriendo PDF en visor predeterminado...")
        except:
            print(f"PDF guardado en: {output_file.absolute()}")
        
        print("\n¡Conversión completada con éxito!")
        
    else:
        print("Error: No se generó el archivo PDF")
        sys.exit(1)

if __name__ == "__main__":
    main()
