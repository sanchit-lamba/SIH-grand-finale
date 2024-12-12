import os
from PyPDF2 import PdfReader, PdfWriter

def remove_pages_and_save_preserving_structure(root_folder):
    # Define the root folder for saving modified files
    output_root = os.path.join(root_folder, "modified_pdfs")
    os.makedirs(output_root, exist_ok=True)

    for dirpath, dirnames, filenames in os.walk(root_folder):
        for file_name in filenames:
            if file_name.endswith('.pdf'):
                # Construct the full path for the current PDF
                input_path = os.path.join(dirpath, file_name)

                # Calculate the relative path from the root folder
                relative_path = os.path.relpath(dirpath, root_folder)

                # Create corresponding output folder
                output_dir = os.path.join(output_root, relative_path)
                os.makedirs(output_dir, exist_ok=True)

                # Process the PDF
                reader = PdfReader(input_path)
                writer = PdfWriter()

                for i in range(len(reader.pages)):
                    if i == 1  :  # Exclude page 1 (index 0) and page 3 (index 2)
                        writer.add_page(reader.pages[i])

                # Save the modified PDF in the output directory
                output_path = os.path.join(output_dir, file_name)
                with open(output_path, 'wb') as output_pdf:
                    writer.write(output_pdf)

                print(f"Processed: {input_path}, saved as: {output_path}")

# Example usage
root_folder = r"C:\Users\Sanchit\Desktop\pp"  # Replace with the path to your folder
remove_pages_and_save_preserving_structure(root_folder)
