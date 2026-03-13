import markdown
import os
from datetime import datetime

def convert_seccion5_to_html():
    # Configuración de rutas
    input_file = "SECCION_5_PLAN_PRODUCCION_OPERACIONES_PFM_VELMAK.md"
    output_file = "SECCION_5_PLAN_PRODUCCION_OPERACIONES_PFM_VELMAK.html"
    
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
        
        # Crear HTML completo con estilos CSS para impresión
        full_html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SECCIÓN 5: PLAN DE PRODUCCIÓN Y OPERACIONES - PFM VELMAK</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        @page {{
            size: A4;
            margin: 2.5cm 3cm 2.5cm 3cm;
        }}
        
        @media print {{
            body {{
                font-family: 'Inter', Arial, sans-serif;
                font-size: 11pt;
                line-height: 1.5;
                color: #072146;
                margin: 0;
                background: white;
            }}
            
            .no-print {{
                display: none !important;
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
            
            h1, h2, h3, h4, h5, h6 {{
                page-break-after: avoid;
                page-break-inside: avoid;
            }}
            
            table, pre, blockquote {{
                page-break-inside: avoid;
            }}
        }}
        
        @media screen {{
            body {{
                font-family: 'Inter', Arial, sans-serif;
                font-size: 12pt;
                line-height: 1.6;
                color: #072146;
                margin: 20px;
                background: #f8f9fa;
            }}
            
            .container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            
            h1 {{
                font-size: 24pt;
                font-weight: 700;
                color: #004481;
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 2px solid #028484;
                padding-bottom: 15px;
            }}
            
            h2 {{
                font-size: 18pt;
                font-weight: 600;
                color: #072146;
                margin-top: 30px;
                margin-bottom: 20px;
                border-left: 4px solid #004481;
                padding-left: 15px;
            }}
            
            h3 {{
                font-size: 16pt;
                font-weight: 600;
                color: #004481;
                margin-top: 25px;
                margin-bottom: 15px;
            }}
            
            p {{
                margin-bottom: 15px;
                text-align: justify;
            }}
            
            strong {{
                color: #004481;
                font-weight: 600;
            }}
            
            blockquote {{
                border-left: 4px solid #028484;
                margin: 20px 0;
                padding: 15px 25px;
                background-color: #f8f9fa;
                font-style: italic;
                border-radius: 0 8px 8px 0;
            }}
            
            code {{
                background-color: #e9ecef;
                padding: 3px 6px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                font-size: 11pt;
            }}
            
            pre {{
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                overflow-x: auto;
                margin: 20px 0;
            }}
            
            pre code {{
                background-color: transparent;
                padding: 0;
                border-radius: 0;
                font-size: 11pt;
            }}
            
            .mermaid {{
                text-align: center;
                margin: 25px 0;
                padding: 20px;
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
            }}
            
            .print-button {{
                background: #004481;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
                cursor: pointer;
                margin: 20px 0;
                display: inline-block;
                text-decoration: none;
            }}
            
            .print-button:hover {{
                background: #028484;
            }}
            
            .header-info {{
                text-align: center;
                margin-bottom: 30px;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #dee2e6;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="no-print">
            <div class="header-info">
                <h3>⚙️ SECCIÓN 5: PLAN DE PRODUCCIÓN Y OPERACIONES</h3>
                <p><strong>PFM VELMAK - Proyecto Fin de Máster</strong><br>
                EUDE Business School | Máster Big Data & Business Analytics</p>
            </div>
        </div>
        
        {html_content}
        
        <div class="no-print">
            <button class="print-button" onclick="window.print()">🖨️ Imprimir como PDF</button>
            <p style="text-align: center; color: #666; font-size: 11px; margin-top: 20px;">
                <strong>Formato PFM:</strong> Arial 11, interlineado 1.5, márgenes 2.5cm/3cm<br>
                <strong>Para imprimir:</strong> Usar Ctrl+P o el botón above, seleccionar "Guardar como PDF"
            </p>
        </div>
    </div>
</body>
</html>
        """
        
        # Escribir archivo HTML
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        print(f"✅ HTML generado exitosamente: {output_file}")
        
        # Verificar tamaño del archivo
        file_size = os.path.getsize(output_file)
        print(f"📊 Tamaño del archivo: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
        return True, output_file
        
    except Exception as e:
        print(f"❌ Error generando HTML: {e}")
        return False, None

if __name__ == "__main__":
    print("🚀 Iniciando conversión de Sección 5 Producción y Operaciones a HTML (para PDF)")
    print("=" * 80)
    
    success, html_file = convert_seccion5_to_html()
    
    print("=" * 80)
    if success:
        print("🎉 Proceso completado exitosamente")
        print(f"📄 Archivo generado: {html_file}")
        print("🌐 Abre el archivo en tu navegador y usa 'Imprimir' → 'Guardar como PDF'")
        print("📋 Formato optimizado: A4, Arial 11, interlineado 1.5, márgenes 2.5cm/3cm")
        print("\n💡 Instrucciones para PDF:")
        print("1. Abre el archivo HTML en Chrome/Edge/Firefox")
        print("2. Presiona Ctrl+P o usa el botón 'Imprimir como PDF'")
        print("3. En 'Destino' selecciona 'Guardar como PDF'")
        print("4. Ajusta márgenes si es necesario y haz clic en 'Guardar'")
    else:
        print("❌ El proceso falló. Revisa los mensajes de error anteriores.")
