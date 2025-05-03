import os
import shutil

def delete_files_with_extensions(folder_path, extensions):
    try:
        files = os.listdir(folder_path)
        print(files)

        files_to_delete = [file for file in files if file.lower().endswith(tuple(extensions))]
        for i in range(10):
            file_path = os.path.join(folder_path, str(i))
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")

        for file_to_delete in files_to_delete:
            file_path = os.path.join(folder_path, file_to_delete)
            os.remove(file_path)
            print(f"Deleted: {file_path}")

        print("Deletion completed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def move_file(source_path, target_folder):
    try:
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        file_name = os.path.basename(source_path)
        target_path = os.path.join(target_folder, file_name)

        shutil.move(source_path, target_path)

        print(f"File moved to: {target_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def get_subdirectories(parent_folder):
    try:
        all_items = os.listdir(parent_folder)
        subdirectories = [item for item in all_items if os.path.isdir(os.path.join(parent_folder, item))]
        subdirectory_paths = [os.path.join(parent_folder, subdir) for subdir in subdirectories]

        return subdirectory_paths
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

def get_files_in_folder(folder_path):
    try:
        all_items = os.listdir(folder_path)
        files = [item for item in all_items if os.path.isfile(os.path.join(folder_path, item))]
        file_paths = [os.path.join(folder_path, file) for file in files]

        return file_paths
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []
