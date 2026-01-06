#!/usr/bin/env python3
import markdown
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black, blue
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.platypus.frames import Frame
import re
import os

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        self.page_num = 0
        self.toc_pages = 0
        
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
        
    def save(self):
        num_pages = len(self._saved_page_states)
        for (page_num, page_state) in enumerate(self._saved_page_states):
            self.__dict__.update(page_state)
            if page_num == 0:  # Title page - no number
                pass
            elif page_num <= self.toc_pages:  # TOC pages - roman numerals
                self.draw_page_number_roman(page_num)
            else:  # Content pages - arabic numerals
                self.draw_page_number_arabic(page_num - self.toc_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
        
    def draw_page_number_roman(self, page_num):
        roman_nums = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']
        if page_num <= len(roman_nums):
            self.setFont("Times-Roman", 10)
            self.drawCentredText(letter[0]/2, 0.75*inch, roman_nums[page_num-1])
            
    def draw_page_number_arabic(self, page_num):
        self.setFont("Times-Roman", 10)
        self.drawCentredText(letter[0]/2, 0.75*inch, str(page_num))

class MyDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kw):
        self.allowSplitting = 0
        BaseDocTemplate.__init__(self, filename, **kw)
        
        # Title page template
        title_frame = Frame(1.25*inch, 1.25*inch, 6*inch, 9*inch, 
                           leftPadding=0, bottomPadding=0, 
                           rightPadding=0, topPadding=0, id='title')
        title_template = PageTemplate(id='title', frames=title_frame)
        
        # Normal page template
        normal_frame = Frame(1.25*inch, 1.25*inch, 6*inch, 9*inch, 
                            leftPadding=0, bottomPadding=0, 
                            rightPadding=0, topPadding=0, id='normal')
        normal_template = PageTemplate(id='normal', frames=normal_frame)
        
        self.addPageTemplates([title_template, normal_template])

class LinkedTOC(TableOfContents):
    def __init__(self):
        TableOfContents.__init__(self)
        self.levelStyles = [
            ParagraphStyle(name='TOCHeading1', fontName='Times-Roman', fontSize=12, 
                          leftIndent=0, leading=18),
            ParagraphStyle(name='TOCHeading2', fontName='Times-Roman', fontSize=11, 
                          leftIndent=20, leading=16),
            ParagraphStyle(name='TOCHeading3', fontName='Times-Roman', fontSize=10, 
                          leftIndent=40, leading=14),
        ]

