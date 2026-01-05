#!/usr/bin/env python3
import markdown
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, darkblue
from reportlab.platypus.tableofcontents import TableOfContents
import re

class AcademicPageTemplate:
    """Custom page template for academic papers"""
    
    def __init__(self, canvas, doc):
        self.canvas = canvas
        self.doc = doc
        
    def draw_header_footer(self):
        """Draw header and footer on each page"""
        canvas = self.canvas
        
        # Page number at bottom center
        page_num = canvas.getPageNumber()
        canvas.setFont("Times-Roman", 10)
        canvas.drawCentredText(letter[0]/2, 0.75*inch, str(page_num))

def create_academic_pdf(qmd_file, pdf_file, style_preset="academic"):
    """
    Create a PDF with academic formatting similar to research papers
    """
    # Read the qmd file
    with open(qmd_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract YAML frontmatter
    lines = content.split('\n')
    in_frontmatter = False
    markdown_content = []
    title = "Document"
    author = "Author"
    bibliography = None

    for line in lines:
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                in_frontmatter = False
                continue
        if in_frontmatter:
            if line.startswith('title:'):
                title = line.split('title:')[1].strip().strip('"').strip("'")
            elif line.startswith('author:'):
                author = line.split('author:')[1].strip().strip('"').strip("'")
            elif line.startswith('bibliography:'):
                bibliography = line.split('bibliography:')[1].strip().strip('"').strip("'")
        else:
            markdown_content.append(line)

    # Convert markdown to HTML
    md_text = '\n'.join(markdown_content)
    html = markdown.markdown(md_text)
    
    # Create PDF with academic styling - typical research paper format
    doc = SimpleDocTemplate(pdf_file, 
                          pagesize=letter,
                          rightMargin=1.25*inch, 
                          leftMargin=1.25*inch,
                          topMargin=1.25*inch, 
                          bottomMargin=1.25*inch)
    
    # Custom page template for academic formatting
    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        page_num = canvas.getPageNumber()
        canvas.drawCentredText(letter[0]/2, 0.75*inch, str(page_num))
        canvas.restoreState()
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Academic paper styles - Times New Roman, proper academic spacing
    title_style = ParagraphStyle(
        'AcademicTitle',
        parent=styles['Title'],
        fontSize=14,
        spaceAfter=18,
        spaceBefore=0,
        alignment=1,  # Center
        fontName='Times-Bold',
        textColor=black,
        leading=16
    )
    
    author_style = ParagraphStyle(
        'AcademicAuthor',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=36,
        spaceBefore=12,
        alignment=1,  # Center
        fontName='Times-Roman',
        textColor=black,
        leading=14
    )
    
    section_heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading1'],
        fontSize=12,
        spaceAfter=6,
        spaceBefore=18,
        fontName='Times-Bold',
        textColor=black,
        alignment=0,  # Left
        leading=14
    )
    
    body_style = ParagraphStyle(
        'AcademicBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=0,
        spaceBefore=0,
        alignment=4,  # Justify
        fontName='Times-Roman',
        leading=24,  # Double spacing (12pt font * 2)
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0.5*inch  # Indent first line of paragraphs
    )
    
    # Style for paragraph spacing in academic format
    paragraph_spacer_style = ParagraphStyle(
        'ParagraphSpacer',
        parent=body_style,
        spaceAfter=12,
        spaceBefore=0
    )
    
    # Build story
    story = []
    
    # Add title
    story.append(Paragraph(title, title_style))
    
    # Add author
    story.append(Paragraph(author, author_style))
    
    # Parse content and add sections with proper academic formatting
    # Remove HTML tags but preserve structure
    clean_text = re.sub('<[^<]+?>', '', html)
    
    # Split content by double newlines to separate paragraphs
    sections = re.split(r'\n\s*\n\s*', clean_text.strip())
    
    for i, section in enumerate(sections):
        section = section.strip()
        if section:
            # Check if it's a heading (starts with # in markdown)
            if section.startswith('#'):
                heading_text = section.lstrip('# ').strip()
                if heading_text:
                    # Add some space before sections (except first one)
                    if i > 0:
                        story.append(Spacer(1, 12))
                    story.append(Paragraph(heading_text, section_heading_style))
            else:
                # Handle regular paragraphs - split by sentences for better formatting
                sentences = section.replace('\n', ' ').strip()
                if sentences:
                    # Create paragraph with proper academic spacing
                    para = Paragraph(sentences, body_style)
                    story.append(para)
                    # Add spacing between paragraphs
                    story.append(Spacer(1, 12))
    
    # Build PDF with page numbering
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"Academic PDF created successfully: {pdf_file}")
    print(f"Formatted with: Times New Roman, 12pt, double-spaced, 1.25\" margins")
    
    # Try to open the PDF in VS Code
    import subprocess
    try:
        subprocess.run(['code', pdf_file], check=False)
        print(f"PDF opened in VS Code: {pdf_file}")
    except:
        print(f"PDF created at: {pdf_file} (open manually)")

if __name__ == "__main__":
    create_academic_pdf('Abstract/Abstract.qmd', 'Abstract/Abstract_academic.pdf')
