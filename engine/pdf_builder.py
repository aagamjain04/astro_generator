from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import io
import os

def generate_pdf(user_data, chart_data, report_content):
    # Load HTML template
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), '..', 'templates')))
    template = env.get_template('report.html')

    # Render variables into the template
    html_out = template.render(
        user=user_data,
        ascendant=chart_data["ascendant"],
        report_content=report_content,     # <--- ADDED THIS LINE
        planet_texts=report_content["planet_texts"]
    )

    # Generate PDF in memory
    pdf_file = io.BytesIO()
    HTML(string=html_out).write_pdf(pdf_file)
    pdf_file.seek(0)

    return pdf_file