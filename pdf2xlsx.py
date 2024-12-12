import os
import pandas as pd
import camelot


def convert_pdf_to_xlsx(pdf_path, output_xlsx_path):
    """
    Extract tables from a PDF and convert them to an .xlsx file.

    Args:
        pdf_path (str): Path to the PDF file.
        output_xlsx_path (str): Path to save the output .xlsx file.
    """
    try:
        # Extract tables using Camelot
        tables = camelot.read_pdf(pdf_path, pages="all",
                                  flavor="stream")  # Use 'stream' or 'lattice' based on the PDF structure

        # Create an Excel writer for .xlsx format
        with pd.ExcelWriter(output_xlsx_path, engine='openpyxl') as writer:
            for idx, table in enumerate(tables):
                # Convert table to DataFrame
                df = table.df
                # Save each table in a separate sheet
                sheet_name = f"Table_{idx + 1}"
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Converted: {pdf_path} -> {output_xlsx_path}")
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")


def process_directory(input_dir, output_root):
    """
    Recursively find all PDF files in a directory and convert them to .xlsx,
    saving them in a new folder while preserving the directory structure.

    Args:
        input_dir (str): Root directory containing PDF files.
        output_root (str): Root directory to save the converted .xlsx files.
    """
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".pdf"):
                # Full path to the input PDF file
                pdf_path = os.path.join(root, file)

                # Create the corresponding output directory
                relative_path = os.path.relpath(root, input_dir)
                output_dir = os.path.join(output_root, relative_path)
                os.makedirs(output_dir, exist_ok=True)

                # Full path for the output .xlsx file
                xlsx_filename = os.path.splitext(file)[0] + ".xlsx"
                output_xlsx_path = os.path.join(output_dir, xlsx_filename)

                # Convert PDF to Excel
                convert_pdf_to_xlsx(pdf_path, output_xlsx_path)


# Input and output directory paths
input_directory = r"testing"  # Replace with the input directory path
output_directory = os.path.join(input_directory, "Converted_XLSX")  # Output folder at the root of the input directory

# Process the directory
process_directory(input_directory, output_directory)