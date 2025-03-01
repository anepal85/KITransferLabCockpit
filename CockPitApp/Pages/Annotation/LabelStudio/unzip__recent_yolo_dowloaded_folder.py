import os
import zipfile

def unzip_newest_zip_file(folder_path, filename=None):
    """
    Finds the newest .zip file in the folder and unzips it with the same name inside the folder path.
    If a filename is provided, unzips only that file inside the folder path.
    """
    zip_files = []
    if filename is not None:
        # Extract the provided filename if it exists and is a .zip file
        if filename.endswith('.zip') and os.path.isfile(os.path.join(folder_path, filename)):
            folder_to_extract = os.path.join(folder_path, filename).split('.')[0]
            with zipfile.ZipFile(os.path.join(folder_path, filename), 'r') as zip_ref:
                zip_ref.extractall(folder_to_extract)
                return folder_to_extract
        else:
            print("Provided filename is not a .zip file or does not exist in the folder")
        return 

    # Get a list of all .zip files in the folder
    zip_files = [f for f in os.listdir(folder_path) if f.endswith('.zip')]

    # Sort the list of .zip files by creation time (newest first)
    zip_files = sorted(zip_files, key=lambda f: os.path.getctime(os.path.join(folder_path, f)), reverse=True)

    # Unzip the newest .zip file with the same name inside the folder path
    if len(zip_files) > 0:
        newest_zip_file = zip_files[0]
        zip_file_path = os.path.join(folder_path, newest_zip_file)
        folder_to_extract = zip_file_path.split('.')[0]
        if os.path.exists(folder_to_extract):
            print(f"{folder_to_extract} already exists, skipping extraction")
            return 
        else:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref: 
                zip_ref.extractall(folder_to_extract)
                return folder_to_extract
    else:
        print("No .zip files found in the folder")