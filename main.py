import os
import argparse
import XMLReader
from file_utils import delete_files_with_extensions, move_file, get_files_in_folder

def process_file(file_path):
    try:
        output = XMLReader.read_and_process(file_path)
        move_file(output, r"./FILMS")
        move_file(file_path, r"./DONE")
    finally:
        delete_files_with_extensions(r"./", [".mp4", ".mp3", ".json"])

def process_xml_string(xml_string):
    try:
        output = XMLReader.process_xml_content(xml_string)
        move_file(output, r"./FILMS")
    finally:
        delete_files_with_extensions(r"./", [".mp4", ".mp3", ".json"])

if __name__ == '__main__':
    # Ask the user how they want to process the XML data
    choice = input("Do you want to process a string of XML data (enter 'string') or files from the 'XMLS' folder (enter 'folder')? ")

    if choice.lower() == 'string':
        xml_string = input("Please enter the XML string: ")
        process_xml_string(xml_string)
    elif choice.lower() == 'folder':
        files = get_files_in_folder(r"./XMLS")
        for f in files:
            process_file(f)
    else:
        print("Invalid choice. Please enter 'string' or 'folder'.")
