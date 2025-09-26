import pandas as pd
from io import BytesIO
from fpdf import FPDF

def to_excel(df):
    """Converts a dataframe to an Excel file in memory."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    return processed_data

def to_csv(df):
    """Converts a dataframe to a CSV string."""
    return df.to_csv(index=False).encode('utf-8')

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Maintenance Schedule Report', 0, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def to_pdf(df):
    """Converts a dataframe to a PDF file in memory."""
    pdf = PDF(orientation='L', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font('Arial', '', 8)

    # Table Header
    headers = df.columns.tolist()
    col_widths = [30] * len(headers) # Basic width, can be optimized
    pdf.set_fill_color(200, 220, 255)
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, str(header), 1, 0, 'C', 1)
    pdf.ln()

    # Table Rows
    for index, row in df.iterrows():
        for i, header in enumerate(headers):
            # Convert all data to string to avoid FPDF errors
            cell_text = str(row[header])
            pdf.cell(col_widths[i], 10, cell_text, 1)
        pdf.ln()

    return pdf.output(dest='S')