def create_enhanced_academic_pdf(qmd_file, pdf_file):
    """
    Create a PDF with enhanced academic formatting, clickable TOC, and references
    """
    # Read the qmd file
    with open(qmd_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract YAML frontmatter and content
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

    # Extract title, author, etc.
    title = metadata.get('title', 'Document Title')
    author = metadata.get('author', 'Author Name')
    course = metadata.get('course', '')
    professor = metadata.get('professor', '')
    date = metadata.get('date', 'January 2026')
    bibliography = metadata.get('bibliography', '')

    # Process content and extract headings for TOC
    md_text = '\n'.join(markdown_content)
    headings = []
    toc_entries = []
    
    # Find all headings
    heading_pattern = r'^(#{1,3})\s+(.+)$'
    lines = md_text.split('\n')
    processed_lines = []
    
    for line_num, line in enumerate(lines):
        match = re.match(heading_pattern, line)
        if match:
            level = len(match.group(1))
            heading_text = match.group(2).strip()
            anchor_name = f"heading_{len(headings)}"
            
            headings.append({
                'level': level,
                'text': heading_text,
                'anchor': anchor_name,
                'line': line_num
            })
            
            # Replace heading with anchor
            processed_lines.append(f'<a name="{anchor_name}"></a>')
            processed_lines.append(line)
        else:
            processed_lines.append(line)
    
    # Convert markdown to HTML
    html = markdown.markdown('\n'.join(processed_lines))
    
    # Create the document
    doc = MyDocTemplate(pdf_file, pagesize=letter, 
                       leftMargin=1.25*inch, rightMargin=1.25*inch,
                       topMargin=1.25*inch, bottomMargin=1.25*inch)

    # Define styles
    styles = getSampleStyleSheet()
    
    # Title page styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontName='Times-Bold',
        fontSize=16,
        spaceAfter=24,
        alignment=1,  # Center
        leading=20
    )
    
    author_style = ParagraphStyle(
        'CustomAuthor', 
        fontName='Times-Roman',
        fontSize=14,
        spaceAfter=12,
        alignment=1,  # Center
        leading=18
    )
    
    info_style = ParagraphStyle(
        'CustomInfo',
        fontName='Times-Roman', 
        fontSize=12,
        spaceAfter=8,
        alignment=1,  # Center
        leading=16
    )
    
    # Content styles
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        fontName='Times-Bold',
        fontSize=12,
        spaceAfter=12,
        spaceBefore=24,
        alignment=0,  # Left
        leading=14
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        fontName='Times-Roman',
        fontSize=12,
        spaceAfter=0,
        spaceBefore=0,
        alignment=4,  # Justified
        leading=24,  # Double spaced
        firstLineIndent=0.5*inch,
        leftIndent=0,
        rightIndent=0
    )
    
    toc_title_style = ParagraphStyle(
        'TOCTitle',
        fontName='Times-Bold',
        fontSize=12,
        spaceAfter=24,
        spaceBefore=0,
        alignment=1,  # Center
        leading=14
    )

    # Build the story (content)
    story = []
    
    # Title page
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(f"by<br/>{author}", author_style))
    story.append(Spacer(1, 1*inch))
    
    if course:
        story.append(Paragraph(course, info_style))
    if professor:
        story.append(Paragraph(professor, info_style))
    story.append(Paragraph(date, info_style))
    
    story.append(PageBreak())
    
    # Table of Contents
    story.append(Paragraph("Table of Contents", toc_title_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Create linked TOC entries
    toc = LinkedTOC()
    story.append(toc)
    
    # Add TOC entries with links
    for i, heading in enumerate(headings):
        level = heading['level'] - 1  # Convert to 0-based
        text = heading['text']
        anchor = heading['anchor']
        
        # Create clickable link
        link_text = f'<a href="#{anchor}" color="blue">{text}</a>'
        dots = '.' * max(1, 50 - len(text) - level*2)
        
        toc_entry_style = ParagraphStyle(
            f'TOCEntry{level}',
            fontName='Times-Roman',
            fontSize=12,
            leftIndent=level * 20,
            leading=18,
            alignment=0
        )
        
        # Add entry to TOC with page reference placeholder
        toc.addEntry(level, text, i+1)  # Page numbers will be calculated
    
    story.append(PageBreak())
    
    # Set TOC pages count for numbering
    doc.canv = NumberedCanvas(pdf_file)
    doc.canv.toc_pages = 1  # Adjust based on TOC length
    
    # Content pages
    # Process the HTML content into reportlab elements
    content_parts = html.split('<h1>')
    
    for part in content_parts:
        if not part.strip():
            continue
            
        if '</h1>' in part:
            # This is a heading + content
            heading_part, content_part = part.split('</h1>', 1)
            
            # Add heading with anchor
            anchor_match = re.search(r'<a name="([^"]+)"></a>', content_part)
            if anchor_match:
                anchor_name = anchor_match.group(1)
                content_part = re.sub(r'<a name="[^"]+"></a>\s*', '', content_part)
            
            # Create heading paragraph with bookmark
            heading_para = Paragraph(f'<a name="{anchor_name if anchor_match else ""}">{heading_part}</a>', heading1_style)
            story.append(heading_para)
            
            # Process content paragraphs
            paragraphs = content_part.split('<p>')
            for para in paragraphs:
                if para.strip():
                    # Clean up HTML tags
                    clean_para = re.sub(r'</p>', '', para)
                    clean_para = re.sub(r'<[^>]+>', '', clean_para)
                    clean_para = clean_para.strip()
                    
                    if clean_para:
                        story.append(Paragraph(clean_para, body_style))
                        story.append(Spacer(1, 12))
        else:
            # This is just content
            paragraphs = part.split('<p>')
            for para in paragraphs:
                if para.strip():
                    clean_para = re.sub(r'</p>', '', para)
                    clean_para = re.sub(r'<[^>]+>', '', clean_para)
                    clean_para = clean_para.strip()
                    
                    if clean_para:
                        story.append(Paragraph(clean_para, body_style))
                        story.append(Spacer(1, 12))

    # Add references section if bibliography exists
    if bibliography:
        story.append(PageBreak())
        story.append(Paragraph("References", heading1_style))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Bibliography file: {bibliography}", body_style))

    # Build the PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    
    print(f"Enhanced academic PDF created: {pdf_file}")
    
    # Open the PDF
    try:
        os.system(f'code "{pdf_file}"')
        print("PDF opened in VS Code")
    except:
        print("Could not auto-open PDF")

if __name__ == "__main__":
    qmd_file = "Abstract/Abstract.qmd"
    pdf_file = "Abstract/Abstract_enhanced.pdf"
    create_enhanced_academic_pdf(qmd_file, pdf_file)