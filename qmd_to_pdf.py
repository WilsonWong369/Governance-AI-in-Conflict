#!/usr/bin/env python3
import markdown
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import re

def qmd_to_pdf(qmd_file, pdf_file):
    # Read the qmd file
    with open(qmd_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract YAML frontmatter
    lines = content.split('\n')
    in_frontmatter = False
    markdown_content = []
    title = "Document"
    author = "Author"

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
                title = line.split('title:')[1].strip().strip('"')
            elif line.startswith('author:'):
                author = line.split('author:')[1].strip().strip('"')
        else:
            markdown_content.append(line)

    # Convert markdown to HTML
    md_text = '\n'.join(markdown_content)
    html = markdown.markdown(md_text)
    
    # Create PDF
    doc = SimpleDocTemplate(pdf_file, pagesize=letter,
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1,  # Center alignment
    )
    
    author_style = ParagraphStyle(
        'CustomAuthor',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=30,
        alignment=1,  # Center alignment
        fontName='Helvetica-Oblique'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=12,
        alignment=4,  # Justify
        leading=14
    )
    
    # Build story
    story = []
    
    # Add title and author
    story.append(Paragraph(title, title_style))
    story.append(Paragraph(f"by {author}", author_style))
    story.append(Spacer(1, 20))
    
    # Parse HTML and add content
    # Remove HTML tags and convert to paragraphs
    clean_text = re.sub('<[^<]+?>', '', html)
    
    # Split into sections based on headings
    sections = re.split(r'\n\n+', clean_text.strip())
    
    for section in sections:
        section = section.strip()
        if section:
            if section.startswith('#'):
                # It's a heading
                heading_text = section.lstrip('# ').strip()
                story.append(Paragraph(heading_text, heading_style))
            else:
                # It's body text
                # Split into paragraphs
                paragraphs = section.split('\n\n')
                for para in paragraphs:
                    if para.strip():
                        story.append(Paragraph(para.strip(), body_style))
                        story.append(Spacer(1, 6))
    
    # Build PDF
    doc.build(story)
    print(f"PDF created successfully: {pdf_file}")
    
    # Try to open the PDF in VS Code
    import subprocess
    try:
        subprocess.run(['code', pdf_file], check=False)
        print(f"PDF opened in VS Code: {pdf_file}")
    except:
        print(f"PDF created at: {pdf_file} (open manually)")

if __name__ == "__main__":
    qmd_to_pdf('Abstract/Abstract.qmd', 'Abstract/Abstract.pdf')
