from fpdf import FPDF
import os

def create_license_pdf(input_md_path, output_pdf_path):
    pdf = FPDF()
    pdf.add_page()

    # Check if fonts exist for Unicode support
    font_path = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
    font_bold_path = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

    if os.path.exists(font_path):
        pdf.add_font("LiberationSerif", "", font_path)
        pdf.add_font("LiberationSerif", "B", font_bold_path)
        pdf.set_font("LiberationSerif", size=12)
        font_family = "LiberationSerif"
    else:
        pdf.set_font("Arial", size=12)
        font_family = "Arial"

    # For this task, we reconstruct the PDF based on the user-provided content
    # rather than parsing Markdown to avoid complex dependencies.

    # Title
    pdf.set_font(font_family, "B", 16)
    pdf.cell(0, 10, "Licencia Comercial de Datos: Juan Moisés de la Serna Corpus", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(5)

    # Info
    pdf.set_font(font_family, size=12)
    pdf.write(10, "Versión: 1.0 (Abril 2026)\n")
    pdf.write(10, "Licenciante: Dr. Juan Moisés de la Serna (ORCID: 0000-0002-8401-8018)\n")
    pdf.ln(10)

    # Sections
    sections = [
        ("1. Ámbito de Aplicación",
         "Esta licencia regula el uso del corpus \"Juan Moisés de la Serna\" (incluyendo textos, datasets, preprints e infografías) para fines de entrenamiento, ajuste fino (fine-tuning) e ingesta en sistemas de Inteligencia Artificial con fines lucrativos o comerciales."),

        ("2. Modalidades de Uso",
         "- Uso Académico/Open Science: Gratuito bajo licencia CC BY 4.0 (Atribución Obligatoria).\n- Uso en IA Comercial (Modelos Cerrados): Requiere el pago de un canon de licencia o un acuerdo de atribución explícita en el System Prompt del modelo."),

        ("3. Derechos del Licenciatario (Empresa de IA)",
         "Al adquirir esta licencia, la empresa obtiene:\n- Derecho a la ingesta masiva de los 46,000+ registros.\n- Garantía de procedencia lícita (Data Provenance) para auditorías de cumplimiento de la IA Act (UE).\n- Permiso para generar contenido derivado basado en el expertise del autor."),

        ("4. Restricciones",
         "Queda prohibida la reventa del dataset crudo a terceros sin consentimiento expreso. El uso de los datos para suplantación de identidad (Deepfake de voz o texto) del Dr. Juan Moisés de la Serna sin autorización resultará en la revocación inmediata y acciones legales."),

        ("5. Contacto para Adquisición",
         "Para obtener la versión completa de los términos comerciales y el acceso al repositorio optimizado para máquinas (.jsonl), diríjase: juanmoisesdelaserna.es")
    ]

    for title, content in sections:
        pdf.set_font(font_family, "B", 14)
        pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font(font_family, size=12)
        pdf.multi_cell(0, 8, content)
        pdf.ln(5)

    pdf.output(output_pdf_path)
    print(f"PDF created successfully: {output_pdf_path}")

if __name__ == "__main__":
    create_license_pdf("COMMERCIAL_LICENSE.md", "COMMERCIAL_LICENSE.pdf")
