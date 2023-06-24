#!/bin/python3

"""
A simple script that renames all files in a directory to a given name. Particularly useful for renaming files downloaded
 from the internet in a different language to English. It uses the Google Translate API to translate the name of the
  file.
"""

import argparse
import pathlib
import shutil

from google_trans_new import google_translator

WELCOME_MESSAGE = """Welcome to the File Renamer!
This script renames all files in a directory to a given name and translates it for you.
"""


def rename_files(directory) -> None:
    """
    Renames all files in a directory to a given name. Particularly useful for renaming files downloaded from the
    internet in a different language to English. It uses the Google Translate API to translate the name of the file.
    :param directory: The directory containing the files to be renamed.
    :return: None
    """
    translator = google_translator()
    # Use while loop to allow user to repeat file on bad name
    directory = pathlib.Path(directory)

    # Get list of files in directory
    files = [file for file in directory.iterdir()]

    i = 0
    while i < len(files):
        file = files[i]
        rename = True
        if file.is_file():
            filename = file.name
            filename_without_extension = filename.split(".")[0]
            translated_filename = translator.translate(
                filename_without_extension, lang_tgt="en"
            )

            new_filename = input(
                f"File | Translated file\n{filename_without_extension}\n{translated_filename}\nNew File Name: "
            )

            if not new_filename:
                print("Skipping file...")
                i += 1
                continue
            if new_filename == "exit":
                print("Exiting...")
                break

            new_filename_with_extension = f"{new_filename}.{filename.split('.')[1]}"

            # Make sure the new filename is unique
            if directory.joinpath(new_filename_with_extension).exists():
                print("File already exists. Please choose a different name.\n")
                rename = False

            # Check for illegal characters in the filename
            illegal_characters = ["<", ">", ":", '"', "/", "\\", "|", "?", "*"]
            for character in illegal_characters:
                if character in new_filename_with_extension:
                    print(
                        "Illegal character in filename. Please choose a different name.\n"
                    )
                    rename = False

            if rename:
                new_file_path = file.parent.joinpath(new_filename_with_extension)
                shutil.move(file, new_file_path)
                print(f"Renamed file to \"{new_filename_with_extension}\"\n")

                i += 1


if __name__ == "__main__":
    print(WELCOME_MESSAGE)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory", help="The directory containing the files to be renamed."
    )
    args = parser.parse_args()
    rename_files(args.directory)
