import zipfile
import os


def compress_files(files, zip_name):
    with zipfile.ZipFile(zip_name, "w") as zipf:
        for file in files:
            zipf.write(file)


def decompress_zip(zip_name, extract_folder):
    with zipfile.ZipFile(zip_name, "r") as zipf:
        zipf.extractall(extract_folder)
