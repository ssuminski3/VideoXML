import os
import XMLReader
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    print(os.getcwd())

import os

def delete_files_with_extensions(folder_path, extensions):
    try:
        # List all files in the folder
        files = os.listdir(folder_path)
        print(files)
        # Filter files with specified extensions
        files_to_delete = [file for file in files if file.lower().endswith(tuple(extensions))]
        for i in range(10):
            file_path = os.path.join(folder_path, str(i))
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        # Delete each file
        for file_to_delete in files_to_delete:
            file_path = os.path.join(folder_path, file_to_delete)
            os.remove(file_path)
            print(f"Deleted: {file_path}")

        print("Deletion completed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

import shutil

def move_file(source_path, target_folder):
    try:
        # Create the target folder if it doesn't exist
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        # Get the file name from the source path
        file_name = os.path.basename(source_path)

        # Create the target path by joining the target folder and file name
        target_path = os.path.join(target_folder, file_name)

        # Move the file to the target folder
        shutil.move(source_path, target_path)

        print(f"File moved to: {target_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_subdirectories(parent_folder):
    try:
        # Get a list of all items in the parent folder
        all_items = os.listdir(parent_folder)

        # Filter only the subdirectories
        subdirectories = [item for item in all_items if os.path.isdir(os.path.join(parent_folder, item))]

        # Get the full path of each subdirectory
        subdirectory_paths = [os.path.join(parent_folder, subdir) for subdir in subdirectories]

        return subdirectory_paths
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
def get_files_in_folder(folder_path):
    try:
        # Get a list of all items in the folder
        all_items = os.listdir(folder_path)

        # Filter only the files (not directories)
        files = [item for item in all_items if os.path.isfile(os.path.join(folder_path, item))]

        # Get the full path of each file
        file_paths = [os.path.join(folder_path, file) for file in files]

        return file_paths
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []



if __name__ == '__main__':
    #dir = get_subdirectories(r"C:\Users\sebas\OneDrive\Pulpit\Tabele_do_tworzenia")
    project_folder = r"./"
    extensions_to_delete = [".mp4", ".mp3", ".json"]
    delete_files_with_extensions(project_folder, extensions_to_delete)

    files = get_files_in_folder(r"./XMLS")
    for f in files:
        try:
            output = XMLReader.Read(f)
            move_file(output, r"./FILMS")
            move_file(f, r"./DONE")
            delete_files_with_extensions(project_folder, extensions_to_delete)
        except:
            delete_files_with_extensions(project_folder, extensions_to_delete)
