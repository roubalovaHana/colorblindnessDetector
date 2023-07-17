import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from xhtml2pdf import pisa
from SourceCode.report_result_object import ReportResultObject


def get_unique_path(file_name):
    counter = 1
    base_name, extension = os.path.splitext(file_name)
    new_file_name = file_name

    while os.path.exists(new_file_name):
        new_file_name = f"{base_name}_{counter}{extension}"
        counter += 1

    return new_file_name

def html_2_pdf(html_string: str, file_name: str):
    """
    Converts html to pdf and saves it to a file_name file
    :param html_string: Html data to convert
    :param file_name: Target pdf file name
    :return: False on success and True on errors
    """
    if os.path.exists(file_name):
        file_name = get_unique_path(file_name)
    # open output file for writing (truncated binary)
    result_file = open(file_name, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
        html_string,  # the HTML to convert
        dest=result_file)  # file handle to receive result

    result_file.close()

    return pisa_status.err


# https://jinja.palletsprojects.com/en/3.1.x/templates/
# https://xhtml2pdf.readthedocs.io/en/latest/usage.html
def generate(pdf_path: str, header: str, img_path: str, template_var_obj: [ReportResultObject]):
    """
    Generates pdf report using the jinja report_template.j2 and saves it to pdf_path file
    :param pdf_path: Target pdf file name
    :param header: Header of the pdf file
    :param img_path: Path of image for the pdf file
    :param template_var_obj: Triggered warnings results of ReportResultObject type
    """
    jinja_env = Environment(
        loader=FileSystemLoader('./'),
        autoescape=select_autoescape()
    )
    template = jinja_env.get_template('report_template.j2')
    html_text = template.render(header=header, img_path=img_path, issue_obj=template_var_obj)
    pisa.showLogging()
    html_2_pdf(html_text, pdf_path)
