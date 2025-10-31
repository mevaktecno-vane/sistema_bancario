from fpdf import FPDF
from datetime import datetime

    # ---1. INICIALIZAR PDF---
    
pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'REPORTE FINANCIERO DEL CLIENTE', 0, 1, 'C')
pdf.ln(5)