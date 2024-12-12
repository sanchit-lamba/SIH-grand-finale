import os
import pandas as pd


def convert_xls_to_csv(input_dir, output_dir):
    """
    Convert all .xls files in the input directory and its subdirectories
    to .csv format, preserving the folder structure in the output directory.

    Args:
        input_dir (str): Path to the input directory containing .xls files.
        output_dir (str): Path to the output directory where .csv files will be saved.
    """
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".xls"):
                # Full path to the input .xls file
                xls_path = os.path.join(root, file)

                # Calculate the relative path to preserve the folder structure
                relative_path = os.path.relpath(root, input_dir)

                # Corresponding output directory
                csv_output_dir = os.path.join(output_dir, relative_path)

                # Ensure the output directory exists
                os.makedirs(csv_output_dir, exist_ok=True)

                # Output .csv file path
                csv_file_name = os.path.splitext(file)[0] + ".csv"
                csv_path = os.path.join(csv_output_dir, csv_file_name)

                # Read the .xls file and save it as .csv
                try:
                    data = pd.read_excel(xls_path)
                    data.to_csv(csv_path, index=False)
                    print(f"Converted: {xls_path} -> {csv_path}")
                except Exception as e:
                    print(f"Error converting {xls_path}: {e}")


# Specify input and output directories
input_directory = ""  # Replace with the path to the folder containing .xls files
output_directory = "path/to/output/folder"  # Replace with the path to the output folder

# Run the conversion
convert_xls_to_csv(input_directory, output_directory)
