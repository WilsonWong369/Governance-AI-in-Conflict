# Governance-AI-in-Conflict

A research repository for studying governance and artificial intelligence in conflict situations, with automated LaTeX PDF rendering in Visual Studio Code.

## Features

- **Bibliography Management**: Pre-configured `reference.bib` file with relevant research citations
- **Automated PDF Rendering**: VSCode settings for automatic PDF compilation on save
- **LaTeX Workshop Integration**: Recommended extensions and build recipes for seamless development

## Prerequisites

1. **LaTeX Distribution**: Install a LaTeX distribution on your system
   - **Windows**: [MiKTeX](https://miktex.org/) or [TeX Live](https://www.tug.org/texlive/)
   - **macOS**: [MacTeX](https://www.tug.org/mactex/)
   - **Linux**: TeX Live (usually available via package manager, e.g., `sudo apt-get install texlive-full`)

2. **Visual Studio Code**: Download from [code.visualstudio.com](https://code.visualstudio.com/)

3. **LaTeX Workshop Extension**: Install from VSCode marketplace or accept the recommendation when opening this project

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/WilsonWong369/Governance-AI-in-Conflict.git
   cd Governance-AI-in-Conflict
   ```

2. **Open in VSCode**
   ```bash
   code .
   ```

3. **Install recommended extensions**
   - VSCode will prompt you to install the LaTeX Workshop extension
   - Click "Install" to enable automatic PDF rendering

4. **Edit and compile**
   - Open `main.tex`
   - Make changes and save (Ctrl+S / Cmd+S)
   - The PDF will automatically compile and open in a new tab
   - View the rendered PDF in the VSCode tab

## File Structure

```
.
├── .vscode/
│   ├── settings.json      # LaTeX Workshop configuration
│   └── extensions.json    # Recommended extensions
├── reference.bib          # Bibliography database
├── main.tex              # Sample LaTeX document
├── .gitignore            # Excludes build artifacts
└── README.md             # This file
```

## Using the Bibliography

The `reference.bib` file contains sample citations related to AI governance and conflict. To cite a reference in your LaTeX document:

```latex
\cite{sample_ai_governance_2023}
```

### Adding New References

Edit `reference.bib` and add entries in BibTeX format:

```bibtex
@article{your_citation_key,
    author = {Last, First},
    title = {Article Title},
    journal = {Journal Name},
    year = {2024},
    volume = {1},
    pages = {1--10}
}
```

## VSCode Configuration

The repository includes pre-configured settings for optimal LaTeX development:

### Automatic Build
- **Trigger**: Saves automatically compile the document
- **Recipe**: Uses `pdflatex -> bibtex -> pdflatex*2` for proper bibliography integration

### PDF Viewer
- Opens in a VSCode tab for side-by-side editing
- Supports SyncTeX for bidirectional navigation between source and PDF

### Auto-Clean
- Automatically removes auxiliary files after successful compilation
- Keeps your workspace clean

## Manual Compilation

If you prefer to compile manually from the command line:

```bash
# Basic compilation
pdflatex main.tex

# With bibliography
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Customization

### Changing the Build Recipe

Edit `.vscode/settings.json` to modify the compilation workflow:

```json
"latex-workshop.latex.recipes": [
    {
        "name": "Your Custom Recipe",
        "tools": ["pdflatex", "bibtex", "pdflatex"]
    }
]
```

### PDF Viewer Options

Change the PDF viewer in `.vscode/settings.json`:
- `"tab"`: Opens in VSCode tab (default)
- `"browser"`: Opens in external browser
- `"external"`: Opens in system PDF viewer

## Troubleshooting

### PDF Not Generating
1. Ensure LaTeX distribution is installed correctly
2. Check the Output panel (View → Output → LaTeX Workshop) for error messages
3. Verify that `pdflatex` and `bibtex` are in your system PATH

### Bibliography Not Appearing
1. Ensure you've run the full build recipe (pdflatex → bibtex → pdflatex × 2)
2. Check that citation keys in `\cite{}` match entries in `reference.bib`
3. Verify the `\bibliography{reference}` line points to the correct file (without .bib extension)

### Extension Not Working
1. Reload VSCode window (Ctrl+Shift+P → "Reload Window")
2. Reinstall LaTeX Workshop extension
3. Check extension settings in `.vscode/settings.json`

## Contributing

Feel free to add more references to `reference.bib` or improve the LaTeX template. Follow standard BibTeX formatting for bibliography entries.

## License

This repository is available for academic and research purposes.