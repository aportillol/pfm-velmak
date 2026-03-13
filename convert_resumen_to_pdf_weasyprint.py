import markdown
import weasyprint
from weasyprint import HTML, CSS
import os
from datetime import datetime

def convert_markdown_to_pdf_weasyprint():
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
        
        # Crear HTML completo con estilos CSS para WeasyPrint
        full_html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SECCIÓN 1: RESUMEN EJECUTIVO - PFM VELMAK</title>
    <style>
        @page {{
            size: A4;
            margin: 2.5cm 3cm 2.5cm 3cm;
            @top-center {{
                content: "PFM VELMAK - Proyecto Fin de Máster | EUDE Business School";
                font-size: 9pt;
                color: #666;
                border-bottom: 1px solid #ddd;
                padding-bottom: 5pt;
            }}
            @bottom-center {{
                content: "Generado el {datetime.now().strftime('%d/%m/%Y')} - Página " counter(page) " de " counter(pages);
                font-size: 9pt;
                color: #666;
                border-top: 1px solid #ddd;
                padding-top: 5pt;
            }}
        }}
        
        body {{
            font-family: 'Inter', Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #072146;
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
            page-break-after: avoid;
        }}
        
        h2 {{
            font-size: 14pt;
            font-weight: 600;
            color: #072146;
            margin-top: 24pt;
            margin-bottom: 16pt;
            border-left: 4px solid #004481;
            padding-left: 12pt;
            page-break-after: avoid;
        }}
        
        h3 {{
            font-size: 12pt;
            font-weight: 600;
            color: #004481;
            margin-top: 18pt;
            margin-bottom: 12pt;
            page-break-after: avoid;
        }}
        
        p {{
            margin-bottom: 12pt;
            text-align: justify;
            orphans: 2;
            widows: 2;
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
            page-break-inside: avoid;
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
            page-break-inside: avoid;
        }}
        
        .page-break {{
            page-break-before: always;
        }}
        
        /* Estilos específicos para el mindmap */
        .mermaid pre {{
            background-color: transparent;
            border: none;
            padding: 0;
            margin: 0;
            text-align: center;
        }}
        
        /* Evitar cortes de línea indeseados */
        h1, h2, h3, h4, h5, h6 {{
            page-break-after: avoid;
            page-break-inside: avoid;
        }}
        
        table, pre, blockquote {{
            page-break-inside: avoid;
        }}
        
        /* Numeración de páginas */
        @page :first {{
            @top-center {{
                content: none;
            }}
            @bottom-center {{
                content: none;
            }}
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
        """
        
        print("✅ Markdown convertido a HTML con estilos WeasyPrint")
        
    except Exception as e:
        print(f"❌ Error convirtiendo Markdown a HTML: {e}")
        return False
    
    # Convertir HTML a PDF usando WeasyPrint
    try:
        print("🔄 Generando PDF con WeasyPrint...")
        
        # Crear objeto HTML
        html_doc = HTML(string=full_html)
        
        # Generar PDF
        html_doc.write_pdf(output_file)
        
        print(f"✅ PDF generado exitosamente: {output_file}")
        
        # Verificar tamaño del archivo
        file_size = os.path.getsize(output_file)
        print(f"📊 Tamaño del archivo: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generando PDF con WeasyPrint: {e}")
        print("💡 Solución: Instalar weasyprint con: pip install weasyprint")
        return False

if __name__ == "__main__":
    print("🚀 Iniciando conversión de Resumen Ejecutivo a PDF (WeasyPrint)")
    print("=" * 60)
    
    success = convert_markdown_to_pdf_weasyprint()
    
    print("=" * 60)
    if success:
        print("🎉 Proceso completado exitosamente")
        print("📄 Archivo generado: SECCION_1_RESUMEN_EJECUTIVO_PFM_VELMAK.pdf")
        print("📋 Formato: A4, márgenes 2.5cm/3cm, fuente Arial 11, interlineado 1.5")
    else:
        print("❌ El proceso falló. Revisa los mensajes de error anteriores.")
