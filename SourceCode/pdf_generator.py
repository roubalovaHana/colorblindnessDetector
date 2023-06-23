from jinja2 import Environment, FileSystemLoader, select_autoescape
from xhtml2pdf import pisa


def html_2_pdf(html_string: str, file_name: str):
    # open output file for writing (truncated binary)
    result_file = open(file_name, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
        html_string,  # the HTML to convert
        dest=result_file)  # file handle to receive result

    # close output file
    result_file.close()  # close output file

    # return False on success and True on errors
    return pisa_status.err


# https://jinja.palletsprojects.com/en/3.1.x/templates/
# https://xhtml2pdf.readthedocs.io/en/latest/usage.html
def generate(pdf_path, header, img_path, template_var_obj):
    jinja_env = Environment(
        loader=FileSystemLoader('./'),
        autoescape=select_autoescape()
    )
    template = jinja_env.get_template('report_template.j2')
    html_text = template.render(header=header, img_path=img_path, issue_obj=template_var_obj)
    pisa.showLogging()
    html_2_pdf(html_text, pdf_path)
