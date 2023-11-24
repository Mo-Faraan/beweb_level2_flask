from flask import Flask, render_template, request, make_response
from reportlab.pdfgen import canvas

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    # Retrieve form data
    client_name = request.form['client_name']
    items = request.form.getlist('item')
    quantities = request.form.getlist('quantity')
    prices = request.form.getlist('price')

    # Combine data into a list of tuples
    invoice_data = zip(items, quantities, prices)

    # Calculate total
    total = sum(int(qty) * float(price) for qty, price in zip(quantities, prices))

    # Render the invoice template with data
    rendered_html = render_template('invoice.html', client_name=client_name, invoice_data=invoice_data, total=total)

    # Create a PDF document
    response = make_response(pdf_from_html(rendered_html))
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=invoice.pdf'

    return response

def pdf_from_html(html):
    from io import BytesIO
    from xhtml2pdf import pisa

    pdf = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode('utf-8')), pdf)
    return pdf.getvalue()

if __name__ == '__main__':
    app.run(debug=True)
