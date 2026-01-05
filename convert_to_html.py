#!/usr/bin/env python3
import markdown

# Read the qmd file
with open('Abstract/Abstract.qmd', 'r') as f:
    content = f.read()

# Remove YAML frontmatter
lines = content.split('\n')
in_frontmatter = False
markdown_content = []

for line in lines:
    if line.strip() == '---':
        if not in_frontmatter:
            in_frontmatter = True
            continue
        else:
            in_frontmatter = False
            continue
    if not in_frontmatter:
        markdown_content.append(line)

# Convert markdown to HTML
md_text = '\n'.join(markdown_content)
html = markdown.markdown(md_text)

# Create a simple HTML file
html_template = f'''<!DOCTYPE html>
<html>
<head>
    <title>Abstract and Introduction - Wilson Wong</title>
    <style>
        body {{ 
            font-family: Georgia, serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 40px 20px; 
            line-height: 1.6; 
            color: #333;
        }}
        h1 {{ 
            color: #2c3e50; 
            border-bottom: 2px solid #eee; 
            padding-bottom: 10px; 
            margin-bottom: 20px;
        }}
        p {{ 
            text-align: justify; 
            margin-bottom: 20px; 
        }}
        .header {{ 
            background: #f8f9fa; 
            padding: 20px; 
            margin-bottom: 30px; 
            border-radius: 5px; 
            border-left: 4px solid #2c3e50;
        }}
        .author {{ 
            font-style: italic; 
            color: #666; 
            margin-bottom: 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Abstract and Introduction</h1>
        <p class="author"><strong>Author:</strong> Wilson Wong</p>
    </div>
    {html}
</body>
</html>'''

# Write HTML file
with open('Abstract/Abstract.html', 'w') as f:
    f.write(html_template)

print('HTML preview created successfully at Abstract/Abstract.html')
