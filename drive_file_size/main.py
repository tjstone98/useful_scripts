import os
import pandas as pd
import datetime as dt

now = dt.datetime.now().strftime('%Y%m%d-%H%M')

drive_to_search_path = r'M:\BA DATA\US_2024'
files_output_path = fr'D:\tstone_temp\z_drive_file_size_files\Drive_Files_{now}.csv'
folders_output_path = fr'D:\tstone_temp\z_drive_file_size_files\Drive_Folders_{now}.csv'

def get_file_and_folder_sizes(drive_path):
    file_info = []
    folder_size = {}

    # Walk through the drive and get the sizes of all files
    for root, dirs, files in os.walk(drive_path):
        folder_total_size = 0  # To accumulate the total size of the folder
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_size = os.path.getsize(file_path)
                file_info.append((file_path, file_size))
                folder_total_size += file_size
            except OSError:
                # Handle the case where the file might not be accessible
                continue
        
        # Store the total size of the current folder
        folder_size[root] = folder_total_size

        # Add the size to all parent directories
        parent = root
        while parent != drive_path:
            parent = os.path.dirname(parent)
            if parent in folder_size:
                folder_size[parent] += folder_total_size
            else:
                folder_size[parent] = folder_total_size

    # Create DataFrames from the file and folder information
    file_info_df = pd.DataFrame(file_info, columns=['File Path', 'Size (bytes)'])
    folder_size_df = pd.DataFrame(list(folder_size.items()), columns=['Folder Path', 'Total Size (bytes)'])

    # Sort the DataFrames by size
    sorted_file_info_df = file_info_df.sort_values(by='Size (bytes)', ascending=False).reset_index(drop=True)
    sorted_folder_size_df = folder_size_df.sort_values(by='Total Size (bytes)', ascending=False).reset_index(drop=True)

    return sorted_file_info_df, sorted_folder_size_df

# Replace 'your/drive/path' with the actual path to the drive you want to scan
drive_path = drive_to_search_path
sorted_files_df, sorted_folders_df = get_file_and_folder_sizes(drive_path)

# Save the dataframes to CSV files
sorted_files_df.to_csv(files_output_path, index=False)
sorted_folders_df.to_csv(folders_output_path, index=False)
