import pandas as pd
from io import BytesIO

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