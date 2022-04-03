# Imports

from pathlib import Path
from tkinter import Tk, filedialog, simpledialog
from zipfile import ZIP_DEFLATED, ZipFile
from os import PathLike
from typing import Union

# Functions

def get_dir_size(dir_path):
    total_bytes = 0
    for f in dir_path.rglob("*"):
        total_bytes += f.stat().st_size
    return total_bytes

def zip_dir(zip_name: str, source_dir: Union[str, PathLike]):
    src_path = Path(source_dir).expanduser().resolve(strict=True)
    with ZipFile(zip_name, 'w', ZIP_DEFLATED) as zf:
        for file in src_path.rglob('*'):
            zf.write(file, file.relative_to(src_path.parent))

def convert_bytes(bytes_number):
    tags = [ "Byte", "Kilobyte", "Megabyte", "Gigabyte", "Terabyte" ]

    i = 0
    double_bytes = bytes_number
 
    while (i < len(tags) and  bytes_number >= 1024):
            double_bytes = bytes_number / 1024.0
            i = i + 1
            bytes_number = bytes_number / 1024
 
    return str(round(double_bytes, 2)) + " " + tags[i]

# Constants and configs

root = Tk()
root.withdraw()

PARENT_FOLDER = Path(filedialog.askdirectory(title="Please select a parent folder containing subfolders to zip."))

total_bytes_saved = 0
not_zipped = list()
zip_suffixes = {".zip", ".rar", ".7z"}

choice = simpledialog.askstring(title="User Input", prompt="Select a [parent of parent] or just a [parent] folder?")

# Procedural Code

if choice == "parent of parent":
    filter = "*/*"
elif choice == "parent":
    filter = "*"
else:
    raise Exception("User did not select 'parent' or 'parent of parent'")

for project_folder in PARENT_FOLDER.glob(filter):
    if project_folder.is_dir() and project_folder.suffix not in zip_suffixes:
        project_folder_size = get_dir_size(project_folder)
        if project_folder_size > 4000000000:
            print(f"Contents of {project_folder.name} amount to {project_folder_size} bytes. Very large.")
            not_zipped.append(project_folder.name)
        else:
            print(f"Contents of {project_folder.name} amount to {project_folder_size} bytes. Zipping it up.")
            zip_filename = project_folder.name + ".zip"
            zip_filepath = PARENT_FOLDER / zip_filename
            zip_dir(zip_name=zip_filepath, source_dir=project_folder)
            total_bytes_saved += project_folder_size - zip_filepath.stat().st_size


print(f"Saved {convert_bytes(total_bytes_saved)}.")
print("Projects too large to be zipped:")
print(*not_zipped)