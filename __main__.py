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

WELCOME_MESSAGE = """
Welcome to the File Renamer!
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
    for file in pathlib.Path(directory).iterdir():
        if file.is_file():
            filename = file.name
            filename_without_extension = filename.split(".")[0]
            translated_filename = translator.translate(
                filename_without_extension, lang_tgt="en"
            )
            new_filename = input(
                f"File: \n{filename}\nTranslated File: \n{translated_filename}\nNew File Name: "
            )
            if not new_filename:
                print("Skipping file...")
                continue
            elif new_filename == "exit":
                print("Exiting...")
                break
            else:
                # Rename the file
                new_filename_with_extension = f"{new_filename}.{filename.split('.')[1]}"
                new_file_path = file.parent.joinpath(new_filename_with_extension)
                shutil.move(file, new_file_path)
                print(f"Renamed file to {new_filename_with_extension}\n")


if __name__ == "__main__":
    print(WELCOME_MESSAGE)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory", help="The directory containing the files to be renamed."
    )
    args = parser.parse_args()
    rename_files(args.directory)
