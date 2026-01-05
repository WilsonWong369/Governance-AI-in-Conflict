# Quick Start Guide for LaTeX PDF Rendering

## Setup Instructions

### 1. Install Prerequisites

Before you begin, ensure you have:

#### LaTeX Distribution
- **Windows**: Download and install [MiKTeX](https://miktex.org/download) or [TeX Live](https://www.tug.org/texlive/windows.html)
- **macOS**: Download and install [MacTeX](https://www.tug.org/mactex/mactex-download.html) (3+ GB)
- **Linux Ubuntu/Debian**: 
  ```bash
  sudo apt-get update
  sudo apt-get install texlive-full
  ```
- **Linux Fedora/RHEL**:
  ```bash
  sudo dnf install texlive-scheme-full
  ```

#### Visual Studio Code
- Download from [https://code.visualstudio.com/](https://code.visualstudio.com/)

### 2. Open the Project in VSCode

```bash
cd Governance-AI-in-Conflict
code .
```

### 3. Install LaTeX Workshop Extension

When you open the project, VSCode will show a notification:
- Click **"Install"** on the "Recommended Extensions" notification
- Or manually install: Press `Ctrl+Shift+X` (Windows/Linux) or `Cmd+Shift+X` (macOS), search for "LaTeX Workshop", and install

### 4. Start Editing

1. Open `main.tex` in VSCode
2. Make any edit (e.g., change the author name)
3. Save the file (`Ctrl+S` or `Cmd+S`)
4. Watch the automatic compilation happen in the Output panel
5. PDF will open automatically in a VSCode tab

## How It Works

### Automatic Compilation
- **Trigger**: Every time you save a `.tex` file
- **Process**: 
  1. Runs `pdflatex` to compile the document
  2. Runs `bibtex` to process citations
  3. Runs `pdflatex` twice more to resolve references
- **Output**: PDF opens in a VSCode tab next to your editor

### File Structure
```
main.tex          → Your LaTeX document
reference.bib     → Bibliography database
main.pdf          → Generated PDF (auto-created)
```

## Common Tasks

### Adding a Citation

1. **Add to bibliography** (`reference.bib`):
   ```bibtex
   @article{mycitation2024,
       author = {Doe, John},
       title = {My Research Paper},
       journal = {Journal Name},
       year = {2024}
   }
   ```

2. **Cite in document** (`main.tex`):
   ```latex
   According to recent research \cite{mycitation2024}, ...
   ```

3. **Save** and watch it compile automatically

### Viewing the PDF

The PDF automatically opens in VSCode. You can:
- Click in the PDF to jump to that location in the source
- Click in the source to jump to that location in the PDF (SyncTeX)
- Zoom in/out using the PDF viewer controls

### Manual Compilation

If auto-compile is disabled, you can manually compile:
- Press `Ctrl+Alt+B` (Windows/Linux) or `Cmd+Option+B` (macOS)
- Or right-click in the editor → "Build LaTeX project"

### Cleaning Build Artifacts

The setup automatically cleans auxiliary files after each build. To manually clean:
- Press `Ctrl+Alt+C` (Windows/Linux) or `Cmd+Option+C` (macOS)
- Or right-click → "Clean up auxiliary files"

## Troubleshooting

### "LaTeX Workshop: Recipe terminated with error"

**Check the Output panel:**
1. View → Output
2. Select "LaTeX Workshop" from dropdown
3. Look for error messages

**Common causes:**
- Syntax error in LaTeX code
- Missing package (install with your LaTeX distribution's package manager)
- Bibliography errors (check citation keys match reference.bib)

### PDF Not Opening

1. Check if PDF was generated (look for `main.pdf`)
2. Try right-click → "View LaTeX PDF"
3. Change PDF viewer in settings (see below)

### Bibliography Not Showing

Make sure you:
1. Have `\cite{}` commands in your document
2. Have matching entries in `reference.bib`
3. Have `\bibliography{reference}` at the end of your document
4. Let the full build recipe run (pdflatex → bibtex → pdflatex × 2)

### Extension Not Loading

1. Reload VSCode: `Ctrl+Shift+P` → "Reload Window"
2. Check extension is installed: Extensions panel (`Ctrl+Shift+X`)
3. Reinstall LaTeX Workshop if needed

## Configuration Options

### Change PDF Viewer

Edit `.vscode/settings.json`:

```json
"latex-workshop.view.pdf.viewer": "tab"  // Default: tab in VSCode
"latex-workshop.view.pdf.viewer": "browser"  // External browser
"latex-workshop.view.pdf.viewer": "external"  // System PDF viewer
```

### Disable Auto-Build

Edit `.vscode/settings.json`:

```json
"latex-workshop.latex.autoBuild.run": "never"
```

Then build manually with `Ctrl+Alt+B`.

### Disable Auto-Clean

Edit `.vscode/settings.json`:

```json
"latex-workshop.latex.autoClean.run": "never"
```

## Tips

1. **Split Editor**: Drag the PDF tab to the side for side-by-side editing
2. **SyncTeX Navigation**: `Ctrl+Click` in PDF jumps to source, and vice versa
3. **Snippets**: Type `\` and press `Ctrl+Space` for LaTeX command suggestions
4. **Bibliography Tools**: Use [JabRef](https://www.jabref.org/) or [Zotero](https://www.zotero.org/) to manage references

## Next Steps

- Customize `main.tex` with your content
- Add more references to `reference.bib`
- Explore LaTeX packages for tables, figures, and more
- Check out [Overleaf Learn](https://www.overleaf.com/learn) for LaTeX tutorials

## Need Help?

- LaTeX Workshop documentation: [https://github.com/James-Yu/LaTeX-Workshop/wiki](https://github.com/James-Yu/LaTeX-Workshop/wiki)
- LaTeX Stack Exchange: [https://tex.stackexchange.com/](https://tex.stackexchange.com/)
- BibTeX documentation: [http://www.bibtex.org/](http://www.bibtex.org/)
