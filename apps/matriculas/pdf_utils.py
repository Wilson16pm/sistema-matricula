from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib import colors
from io import BytesIO
from django.utils import timezone

def generar_ficha_matricula(matricula):
    # Usamos BytesIO para guardar el PDF en memoria antes de enviarlo al navegador
    buffer = BytesIO()
    
    # Creamos el lienzo (A4)
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --- ENCABEZADO ---
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width/2, height - 2*cm, "I.E. SECUNDARIA")
    
    p.setFont("Helvetica", 12)
    p.drawCentredString(width/2, height - 2.7*cm, "FICHA OFICIAL DE MATRÍCULA")
    
    p.setFont("Helvetica-Bold", 10)
    p.drawRightString(width - 2*cm, height - 3.5*cm, f"Año Académico: {matricula.anio.anio}")
    p.drawRightString(width - 2*cm, height - 4*cm, f"Código: {matricula.codigo}")

    # Línea divisoria
    p.setStrokeColor(colors.black)
    p.setLineWidth(1)
    p.line(2*cm, height - 4.5*cm, width - 2*cm, height - 4.5*cm)

    # --- DATOS DEL ESTUDIANTE ---
    y = height - 6*cm
    p.setFont("Helvetica-Bold", 12)
    p.drawString(2*cm, y, "1. DATOS DEL ESTUDIANTE")
    
    p.setFont("Helvetica", 11)
    y -= 0.8*cm
    p.drawString(2*cm, y, f"DNI: {matricula.estudiante.dni}")
    p.drawString(10*cm, y, f"Sexo: {matricula.estudiante.get_sexo_display()}")
    
    y -= 0.7*cm
    p.drawString(2*cm, y, f"Apellidos y Nombres: {matricula.estudiante.apellidos}, {matricula.estudiante.nombres}")
    
    y -= 0.7*cm
    p.drawString(2*cm, y, f"Fecha de Nacimiento: {matricula.estudiante.fecha_nacimiento.strftime('%d/%m/%Y')}")
    
    y -= 0.7*cm
    p.drawString(2*cm, y, f"Dirección: {matricula.estudiante.direccion or 'No registrada'}")

    # --- DATOS DEL APODERADO ---
    y -= 1.5*cm
    p.setFont("Helvetica-Bold", 12)
    p.drawString(2*cm, y, "2. DATOS DEL APODERADO")
    
    p.setFont("Helvetica", 11)
    y -= 0.8*cm
    p.drawString(2*cm, y, f"DNI: {matricula.apoderado.dni}")
    p.drawString(10*cm, y, f"Parentesco: {matricula.apoderado.parentesco}")
    
    y -= 0.7*cm
    p.drawString(2*cm, y, f"Apellidos y Nombres: {matricula.apoderado.apellidos}, {matricula.apoderado.nombres}")
    
    y -= 0.7*cm
    p.drawString(2*cm, y, f"Teléfono: {matricula.apoderado.telefono or 'No registrado'}")

    # --- DATOS DE LA MATRÍCULA ---
    y -= 1.5*cm
    p.setFont("Helvetica-Bold", 12)
    p.drawString(2*cm, y, "3. DETALLES DE LA MATRÍCULA")
    
    p.setFont("Helvetica", 11)
    y -= 0.8*cm
    p.drawString(2*cm, y, f"Grado: {matricula.grado_solicitado.nombre}")
    p.drawString(10*cm, y, f"Sección: {matricula.seccion}")
    
    y -= 0.7*cm
    p.drawString(2*cm, y, f"Estado: {matricula.estado.upper()}")
    p.drawString(10*cm, y, f"Fecha de Matrícula: {matricula.fecha_matricula.strftime('%d/%m/%Y') if matricula.fecha_matricula else 'Pendiente'}")

    # --- PIE DE PÁGINA ---
    p.setFont("Helvetica-Oblique", 9)
    p.drawCentredString(width/2, 3*cm, "Este documento es una constancia oficial de matrícula generada por el sistema.")
    p.drawCentredString(width/2, 2.5*cm, f"Generado el: {timezone.now().strftime('%d/%m/%Y %H:%M')}")

    # Firmas
    p.setFont("Helvetica", 10)
    p.line(3*cm, 5*cm, 8*cm, 5*cm)
    p.drawCentredString(5.5*cm, 4.5*cm, "Firma del Apoderado")
    
    p.line(12*cm, 5*cm, 17*cm, 5*cm)
    p.drawCentredString(14.5*cm, 4.5*cm, "Dirección / Sello")

    # Guardar y cerrar
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer