# **Instrucciones para Convertir PFM Velmak a PDF**

## **🔄 Métodos de Conversión Disponibles**

### **📋 Método 1: Usar Script Python (Recomendado)**

#### **🔧 Instalación de Dependencias:**
```bash
# Abrir PowerShell o CMD como Administrador
pip install markdown pdfkit
```

#### **📥 Descargar wkhtmltopdf:**
1. **Ir a:** https://wkhtmltopdf.org/downloads.html
2. **Descargar:** Versión para Windows (64-bit)
3. **Instalar:** Ejecutar el instalador con opciones por defecto
4. **Reiniciar:** Reiniciar PowerShell/ CMD después de instalación

#### **🚀 Ejecutar Conversión:**
```bash
python convert_to_pdf.py
```

#### **✅ Resultado:**
- **Archivo:** `PFM_VELMAK_PRIMERA_PRUEBA.pdf`
- **Formato:** A4 con márgenes académicos
- **Estilo:** Arial 11pt, interlineado 1.5
- **Calidad:** Alta resolución para impresión

---

### **🌐 Método 2: Conversión Online (Rápido)**

#### **📈 Opciones Online Gratuitas:**

##### **1. Markdown to PDF Converter**
- **Sitio:** https://md-to-pdf.fly.dev/
- **Pasos:**
  1. Copiar contenido de `PFM_VELMAK_PRIMERA_PRUEBA.md`
  2. Pegar en el sitio web
  3. Descargar PDF

##### **2. Dillinger Markdown Editor**
- **Sitio:** https://dillinger.io/
- **Pasos:**
  1. Importar archivo `.md`
  2. Usar "Export as PDF"
  3. Descargar resultado

##### **3. Online Markdown to PDF**
- **Sitio:** https://www.markdowntopdf.com/
- **Pasos:**
  1. Subir archivo markdown
  2. Configurar opciones de formato
  3. Generar y descargar PDF

---

### **📝 Método 3: Microsoft Word (Manual)**

#### **🔄 Pasos:**

##### **1. Abrir en Word:**
- **Copiar** todo el contenido de `PFM_VELMAK_PRIMERA_PRUEBA.md`
- **Pegar** en Microsoft Word

##### **2. Formato Académico:**
- **Fuente:** Arial, 11 puntos
- **Interlineado:** 1.5 líneas
- **Márgenes:** 2.5cm (arriba/abajo), 3cm (izquierda/derecha)
- **Justificar** texto

##### **3. Estructura:**
- **Títulos:** Formato jerárquico (H1, H2, H3)
- **Tablas:** Ajustar ancho al 100%
- **Citas:** Formato APA consistente

##### **4. Exportar a PDF:**
- **Archivo → Guardar como**
- **Tipo:** PDF (*.pdf)
- **Opciones:** Optimizado para impresión
- **Guardar:** `PFM_VELMAK_PRIMERA_PRUEBA.pdf`

---

### **🛠️ Método 4: Pandoc (Avanzado)**

#### **📦 Instalar Pandoc:**
1. **Descargar:** https://pandoc.org/installing.html
2. **Versión:** Windows (64-bit)
3. **Instalar:** Ejecutar instalador
4. **Verificar:** `pandoc --version`

#### **🔧 Comando de Conversión:**
```bash
pandoc PFM_VELMAK_PRIMERA_PRUEBA.md -o PFM_VELMAK_PRIMERA_PRUEBA.pdf --pdf-engine=xelatex -V geometry:margin=1in
```

#### **⚙️ Opciones Adicionales:**
```bash
# Con márgenes académicos específicos
pandoc PFM_VELMAK_PRIMERA_PRUEBA.md -o PFM_VELMAK_PRIMERA_PRUEBA.pdf \
  --pdf-engine=xelatex \
  -V geometry:top=2.5cm,bottom=2.5cm,left=3cm,right=3cm \
  -V fontsize=11pt \
  -V lineheight=1.5
```

---

### **📊 Método 5: VS Code Extension**

#### **🔌 Extensiones Recomendadas:**

