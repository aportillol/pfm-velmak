import markdown
import pdfkit
import os
from datetime import datetime

def convert_markdown_to_pdf():
    # Configuración de rutas
    input_file = "SECCION_1_RESUMEN_EJECUTIVO_PFM_VELMAK.md"
    output_file = "SECCION_1_RESUMEN_EJECUTIVO_PFM_VELMAK.pdf"
    
    # Leer el archivo Markdown
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        print(f"✅ Archivo {input_file} leído correctamente")
    except FileNotFoundError:
        print(f"❌ Error: No se encuentra el archivo {input_file}")
        return False
    
    # Convertir Markdown a HTML
    try:
        # Configuración de extensiones Markdown
        extensions = [
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.tables',
            'markdown.extensions.fenced_code'
        ]
        
        # Convertir a HTML
        html_content = markdown.markdown(md_content, extensions=extensions)
        
        # Crear HTML completo con estilos CSS
        full_html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SECCIÓN 1: RESUMEN EJECUTIVO - PFM VELMAK</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        body {{
            font-family: 'Inter', Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #072146;
            margin: 2.5cm;
            background: white;
        }}
        
        h1 {{
            font-size: 18pt;
            font-weight: 700;
            color: #004481;
            text-align: center;
            margin-bottom: 30pt;
            border-bottom: 2px solid #028484;
            padding-bottom: 10pt;
        }}
        
        h2 {{
            font-size: 14pt;
            font-weight: 600;
            color: #072146;
            margin-top: 24pt;
            margin-bottom: 16pt;
            border-left: 4px solid #004481;
            padding-left: 12pt;
        }}
        
        h3 {{
            font-size: 12pt;
            font-weight: 600;
            color: #004481;
            margin-top: 18pt;
            margin-bottom: 12pt;
        }}
        
        p {{
            margin-bottom: 12pt;
            text-align: justify;
        }}
        
        strong {{
            color: #004481;
            font-weight: 600;
        }}
        
        blockquote {{
            border-left: 4px solid #028484;
            margin: 16pt 0;
            padding: 12pt 20pt;
            background-color: #f8f9fa;
            font-style: italic;
        }}
        
        code {{
            background-color: #e9ecef;
            padding: 2pt 4pt;
            border-radius: 3pt;
            font-family: 'Courier New', monospace;
            font-size: 10pt;
        }}
        
        pre {{
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 4pt;
            padding: 16pt;
            overflow-x: auto;
            margin: 16pt 0;
        }}
        
        pre code {{
            background-color: transparent;
            padding: 0;
            border-radius: 0;
            font-size: 10pt;
        }}
        
        .mermaid {{
            text-align: center;
            margin: 20pt 0;
            padding: 16pt;
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 4pt;
        }}
        
        .page-break {{
            page-break-before: always;
        }}
        
        .header {{
            position: fixed;
            top: -20pt;
            left: 0;
            right: 0;
            text-align: center;
            font-size: 9pt;
            color: #666;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5pt;
        }}
        
        .footer {{
            position: fixed;
            bottom: -20pt;
            left: 0;
            right: 0;
            text-align: center;
            font-size: 9pt;
            color: #666;
            border-top: 1px solid #ddd;
            padding-top: 5pt;
        }}
        
        .content {{
            margin-top: 40pt;
            margin-bottom: 40pt;
        }}
        
        @media print {{
            .page-break {{ page-break-before: always; }}
            body {{ margin: 2.5cm; }}
            .header, .footer {{ display: none; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        PFM VELMAK - Proyecto Fin de Máster | EUDE Business School
    </div>
    
    <div class="content">
        {html_content}
    </div>
    
    <div class="footer">
        Generado el {datetime.now().strftime('%d/%m/%Y')} | Página <span class="page"></span> de <span class="topage"></span>
    </div>
</body>
</html>
        """
        
        print("✅ Markdown convertido a HTML con estilos")
        
    except Exception as e:
        print(f"❌ Error convirtiendo Markdown a HTML: {e}")
        return False
    
    # Configuración de opciones para PDF
    options = {
        'page-size': 'A4',
        'margin-top': '2.5cm',
        'margin-right': '3cm',
        'margin-bottom': '2.5cm',
        'margin-left': '3cm',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None,
        'javascript-delay': '1000',
        'load-error-handling': 'ignore',
        'load-media-error-handling': 'ignore',
        'disable-smart-shrinking': '',
        'zoom': '1.0',
        'dpi': '300',
        'encoding': 'UTF-8',
        'quiet': ''
    }
    
    # Convertir HTML a PDF
    try:
        print("🔄 Generando PDF...")
        pdfkit.from_string(full_html, output_file, options=options)
        print(f"✅ PDF generado exitosamente: {output_file}")
        
        # Verificar tamaño del archivo
        file_size = os.path.getsize(output_file)
        print(f"📊 Tamaño del archivo: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generando PDF: {e}")
        print("💡 Solución: Instalar wkhtmltopdf desde https://wkhtmltopdf.org/downloads.html")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando conversión de Resumen Ejecutivo a PDF")
    print("=" * 50)
    
    success = convert_markdown_to_pdf()
    
    print("=" * 50)
    if success:
        print("🎉 Proceso completado exitosamente")
        print("📄 Archivo generado: SECCION_1_RESUMEN_EJECUTIVO_PFM_VELMAK.pdf")
    else:
        print("❌ El proceso falló. Revisa los mensajes de error anteriores.")
