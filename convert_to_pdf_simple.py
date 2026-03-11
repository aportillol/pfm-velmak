#!/usr/bin/env python3
"""
Script simple para convertir PFM VELMAK Markdown a PDF usando ReportLab
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import markdown2
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def check_dependencies():
    """Verificar dependencias necesarias"""
    try:
        import markdown2
        print("markdown2 disponible")
    except ImportError:
        print("markdown2 no encontrado. Instalar con: pip install markdown2")
        return False
    
    try:
        import reportlab
        print("reportlab disponible")
        return True
    except ImportError:
        print("reportlab no encontrado. Instalar con: pip install reportlab")
        return False

def create_academic_styles():
    """Crea estilos académicos para el documento"""
    styles = getSampleStyleSheet()
    
    # Estilo para título principal
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        spaceBefore=50,
        alignment=TA_CENTER,
        textColor='black'
    )
    
    # Estilo para subtítulos
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=24,
        alignment=TA_LEFT,
        textColor='black'
    )
    
    # Estilo para sub-subtítulos
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=10,
        spaceBefore=18,
        alignment=TA_LEFT,
        textColor='black'
    )
    
    # Estilo para párrafos
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        leading=16  # Interlineado 1.5
    )
    
    return {
        'title': title_style,
        'heading2': heading2_style,
        'heading3': heading3_style,
        'body': body_style,
        'normal': styles['Normal']
    }

def parse_markdown_content(content):
    """Parsea el contenido markdown y lo convierte a elementos PDF"""
    lines = content.split('\n')
    elements = []
    styles = create_academic_styles()
    
    current_paragraph = []
    in_code_block = False
    code_content = []
    
    for line in lines:
        line = line.rstrip()
        
        # Manejar bloques de código
        if line.startswith('```'):
            if in_code_block:
                # Finalizar bloque de código
                if code_content:
                    code_text = '\n'.join(code_content)
                    elements.append(Paragraph(code_text, styles['normal']))
                    elements.append(Spacer(1, 12))
                code_content = []
                in_code_block = False
            else:
                # Iniciar bloque de código
                if current_paragraph:
                    para_text = ' '.join(current_paragraph)
                    if para_text.strip():
                        elements.append(Paragraph(para_text, styles['body']))
                    current_paragraph = []
                in_code_block = True
            continue
        
        if in_code_block:
            code_content.append(line)
            continue
        
        # Manejar encabezados
        if line.startswith('# '):
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                if para_text.strip():
                    elements.append(Paragraph(para_text, styles['body']))
                current_paragraph = []
            elements.append(Paragraph(line[2:], styles['title']))
            elements.append(Spacer(1, 12))
        elif line.startswith('## '):
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                if para_text.strip():
                    elements.append(Paragraph(para_text, styles['body']))
                current_paragraph = []
            elements.append(Paragraph(line[3:], styles['heading2']))
            elements.append(Spacer(1, 6))
        elif line.startswith('### '):
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                if para_text.strip():
                    elements.append(Paragraph(para_text, styles['body']))
                current_paragraph = []
            elements.append(Paragraph(line[4:], styles['heading3']))
            elements.append(Spacer(1, 4))
        # Manejar listas
        elif line.startswith(('- ') or ('* ')) and len(line) > 2:
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                if para_text.strip():
                    elements.append(Paragraph(para_text, styles['body']))
                current_paragraph = []
            elements.append(Paragraph(f"• {line[2:]}", styles['body']))
        # Manejar líneas en blanco
        elif not line.strip():
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                if para_text.strip():
                    elements.append(Paragraph(para_text, styles['body']))
                current_paragraph = []
                elements.append(Spacer(1, 6))
        else:
            # Agregar línea al párrafo actual
            current_paragraph.append(line)
    
    # Procesar último párrafo
    if current_paragraph:
        para_text = ' '.join(current_paragraph)
        if para_text.strip():
            elements.append(Paragraph(para_text, styles['body']))
    
    return elements

def convert_markdown_to_pdf():
    """Convierte archivo markdown a PDF"""
    
    # Verificar dependencias
    if not check_dependencies():
        return False
    
    # Rutas de archivos
    md_file = Path("PFM_VELMAK_DOCUMENTO_COMPLETO.md")
    pdf_file = Path("PFM_VELMAK_DOCUMENTO_COMPLETO.pdf")
    
    if not md_file.exists():
        print(f"Error: No se encuentra el archivo {md_file}")
        return False
    
    try:
        # Leer archivo markdown
        print(f"Leyendo archivo: {md_file}")
        print(f"Tamaño: {md_file.stat().st_size / 1024:.1f} KB")
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Crear documento PDF
        print("Creando documento PDF...")
        doc = SimpleDocTemplate(
            str(pdf_file),
            pagesize=A4,
            leftMargin=3*cm,
            rightMargin=3*cm,
            topMargin=2.5*cm,
            bottomMargin=2.5*cm
        )
        
        # Parsear contenido markdown
        print("Procesando contenido Markdown...")
        elements = parse_markdown_content(content)
        
        # Construir PDF
        print("Generando PDF...")
        doc.build(elements)
        
        print(f"PDF generado exitosamente: {pdf_file}")
        
        # Verificar archivo PDF
        if pdf_file.exists():
            file_size = pdf_file.stat().st_size / (1024 * 1024)  # MB
            print(f"Tamaño del archivo: {file_size:.2f} MB")
            print(f"Ubicación: {pdf_file.absolute()}")
            
            # Información adicional
            print("\nInformación del documento:")
            print("Título: PFM VELMAK: Sistema de Scoring Crediticio con IA Explicable")
            print("Formato: Académico EUDE (A4, fuente 11pt, interlineado 1.5)")
            print(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            
            # Intentar abrir el PDF
            try:
                os.startfile(pdf_file)
                print("Abriendo PDF en visor predeterminado...")
            except:
                print(f"PDF guardado en: {pdf_file.absolute()}")
            
            print("\n¡Conversión completada con éxito!")
            return True
        else:
            print("Error: No se generó el archivo PDF")
            return False
        
    except Exception as e:
        print(f"Error durante la conversión: {e}")
        return False

def main():
    """Función principal"""
    print("Iniciando conversión de PFM VELMAK a PDF (método simple)...")
    print("=" * 60)
    
    success = convert_markdown_to_pdf()
    
    if success:
        print("\nProceso completado exitosamente")
        print("El documento PFM VELMAK está disponible en formato PDF")
    else:
        print("\nNo se pudo completar la conversión")
        print("Por favor, verifique las dependencias y el archivo de entrada")

if __name__ == "__main__":
    main()