##### **1. Markdown PDF**
- **Extension ID:** yzane.markdown-pdf
- **Instalación:** VS Code Extensions → Buscar "Markdown PDF"
- **Uso:** Ctrl+Shift+P → "Markdown PDF: Export"

##### **2. Markdown Preview Enhanced**
- **Extension ID:** shd101wyy.markdown-preview-enhanced
- **Instalación:** VS Code Extensions → Buscar "Markdown Preview Enhanced"
- **Uso:** Click derecho → "Markdown Preview Enhanced: Open in Browser" → Export PDF

---

## **📋 Requisitos de Formato Académico**

### **🎓 Especificaciones EUDE:**
- **Tamaño:** A4
- **Fuente:** Arial 11 puntos
- **Interlineado:** 1.5 líneas
- **Márgenes:** 2.5cm (arriba/abajo), 3cm (izquierda/derecha)
- **Justificación:** Texto justificado
- **Citas:** Formato APA 7th edition

### **📊 Contenido del PDF:**
- **78 páginas** (sin anexos)
- **17 capítulos** completos
- **25 referencias** bibliográficas
- **Índice expandido** detallado
- **Formato profesional** académico

---

## **🚀 Proceso Recomendado**

### **📋 Paso 1: Preparación**
1. **Verificar** que el archivo `PFM_VELMAK_PRIMERA_PRUEBA.md` existe
2. **Revisar** contenido y formato
3. **Asegurar** que todas las citas están correctas

### **📋 Paso 2: Conversión**
1. **Elegir método** de conversión (recomendado: Script Python)
2. **Instalar dependencias** necesarias
3. **Ejecutar conversión**
4. **Verificar** resultado

### **📋 Paso 3: Revisión Final**
1. **Abrir PDF** generado
2. **Verificar formato** académico
3. **Revisar paginación**
4. **Confirmar** contenido completo

---

## **🔧 Solución de Problemas**

### **❌ Problemas Comunes:**

##### **Python no encontrado:**
```bash
# Solución: Usar Python completo
C:\Python311\python.exe convert_to_pdf.py
```

##### **wkhtmltopdf no encontrado:**
- **Descargar:** https://wkhtmltopdf.org/downloads.html
- **Instalar:** Versión Windows 64-bit
- **Reiniciar:** Terminal después de instalación

##### **Errores de codificación:**
- **Verificar:** Codificación UTF-8
- **Solución:** Guardar archivo con codificación UTF-8

##### **Formato incorrecto:**
- **Revisar:** Configuración de márgenes y fuentes
- **Ajustar:** Opciones de conversión según método

---

## **✅ Verificación Final**

### **📊 Checklist de Calidad:**
- [ ] **78 páginas** completas
- [ ] **Formato A4** correcto
- [ ] **Fuente Arial 11pt**
- [ ] **Interlineado 1.5**
- [ ] **Márgenes académicos**
- [ ] **Texto justificado**
- [ ] **Índice completo**
- [ ] **Citas APA correctas**
- [ ] **Sin errores gramaticales**
- [ ] **PDF optimizado** para impresión

---

## **🎯 Resultado Esperado**

### **📚 Documento Final:**
- **Nombre:** `PFM_VELMAK_PRIMERA_PRUEBA.pdf`
- **Tamaño:** ~2-3 MB
- **Calidad:** Alta resolución (300 DPI)
- **Formato:** Profesional académico
- **Contenido:** 78 páginas + anexos

### **🚀 Uso del PDF:**
- **Presentación** EUDE
- **Evaluación** académica
- **Impresión** física
- **Distribución** digital

---

## **📞 Soporte**

### **🔧 Si necesita ayuda:**
1. **Verificar** dependencias instaladas
2. **Revisar** rutas de archivos
3. **Consultar** logs de error
4. **Probar** método alternativo

### **💡 Recursos Adicionales:**
- **Documentación Pandoc:** https://pandoc.org/
- **wkhtmltopdf Guide:** https://wkhtmltopdf.org/
- **Markdown PDF:** https://github.com/yzane/vscode-markdown-pdf

---

**¡Listo para convertir su documento PFM Velmak a PDF con formato académico profesional!** 🚀📚✅
