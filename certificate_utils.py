from fpdf import FPDF
from datetime import datetime
import os

def generate_certificate(name, stats, output_path="certificate.pdf"):
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 20, "Certificate of Achievement", ln=True, align="C")

    # Subtitle
    pdf.set_font("Arial", "", 16)
    pdf.cell(0, 15, f"Presented to: {name}", ln=True, align="C")
    pdf.cell(0, 10, f"For successful completion of the AML Triage Simulation", ln=True, align="C")

    # Stats
    pdf.ln(20)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Date: {datetime.today().strftime('%Y-%m-%d')}", ln=True, align="C")
    pdf.cell(0, 10, f"Cases Handled: {stats.get('cases', 0)}", ln=True, align="C")
    pdf.cell(0, 10, f"Correct Decisions: {stats.get('correct', 0)}", ln=True, align="C")
    pdf.cell(0, 10, f"Missed Red Flags: {stats.get('missed', 0)}", ln=True, align="C")

    # Footer
    pdf.ln(20)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, "This certificate is auto-generated for training purposes only.", ln=True, align="C")

    # Save
    pdf.output(output_path)
    return output_path
