#!/usr/bin/env python3
import re
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

class AssignmentCanvas(canvas.Canvas):
    """Custom canvas for academic assignment formatting"""
    
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        num_pages = len(self._saved_page_states)
        for (page_num, page_state) in enumerate(self._saved_page_states):
            self.__dict__.update(page_state)
            
            # Add page numbers in top right corner (typical assignment style)
            if page_num > 0:  # Skip first page if it's title page
                self.setFont("Times-Roman", 12)
                self.drawRightString(letter[0] - 1*inch, letter[1] - 0.75*inch, str(page_num))
            
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

def create_assignment_style_pdf(qmd_file, pdf_file):
    """Create PDF matching typical academic assignment format"""
    
    # Read the qmd file
    with open(qmd_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract YAML frontmatter
    lines = content.split('\n')
    in_frontmatter = False
    markdown_content = []
    metadata = {}

    for line in lines:
        if line.strip() == '---':
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                in_frontmatter = False
                continue
        if in_frontmatter:
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip().strip('"').strip("'")
        else:
            markdown_content.append(line)

    # Extract metadata
    title = metadata.get('title', 'Document Title')
    author = metadata.get('author', 'Author Name')
    course = metadata.get('course', metadata.get('Course', ''))
    professor = metadata.get('professor', '')
    date = metadata.get('date', 'January 2026')

    # Create document with standard academic margins
    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=letter,
        leftMargin=1*inch,
        rightMargin=1*inch,
        topMargin=1*inch,
        bottomMargin=1*inch
    )

    # Define academic assignment styles
    styles = getSampleStyleSheet()
    
    # Header block style (top of first page)
    header_style = ParagraphStyle(
        'Header',
        fontName='Times-Roman',
        fontSize=12,
        alignment=0,  # Left aligned
        leading=14,
        spaceAfter=0,
        spaceBefore=0
    )
    
    # Title style (centered, after header)
    title_style = ParagraphStyle(
        'Title',
        fontName='Times-Roman',
        fontSize=12,
        alignment=1,  # Centered
        leading=14,
        spaceAfter=12,
        spaceBefore=24
    )
    
    # Heading style
    heading_style = ParagraphStyle(
        'Heading',
        fontName='Times-Bold',
        fontSize=12,
        alignment=1,  # Centered
        leading=14,
        spaceAfter=12,
        spaceBefore=24
    )
    
    # Body text style - double spaced
    body_style = ParagraphStyle(
        'Body',
        fontName='Times-Roman',
        fontSize=12,
        alignment=4,  # Justified
        leading=24,   # Double spacing
        spaceAfter=0,
        spaceBefore=0,
        firstLineIndent=0.5*inch
    )

    # Build content
    story = []
    
    # Header block (top left of first page)
    story.append(Paragraph(author, header_style))
    story.append(Paragraph(professor, header_style))
    story.append(Paragraph(course, header_style))
    story.append(Paragraph(date, header_style))
    
    # Title (centered)
    story.append(Paragraph(title, title_style))
    
    # Process markdown content
    md_text = '\n'.join(markdown_content)
    
    # Split content into sections and paragraphs
    current_paragraphs = []
    
    for line in md_text.split('\n'):
        line = line.strip()
        
        if not line:
            # Empty line - end current paragraph
            if current_paragraphs:
                paragraph_text = ' '.join(current_paragraphs)
                story.append(Paragraph(paragraph_text, body_style))
                current_paragraphs = []
        elif line.startswith('#'):
            # Heading - finish current paragraph and add heading
            if current_paragraphs:
                paragraph_text = ' '.join(current_paragraphs)
                story.append(Paragraph(paragraph_text, body_style))
                current_paragraphs = []
            
            # Add heading (centered and bold)
            heading_text = line.lstrip('#').strip()
            story.append(Paragraph(heading_text, heading_style))
        else:
            # Regular text line
            current_paragraphs.append(line)
    
    # Add final paragraph if exists
    if current_paragraphs:
        paragraph_text = ' '.join(current_paragraphs)
        story.append(Paragraph(paragraph_text, body_style))

    # Build PDF with custom canvas
    doc.build(story, canvasmaker=AssignmentCanvas)
    print(f"Assignment-style PDF created: {pdf_file}")
    
    # Open in VS Code
    try:
        os.system(f'code "{pdf_file}"')
        print("PDF opened in VS Code")
    except Exception as e:
        print(f"Could not auto-open PDF: {e}")

if __name__ == "__main__":
    qmd_file = "Abstract/Abstract.qmd"
    pdf_file = "Abstract/Abstract_assignment.pdf"
    
    if os.path.exists(qmd_file):
        create_assignment_style_pdf(qmd_file, pdf_file)
    else:
        print(f"File not found: {qmd_file}")
        print("Available files:")
        if os.path.exists("Abstract"):
            for f in os.listdir("Abstract"):
                print(f"  - Abstract/{f}")