#!/usr/bin/env python3
import markdown
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.frames import Frame
from reportlab.platypus.tableofcontents import TableOfContents
import re
from datetime import datetime

class AcademicDocTemplate(BaseDocTemplate):
    """Custom document template for academic papers with title page, TOC, and page numbers"""
    
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        
        # Create frame for normal pages
        frame = Frame(
            self.leftMargin, self.bottomMargin, 
            self.width, self.height, 
            id='normal'
        )
        
        # Template for title page (no page number)
        title_template = PageTemplate(
            id='title',
            frames=[frame],
            onPage=self.on_title_page
        )
        
        # Template for TOC page (with Roman numerals)
        toc_template = PageTemplate(
            id='toc',
            frames=[frame], 
            onPage=self.on_toc_page
        )
        
        # Template for content pages (with page numbers)
        content_template = PageTemplate(
            id='content', 
            frames=[frame],
            onPage=self.on_content_page
        )
        
        self.addPageTemplates([title_template, toc_template, content_template])
        self.toc_page_count = 0
    
    def on_title_page(self, canvas, doc):
        """Title page - no page number"""
        pass
    
    def on_toc_page(self, canvas, doc):
        """TOC pages - with Roman numerals"""
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        page_num = canvas.getPageNumber()
        # Roman numerals for TOC (starting from ii since title is i but not shown)
        roman_nums = ['', 'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
        if page_num > 1:
            roman = roman_nums[min(page_num - 1, len(roman_nums) - 1)]
            text_width = canvas.stringWidth(roman, 'Times-Roman', 10)
            x_position = (letter[0] - text_width) / 2
            canvas.drawString(x_position, 0.75*inch, roman)
        canvas.restoreState()
    
    def on_content_page(self, canvas, doc):
        """Content pages - with Arabic numbers"""
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        page_num = canvas.getPageNumber()
        # Calculate content page number (subtract title + TOC pages)
        content_page_num = page_num - 2 - self.toc_page_count
        if content_page_num > 0:
            text_width = canvas.stringWidth(str(content_page_num), 'Times-Roman', 10)
            x_position = (letter[0] - text_width) / 2
            canvas.drawString(x_position, 0.75*inch, str(content_page_num))
        canvas.restoreState()

def create_academic_pdf(qmd_file, pdf_file):
    """
    Create a PDF with academic formatting similar to research papers
    Mimics standard academic paper format: Times New Roman, 12pt, double-spaced, 1.25" margins
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
    course = None
    professor = None
    date = datetime.now().strftime("%B %d, %Y")

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
            elif line.startswith('course:'):
                course = line.split('course:')[1].strip().strip('"').strip("'")
            elif line.startswith('professor:'):
                professor = line.split('professor:')[1].strip().strip('"').strip("'")
            elif line.startswith('date:'):
                date = line.split('date:')[1].strip().strip('"').strip("'")
        else:
            markdown_content.append(line)

    # Convert markdown to HTML
    md_text = '\n'.join(markdown_content)
    html = markdown.markdown(md_text)
    
    # Create PDF with academic styling using custom template
    doc = AcademicDocTemplate(pdf_file, 
                            pagesize=letter,
                            rightMargin=1.25*inch, 
                            leftMargin=1.25*inch,
                            topMargin=1.25*inch, 
                            bottomMargin=1.25*inch)
    
    # Academic paper styles - Standard academic format
    styles = getSampleStyleSheet()
    
    # Title page styles
    title_page_title_style = ParagraphStyle(
        'TitlePageTitle',
        parent=styles['Title'],
        fontSize=16,
        spaceAfter=36,
        spaceBefore=0,
        alignment=1,  # Center
        fontName='Times-Bold',
        textColor=black,
        leading=20
    )
    
    title_page_author_style = ParagraphStyle(
        'TitlePageAuthor',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=24,
        spaceBefore=12,
        alignment=1,  # Center
        fontName='Times-Roman',
        textColor=black,
        leading=16
    )
    
    title_page_info_style = ParagraphStyle(
        'TitlePageInfo',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=18,
        spaceBefore=6,
        alignment=1,  # Center
        fontName='Times-Roman',
        textColor=black,
        leading=14
    )
    
    title_page_date_style = ParagraphStyle(
        'TitlePageDate',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=0,
        spaceBefore=36,
        alignment=1,  # Center
        fontName='Times-Roman',
        textColor=black,
        leading=14
    )
    
    
    # Table of Contents styles
    toc_title_style = ParagraphStyle(
        'TOCTitle',
        parent=styles['Title'],
        fontSize=14,
        spaceAfter=24,
        spaceBefore=0,
        alignment=1,  # Center
        fontName='Times-Bold',
        textColor=black,
        leading=16
    )
    
    toc_heading_style = ParagraphStyle(
        'TOCHeading',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=6,
        spaceBefore=6,
        alignment=0,  # Left
        fontName='Times-Roman',
        textColor=black,
        leading=14,
        leftIndent=0
    )
    
    # Content page styles
    # Title: centered, bold, 14pt (for content pages, smaller than title page)
    content_title_style = ParagraphStyle(
        'ContentTitle',
        parent=styles['Title'],
        fontSize=14,
        spaceAfter=18,
        spaceBefore=0,
        alignment=1,  # Center
        fontName='Times-Bold',
        textColor=black,
        leading=16
    )
    
    # Section headings: left-aligned, bold, 12pt
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
    
    # Body text: justified, 12pt, double-spaced, first-line indent
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
        firstLineIndent=0.5*inch  # Standard paragraph indent
    )
    
    # Parse content first to extract headings for TOC
    clean_text = re.sub('<[^<]+?>', '', html)
    sections = re.split(r'\n\s*\n\s*', clean_text.strip())
    
    # Extract headings for table of contents
    headings = []
    content_sections = []
    
    for i, section in enumerate(sections):
        section = section.strip()
        if section:
            if section.startswith('#'):
                heading_text = section.lstrip('# ').strip()
                if heading_text:
                    headings.append(heading_text)
                    content_sections.append(('heading', heading_text))
            else:
                sentences = section.replace('\n', ' ').strip()
                if sentences:
                    content_sections.append(('content', sentences))
    
    # Build story
    story = []
    
    # CREATE TITLE PAGE
    from reportlab.platypus import NextPageTemplate, PageBreak as PB
    
    # Use title page template
    story.append(NextPageTemplate('title'))
    
    # Add vertical space to center content on title page
    story.append(Spacer(1, 2*inch))
    
    # Add title page content
    story.append(Paragraph(title, title_page_title_style))
    story.append(Paragraph(f"by", title_page_info_style))
    story.append(Paragraph(author, title_page_author_style))
    
    if course:
        story.append(Paragraph(course, title_page_info_style))
    if professor:
        story.append(Paragraph(f"Professor {professor}", title_page_info_style))
    
    story.append(Paragraph(date, title_page_date_style))
    
    # CREATE TABLE OF CONTENTS
    story.append(PB())
    story.append(NextPageTemplate('toc'))
    
    # Add TOC title
    story.append(Paragraph("Table of Contents", toc_title_style))
    story.append(Spacer(1, 24))
    
    # Add TOC entries
    page_num = 1  # Content starts at page 1
    for heading in headings:
        toc_entry = f"{heading} {'.' * (60 - len(heading))} {page_num}"
        story.append(Paragraph(toc_entry, toc_heading_style))
        page_num += 1  # Estimate pages (simple approximation)
    
    # Page break and switch to content template
    story.append(PB())
    story.append(NextPageTemplate('content'))
    
    # Set TOC page count for proper page numbering
    doc.toc_page_count = 1  # Assume 1 page for TOC
    
    # Add content title (smaller, for content pages)
    story.append(Paragraph(title, content_title_style))
    
    # Add content sections
    for section_type, content in content_sections:
        if section_type == 'heading':
            # Add space before sections
            story.append(Spacer(1, 12))
            story.append(Paragraph(content, section_heading_style))
        else:
            # Handle regular paragraphs
            story.append(Paragraph(content, body_style))
            # Add spacing between paragraphs
            story.append(Spacer(1, 12))
    
    # Build PDF (with title page, TOC, and page numbering)
    doc.build(story)
    print(f"Academic PDF created: {pdf_file}")
    print(f"Format: Times New Roman, 12pt, double-spaced, 1.25\" margins")
    print(f"Features: Title page + Table of Contents + page numbers")
    
    # Try to open the PDF in VS Code
    import subprocess
    try:
        subprocess.run(['code', pdf_file], check=False)
        print(f"PDF opened in VS Code")
    except:
        print(f"PDF ready to open manually")

if __name__ == "__main__":
    create_academic_pdf('Abstract/Abstract.qmd', 'Abstract/Abstract_academic.pdf')
