import pandas as pd
import zipfile
import os

# Specific paths for the months you want to process in 2016
month_folders = [
    r"D:\5th Sem\SIH\Converted_XLSX\2016\May 2016",
    r"D:\5th Sem\SIH\Converted_XLSX\2016\April 2016",
    r"D:\5th Sem\SIH\Converted_XLSX\2016\August 2016",
    r"D:\5th Sem\SIH\Converted_XLSX\2016\December 2016",
    r"D:\5th Sem\SIH\Converted_XLSX\2016\February 2016",
    r"D:\5th Sem\SIH\Converted_XLSX\2016\January 2016",
    r"D:\5th Sem\SIH\Converted_XLSX\2016\July 2016",
    r"D:\5th Sem\SIH\Converted_XLSX\2016\June 2016",
    r"D:\5th Sem\SIH\Converted_XLSX\2016\March 2016"
]

# Output folder for trimmed files
output_folder = "output_trimmed_files_2016"
os.makedirs(output_folder, exist_ok=True)

trimmed_file_paths = []

# Loop through the specified month folders
for month_folder in month_folders:
    if os.path.exists(month_folder):
        print(f"Processing folder: {month_folder}")
        for root, dirs, files in os.walk(month_folder):
            for file in files:
                file_path = os.path.join(root, file)
                # Check if the file is an Excel file
                if file.lower().endswith(('.xls', '.xlsx')):
                    print(f"    Processing file: {file}")
                    try:
                        # Read the Excel file and check the first few rows
                        df = pd.read_excel(file_path, parse_dates=True)
                        
                        print(f"    First few rows of {file}:")
                        print(df.head())

                        # Check for the presence of "Punjab" and "Tripura" across all columns
                        start_index = df.apply(lambda row: row.astype(str).str.contains("Punjab", case=False).any(), axis=1).idxmax() if df.apply(lambda row: row.astype(str).str.contains("Punjab", case=False).any(), axis=1).any() else -1
                        end_index = df.apply(lambda row: row.astype(str).str.contains("Tripura", case=False).any(), axis=1).idxmax() if df.apply(lambda row: row.astype(str).str.contains("Tripura", case=False).any(), axis=1).any() else -1

                        # Debugging: Print if 'Punjab' and 'Tripura' are found
                        print(f"    Searching for 'Punjab' and 'Tripura'...")

                        if start_index != -1:
                            print(f"    'Punjab' found at row {start_index}")
                        else:
                            print(f"    'Punjab' not found in {file}")
                            
                        if end_index != -1:
                            print(f"    'Tripura' found at row {end_index}")
                        else:
                            print(f"    'Tripura' not found in {file}")

                        # Check if "Punjab" and "Tripura" were found
                        if start_index != -1 and end_index != -1 and start_index <= end_index:
                            # Trim the DataFrame between these rows
                            trimmed_df = df.iloc[start_index:end_index + 1]

                            # Create output folder for this month if it doesn't exist
                            month_name = os.path.basename(month_folder)
                            month_output_folder = os.path.join(output_folder, month_name)
                            os.makedirs(month_output_folder, exist_ok=True)

                            # Save trimmed data to CSV
                            trimmed_file_name = os.path.splitext(file)[0] + '_trimmed.csv'
                            trimmed_file_path = os.path.join(month_output_folder, trimmed_file_name)
                            trimmed_df.to_csv(trimmed_file_path, index=False)
                            trimmed_file_paths.append(trimmed_file_path)
                            print(f"    Trimmed file saved: {trimmed_file_path}")
                        else:
                            print(f"    No valid data found in {file} between 'Punjab' and 'Tripura'.")
                    except Exception as e:
                        print(f"    Error processing file {file}: {e}")

# Create a ZIP archive of all trimmed files
zip_file_path = os.path.join(output_folder, "Trimmed_Files_2016_Months.zip")
with zipfile.ZipFile(zip_file_path, 'w') as zipf:
    for file_path in trimmed_file_paths:
        zipf.write(file_path, os.path.relpath(file_path, output_folder))

print(f"Trimmed files saved and archived at: {zip_file_path}")
