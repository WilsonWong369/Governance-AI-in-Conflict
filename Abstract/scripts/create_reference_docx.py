from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
import os

out = "/workspaces/Governance-AI-in-Conflict/Abstract/reference.docx"
if os.path.exists(out):
    print(f"Reference docx exists: {out}")
else:
    doc = Document()
    normal = doc.styles['Normal']
    normal.font.name = 'Arial'
    normal._element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing = 2
    doc.add_paragraph("Reference template for Quarto/Pandoc output. Normal style = Arial 12, double-spaced.")
    doc.save(out)
    print(f"Created: {out}")