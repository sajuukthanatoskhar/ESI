"""
This file looks at getting, setting up files

At the end of this, one will use this to setup the whole directory
"""
import os
import urllib.request
import bz2
import shutil


def create_temp_folder_and_download(website: str, folder="default_temp") -> bool:
    try:
        os.mkdir(folder)
    except FileExistsError:
        pass
    new_file = "{}/eve.db.bz2".format(folder)
    urllib.request.urlretrieve(website, new_file)


    with open("{}/eve.db".format(folder), "wb") as eve_db_file:
        eve_db_file.write(bz2.BZ2File(new_file).read())
        eve_db_file.close()


def extract_files(website):
    return True


def download_files(website: str, folder: str) -> bool:
    """Downloads files from website into temp folder"""
    if create_temp_folder_and_download(website, folder="tempfolder"):
        return True
    extract_files(website)


def format_files() -> bool:
    return True


if __name__ == '__main__':
    download_files("https://www.fuzzwork.co.uk/dump/latest/eve.db.bz2", folder="temp_folder")
