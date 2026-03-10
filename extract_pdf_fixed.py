#!/usr/bin/env python3
"""
Extractor de PDFs para Guía PFM
================================

Script para extraer texto de PDFs problemáticos.

Autor: PFM Velmak Team
Fecha: Marzo 2026
"""

import os
import sys
from pathlib import Path

def try_extract_pdf_with_pdfplumber(pdf_path):
    """Intenta extraer texto usando pdfplumber."""
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text
    except ImportError:
        return None
    except Exception as e:
        print(f"Error con pdfplumber: {e}")
        return None

def try_extract_pdf_with_pypdf2(pdf_path):
    """Intenta extraer texto usando PyPDF2."""
    try:
        import PyPDF2
        text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        return text
    except ImportError:
        return None
    except Exception as e:
        print(f"Error con PyPDF2: {e}")
        return None

def try_extract_pdf_with_pymupdf(pdf_path):
    """Intenta extraer texto usando PyMuPDF."""
    try:
        import fitz
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        return text
    except ImportError:
        return None
    except Exception as e:
        print(f"Error con PyMuPDF: {e}")
        return None

def extract_pdf_text(pdf_path):
    """Intenta extraer texto usando múltiples métodos."""
    print(f"Extrayendo texto de: {pdf_path}")
    
    # Método 1: pdfplumber
    text = try_extract_pdf_with_pdfplumber(pdf_path)
    if text and len(text.strip()) > 100:
        print("Extraído con pdfplumber")
        return text
    
    # Método 2: PyPDF2
    text = try_extract_pdf_with_pypdf2(pdf_path)
    if text and len(text.strip()) > 100:
        print("Extraído con PyPDF2")
        return text
    
    # Método 3: PyMuPDF
    text = try_extract_pdf_with_pymupdf(pdf_path)
    if text and len(text.strip()) > 100:
        print("Extraído con PyMuPDF")
        return text
    
    print("No se pudo extraer texto con ningún método")
    return None

def main():
    """Función principal."""
    docs_dir = Path("docs")
    
    # Buscar PDFs
    pdf_files = list(docs_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("No se encontraron archivos PDF")
        return
    
    print(f"Encontrados {len(pdf_files)} PDFs:")
    for pdf in pdf_files:
        print(f"  {pdf.name}")
    
    print("\n" + "="*50)
    
    # Extraer texto de cada PDF
    for pdf_file in pdf_files:
        print(f"\nProcesando: {pdf_file.name}")
        
        text = extract_pdf_text(pdf_file)
        
        if text:
            # Guardar texto extraído
            output_file = pdf_file.with_suffix('.txt')
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"Texto guardado en: {output_file}")
                print(f"Longitud del texto: {len(text)} caracteres")
                
                # Mostrar primeras líneas
                lines = text.split('\n')[:10]
                print("Primeras líneas:")
                for i, line in enumerate(lines, 1):
                    if line.strip():
                        print(f"  {i}. {line.strip()}")
                
            except Exception as e:
                print(f"Error guardando texto: {e}")
        else:
            print(f"No se pudo extraer texto de {pdf_file.name}")
        
        print("-" * 50)

if __name__ == "__main__":
    main()
