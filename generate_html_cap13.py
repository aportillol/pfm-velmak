import markdown
import os

def generate_html_cap13():
    """Genera HTML a partir del Markdown del Capítulo 13"""
    
    # Archivos
    md_file = 'CAPITULO_13_PLAN_FINANCIERO.md'
    html_file = 'CAPITULO_13_PLAN_FINANCIERO.html'
    
    try:
        # Leer Markdown
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        print(f'✅ Archivo Markdown leído: {md_file}')
        
        # Convertir a HTML
        html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'codehilite'])
        print('✅ Markdown convertido a HTML')
        
        # Estilos CSS
        css_styles = '''
<style>
body {
    font-family: 'Times New Roman', Times, serif;
    font-size: 12pt;
    line-height: 1.6;
    color: #000000;
    text-align: justify;
    margin: 40px;
    max-width: 800px;
    margin: 0 auto;
    padding: 40px;
}

h1 {
    font-size: 18pt;
    font-weight: bold;
    color: #000000;
    text-align: center;
    margin-bottom: 20pt;
    border-bottom: 2px solid #000000;
    padding-bottom: 10pt;
}

h2 {
    font-size: 16pt;
    font-weight: bold;
    color: #000000;
    margin-top: 24pt;
    margin-bottom: 12pt;
    border-bottom: 1px solid #cccccc;
    padding-bottom: 6pt;
}

h3 {
    font-size: 14pt;
    font-weight: bold;
    color: #000000;
    margin-top: 18pt;
    margin-bottom: 10pt;
}

p {
    margin-bottom: 12pt;
    text-align: justify;
    line-height: 1.6;
}

code {
    font-family: 'Courier New', monospace;
    background-color: #f5f5f5;
    padding: 2px 4px;
    border-radius: 3px;
    font-size: 11pt;
}

pre {
    font-family: 'Courier New', monospace;
    background-color: #f5f5f5;
    padding: 12pt;
    border-radius: 5px;
    border-left: 4px solid #cccccc;
    margin: 12pt 0;
    font-size: 10pt;
    white-space: pre-wrap;
    word-wrap: break-word;
    overflow-x: auto;
}

strong, b {
    font-weight: bold;
}

em, i {
    font-style: italic;
}

ul, ol {
    margin-left: 20pt;
    margin-bottom: 12pt;
}

li {
    margin-bottom: 6pt;
}

blockquote {
    margin: 12pt 20pt;
    padding-left: 12pt;
    border-left: 3px solid #cccccc;
    font-style: italic;
}

table {
    border-collapse: collapse;
    width: 100%;
    margin: 12pt 0;
}

th, td {
    border: 1px solid #cccccc;
    padding: 8pt;
    text-align: left;
}

th {
    background-color: #f5f5f5;
    font-weight: bold;
}

a {
    color: #0066cc;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

.mermaid {
    text-align: center;
    margin: 20pt 0;
    background-color: #f9f9f9;
    padding: 15pt;
    border-radius: 5px;
    border: 1px solid #e0e0e0;
}

@media print {
    body {
        margin: 2.5cm 3cm;
        max-width: none;
        padding: 0;
    }
    
    h1 {
        page-break-after: always;
    }
    
    h2, h3, p, ul, ol, blockquote, pre {
        page-break-inside: avoid;
    }
    
    .mermaid {
        page-break-inside: avoid;
    }
}
</style>
'''
        
        # Crear HTML completo
        full_html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <title>Capítulo 13: Breve Plan Financiero</title>
    {css_styles}
</head>
<body>
{html_content}
</body>
</html>'''
        
        # Guardar HTML
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        print(f'✅ HTML generado: {html_file}')
        
        # Verificar tamaño
        file_size = os.path.getsize(html_file)
        print(f'📄 Tamaño: {file_size/1024:.1f} KB')
        
        print(f'\n🎉 ¡Listo! Abre {html_file} en tu navegador y usa Ctrl+P para guardar como PDF')
        print('\n📋 Pasos para PDF:')
        print('1. Abre el archivo HTML en Chrome/Firefox/Edge')
        print('2. Presiona Ctrl+P')
        print('3. Selecciona "Guardar como PDF"')
        print('4. Configura márgenes: 2.5cm superior/inferior, 3cm lados')
        print('5. Selecciona tamaño A4')
        print('6. Haz clic en "Guardar"')
        
        return True
        
    except Exception as e:
        print(f'❌ Error: {e}')
        return False

if __name__ == '__main__':
    generate_html_cap13()
