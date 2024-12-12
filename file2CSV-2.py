import os
import pandas as pd
import PyPDF2


def extract_text_from_pdf(pdf_path):
    """
    Extracts all text from a PDF file.
    """
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text


def parse_text_to_structure(text):
    """
    Converts extracted text into a structured format based on the hardcoded Excel structure.
    """
    # Hardcoded column names derived from the provided Excel file
    column_names = [
        "Region", "States Met", "Demand Met during the day(MW)", "maximum Demand(MW)",
        "Energy Met (MU)", "Schedule (MU)", "OD(+)/UD(-) (MU)", "Max OD (MW)", "Energy Shortage (MU)"
    ]

    rows = text.split("\n")
    structured_data = []

    # Process rows to match the column structure
    for row in rows:
        split_row = row.split()  # Split the text by whitespace
        if len(split_row) == len(column_names):
            structured_data.append(split_row)

    # Convert to DataFrame with the hardcoded column names
    structured_df = pd.DataFrame(structured_data, columns=column_names)
    return structured_df


def convert_pdfs_to_csv(root_folder):
    """
    Recursively finds PDF files, extracts their data, and saves them as CSV files
    with a hardcoded column structure.
    """
    # Define the output root folder
    output_root = os.path.join(root_folder, "converted_csvs")
    os.makedirs(output_root, exist_ok=True)

    for dirpath, _, filenames in os.walk(root_folder):
        for file_name in filenames:
            if file_name.endswith('.pdf'):
                pdf_path = os.path.join(dirpath, file_name)
                text = extract_text_from_pdf(pdf_path)

                # Parse the text to match the hardcoded structure
                structured_df = parse_text_to_structure(text)

                # Create a CSV file in the output directory
                relative_path = os.path.relpath(dirpath, root_folder)
                output_dir = os.path.join(output_root, relative_path)
                os.makedirs(output_dir, exist_ok=True)

                csv_file_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.csv")
                structured_df.to_csv(csv_file_path, index=False)

                print(f"Converted {pdf_path} to {csv_file_path}")


# Example usage
root_folder = r"C:\Users\Sanchit\projects\SIH2\OG DATA\modified_pdfs"
convert_pdfs_to_csv(root_folder)
