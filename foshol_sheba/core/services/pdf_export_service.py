import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle

def generate_diagnosis_pdf(result):
    """
    Generates a PDF report for a diagnostic result.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    story = []

    # Register Bengali Font (Nirmala UI supports Bengali)
    font_path = "C:\\Windows\\Fonts\\Nirmala.ttf"
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('Nirmala', font_path))
        font_name = 'Nirmala'
    else:
        font_name = 'Helvetica' # Fallback, though Bengali won't work

    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=24,
        textColor=colors.HexColor("#2e7d32"),
        spaceAfter=20,
        alignment=1 # Center
    )
    
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading2'],
        fontName=font_name,
        fontSize=18,
        textColor=colors.HexColor("#2e7d32"),
        spaceBefore=15,
        spaceAfter=10
    )
    
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=12,
        leading=16,
        spaceAfter=10
    )

    # Title
    story.append(Paragraph("ফসলসেবা - রোগ নির্ণয় রিপোর্ট", title_style))
    story.append(Spacer(1, 10))

    # Diagnostic Image
    if result.crop_image:
        img_path = result.crop_image.path
        if os.path.exists(img_path):
            img = Image(img_path, width=4*inch, height=3*inch)
            img.hAlign = 'CENTER'
            story.append(img)
            story.append(Spacer(1, 20))

    # Basic Info Table
    data = [
        ["ফসল:", result.detected_disease.crop.name_bn],
        ["শনাক্তকৃত রোগ:", result.detected_disease.name_bn],
        ["নির্ভুলতার হার:", f"{result.confidence_score}%"],
        ["তারিখ:", result.created_at.strftime("%d %B, %Y %I:%M %p")]
    ]
    
    table = Table(data, colWidths=[1.5*inch, 3.5*inch])
    table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), font_name),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('TEXTCOLOR', (0,0), (0,-1), colors.grey),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(table)
    story.append(Spacer(1, 20))

    # Details
    story.append(Paragraph("রোগের বিবরণ", header_style))
    story.append(Paragraph(result.detected_disease.description_bn or "তথ্য পাওয়া যায়নি।", normal_style))

    story.append(Paragraph("লক্ষণসমূহ", header_style))
    story.append(Paragraph(result.detected_disease.symptoms_bn or "তথ্য পাওয়া যায়নি।", normal_style))

    story.append(Paragraph("প্রতিরোধ ব্যবস্থা", header_style))
    story.append(Paragraph(result.detected_disease.preventative_measures_bn or "তথ্য পাওয়া যায়নি।", normal_style))

    story.append(Paragraph("প্রস্তাবিত প্রতিকার", header_style))
    story.append(Paragraph(f"<b>জৈব প্রতিকার:</b> {result.detected_disease.organic_remedy_bn or 'তথ্য পাওয়া যায়নি।'}", normal_style))
    story.append(Paragraph(f"<b>রাসায়নিক চিকিৎসা:</b> {result.detected_disease.chemical_treatment_bn or 'তথ্য পাওয়া যায়নি।'}", normal_style))

    # Build PDF
    doc.build(story)
    
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
