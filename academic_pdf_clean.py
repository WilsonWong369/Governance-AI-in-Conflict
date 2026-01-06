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
        
        # Template for TOC page (with numerical page numbers)
        toc_template = PageTemplate(
            id='toc',
            frames=[frame], 
            onPage=self.on_numbered_page
        )
        
        # Template for content pages (with page numbers)
        content_template = PageTemplate(
            id='content', 
            frames=[frame],
            onPage=self.on_numbered_page
        )
        
        self.addPageTemplates([title_template, toc_template, content_template])
    
    def on_title_page(self, canvas, doc):
        """Title page - no page number"""
        pass
    
    def on_numbered_page(self, canvas, doc):
        """All pages with numerical page numbers starting from 2"""
        canvas.saveState()
        canvas.setFont('Times-Roman', 10)
        page_num = canvas.getPageNumber()
        
        # Start numbering from page 2 (TOC page = 2, first content page = 3, etc.)
        if page_num >= 2:
            text_width = canvas.stringWidth(str(page_num), 'Times-Roman', 10)
            x_position = (letter[0] - text_width) / 2
            canvas.drawString(x_position, 0.75*inch, str(page_num))
        canvas.restoreState()

def create_academic_pdf(qmd_file, pdf_file):
    """
    Create a PDF with academic formatting and manual table of contents
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

    # Process markdown content and extract headings
    md_text = '\n'.join(markdown_content)
    
    # Find all headings with their levels
    heading_pattern = r'^(#{1,3})\s+(.+)$'
    toc_entries = []
    
    for line in md_text.split('\n'):
        match = re.match(heading_pattern, line)
        if match:
            level = len(match.group(1))
            heading_text = match.group(2).strip()
            toc_entries.append({
                'level': level,
                'text': heading_text
            })
    
    # Create PDF with academic styling
    doc = AcademicDocTemplate(pdf_file, 
                            pagesize=letter,
                            rightMargin=1.25*inch, 
                            leftMargin=1.25*inch,
                            topMargin=1.25*inch, 
                            bottomMargin=1.25*inch)
    
    # Define academic paper styles
    styles = getSampleStyleSheet()
    
    # Title page styles
    title_page_title_style = ParagraphStyle(
        'TitlePageTitle',
        fontSize=16,
        spaceAfter=36,
        alignment=1,
        fontName='Times-Bold',
        leading=20
    )
    
    title_page_author_style = ParagraphStyle(
        'TitlePageAuthor',
        fontSize=14,
        spaceAfter=24,
        spaceBefore=12,
        alignment=1,
        fontName='Times-Roman',
        leading=16
    )
    
    title_page_info_style = ParagraphStyle(
        'TitlePageInfo',
        fontSize=12,
        spaceAfter=18,
        spaceBefore=6,
        alignment=1,
        fontName='Times-Roman',
        leading=14
    )
    
    title_page_date_style = ParagraphStyle(
        'TitlePageDate',
        fontSize=12,
        spaceAfter=0,
        spaceBefore=36,
        alignment=1,
        fontName='Times-Roman',
        leading=14
    )
    
    # TOC styles
    toc_title_style = ParagraphStyle(
        'TOCTitle',
        fontSize=14,
        spaceAfter=24,
        alignment=1,
        fontName='Times-Bold',
        leading=16
    )
    
    toc_entry_style = ParagraphStyle(
        'TOCEntry',
        fontSize=12,
        spaceAfter=8,
        alignment=0,
        fontName='Times-Roman',
        leading=16,
        leftIndent=0
    )
    
    toc_entry_indent_style = ParagraphStyle(
        'TOCEntryIndent',
        fontSize=12,
        spaceAfter=6,
        alignment=0,
        fontName='Times-Roman',
        leading=14,
        leftIndent=20
    )
    
    # Content styles
    section_heading_style = ParagraphStyle(
        'SectionHeading',
        fontSize=12,
        spaceAfter=6,
        spaceBefore=18,
        fontName='Times-Bold',
        alignment=0,
        leading=14
    )
    
    body_style = ParagraphStyle(
        'AcademicBody',
        fontSize=12,
        spaceAfter=0,
        spaceBefore=0,
        alignment=4,  # Justify
        fontName='Times-Roman',
        leading=24,   # Double spacing
        firstLineIndent=0.5*inch
    )
    
    # Build story
    story = []
    
    # TITLE PAGE
    from reportlab.platypus import NextPageTemplate, PageBreak as PB
    
    story.append(NextPageTemplate('title'))
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph(title, title_page_title_style))
    story.append(Paragraph("by", title_page_info_style))
    story.append(Paragraph(author, title_page_author_style))
    
    if course:
        story.append(Paragraph(course, title_page_info_style))
    if professor:
        story.append(Paragraph(professor, title_page_info_style))
    
    story.append(Paragraph(date, title_page_date_style))
    
    # TABLE OF CONTENTS (Manual creation)
    story.append(PB())
    story.append(NextPageTemplate('toc'))
    story.append(Paragraph("Table of Contents", toc_title_style))
    story.append(Spacer(1, 24))
    
    # Manually create TOC entries with estimated page numbers
    current_page = 3  # Content starts on page 3
    for entry in toc_entries:
        level = entry['level']
        text = entry['text']
        
        # Create dotted line effect
        dots = '.' * max(1, 60 - len(text) - len(str(current_page)) - (level-1)*4)
        
        if level == 1:
            toc_line = f"{text} {dots} {current_page}"
            story.append(Paragraph(toc_line, toc_entry_style))
            current_page += 1  # Each major section gets a new page
        else:
            toc_line = f"{'    ' * (level-1)}{text} {dots} {current_page}"
            story.append(Paragraph(toc_line, toc_entry_indent_style))
    
    # CONTENT PAGES
    story.append(PB())
    story.append(NextPageTemplate('content'))
    
    # Process and add content
    current_paragraph = []
    
    for line in md_text.split('\n'):
        line = line.strip()
        
        if not line:
            # Empty line - end current paragraph
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                story.append(Paragraph(para_text, body_style))
                story.append(Spacer(1, 12))
                current_paragraph = []
        elif line.startswith('#'):
            # Heading - end current paragraph and add heading
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                story.append(Paragraph(para_text, body_style))
                story.append(Spacer(1, 12))
                current_paragraph = []
            
            # Add heading
            heading_text = line.lstrip('#').strip()
            story.append(Paragraph(heading_text, section_heading_style))
        else:
            # Regular text line
            current_paragraph.append(line)
    
    # Add final paragraph if exists
    if current_paragraph:
        para_text = ' '.join(current_paragraph)
        story.append(Paragraph(para_text, body_style))
    
    # Build PDF
    doc.build(story)
    
    print(f"✅ Academic PDF created: {pdf_file}")
    print(f"📄 Features:")
    print(f"   • Title page (no page number)")
    print(f"   • Manual Table of Contents with page numbers")
    print(f"   • {len(toc_entries)} headings detected")
    print(f"   • Times New Roman, 12pt, double-spaced")
    print(f"   • 1.25\" margins, justified text")
    print(f"   • Numerical page numbering throughout")
    
    # Open in VS Code
    import subprocess
    try:
        subprocess.run(['code', pdf_file], check=False)
        print(f"🚀 PDF opened in VS Code")
    except:
        print(f"📁 PDF ready: {pdf_file}")

if __name__ == "__main__":
    create_academic_pdf('Abstract/Abstract.qmd', 'Abstract/Abstract_academic.pdf')