from weasyprint import HTML, CSS
from pathlib import Path
import subprocess
import os

class DocumentConverter:
    @staticmethod
    def html_to_pdf(html_path, pdf_path, css_path=None):
        """Convierte HTML a PDF usando WeasyPrint"""
        try:
            html = HTML(html_path)
            css = [CSS(css_path)] if css_path and os.path.exists(css_path) else []
            html.write_pdf(pdf_path, stylesheets=css)
            return True
        except Exception as e:
            print(f"Error en HTML a PDF: {str(e)}")
            return False

    @staticmethod
    def pdf_to_odt(pdf_path, odt_path):
        """Convierte PDF a ODT usando LibreOffice"""
        try:
            subprocess.run([
                'libreoffice',
                '--headless',
                '--convert-to',
                'odt',
                '--outdir',
                str(Path(odt_path).parent),
                pdf_path
            ], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error en PDF a ODT: {str(e)}")
            return False

# Ejemplo de uso:
if __name__ == "__main__":
    converter = DocumentConverter()
    converter.html_to_pdf("input.html", "output.pdf")
    converter.pdf_to_odt("output.pdf", "final.odt")