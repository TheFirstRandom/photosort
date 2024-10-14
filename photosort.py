import argparse
import os
from PIL import Image
import shutil
from datetime import datetime

def get_modification_date(file_path):
    timestamp = os.path.getmtime(file_path)
    modification_date = datetime.fromtimestamp(timestamp)
    print(f"modification date: {modification_date}")
    return modification_date.strftime("%Y-%m-%d %H:%M:%S")

def get_capture_date(file_path, file):
    try:
        img = Image.open(file_path)
        exif = img._getexif()

        if not exif:
            print(f"{file}: has no EXIF data, take modification date instead")
            return None

        # Check DateTimeOriginal (Tag 36867)
        if 36867 in exif:
            print(f"{file}: EXIF looks correct")
            datetimeoriginal = exif[36867]
            print(f"DateTimeOriginal: {datetimeoriginal}")
            # Convert to datetime object
            capture_date = datetime.strptime(datetimeoriginal, "%Y:%m:%d %H:%M:%S")
            return capture_date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            print(f"{file}: has no DateTimeOriginal EXIF tag, take modification date instead")
            return None

    except Exception as e:
        print(e)
        print("take modification date instead")
        return None

def sort(file_path, end_dir, capture):
    year_folder = os.path.join(end_dir, capture[:4])

    if not os.path.exists(year_folder):
        os.makedirs(year_folder)
        print(f"created new directory: {year_folder}")
    else:
        print(f"directory is already existing: {year_folder}")

    shutil.move(file_path, year_folder)
    print(f"moved file to: {year_folder}")

def unsort(folder_path, end_dir):
    for item in os.listdir(folder_path):
        file_path = os.path.join(folder_path, item)

        if os.path.isfile(file_path):
            shutil.move(file_path, end_dir)
            print(f"{item}: moved to output directory")
        else:
            print(f"{item}: is not a file")

    if len(os.listdir(folder_path)) == 0:
        shutil.rmtree(folder_path)
        print("deleting empty directory")
    else:
        print("there are items left in the directory")

parser = argparse.ArgumentParser(description="Sorts your photos and videos based on their creation date.")

parser.add_argument("source_dir", type=str, help="Path to directory with unsorted files")
parser.add_argument("end_dir", type=str, help="Path to output directory")
parser.add_argument("-r", "--redo", action="store_true", help="Move sorted files back to one folder. source_dir must be the directory with sorted folders.")

args = parser.parse_args()
source_dir = os.path.normpath(args.source_dir)
end_dir = os.path.normpath(args.end_dir)
redo = args.redo

if not os.path.isdir(source_dir):
    print(f"{source_dir}: directory isn't existing yet, create")
    os.makedirs(source_dir)

if not os.path.isdir(end_dir):
    print(f"{end_dir}: directory isn't existing yet, create")
    os.makedirs(end_dir)

if not redo:
    for item in os.listdir(source_dir):
        file_path = os.path.join(source_dir, item)

        if os.path.isfile(file_path):
            capture = get_capture_date(file_path, item)
            if not capture:
                capture = get_modification_date(file_path)
            sort(file_path, end_dir, capture)
        else:
            print(f"{item}: is not a file")
        print()
else:
    for item in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, item)
        if os.path.isdir(folder_path):
            folder_name = os.path.basename(folder_path)
            if folder_name.isdigit():
                year = int(folder_name)
                current_year = datetime.now().year
                if 1000 <= year <= current_year:
                    print(f"{folder_path}: opened directory")
                    unsort(folder_path, end_dir)
                    print()
            else:
                print(f"{folder_path}: directory name is not an integer")
        else:
            print(f"{item}: is not a directory")
