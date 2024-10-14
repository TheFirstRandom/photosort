# PHOTOSORT

---

## About
This program reads the EXIF data from photos or similar files. It creates a folder in the target directory named after the year the file was taken (EXIF tag: `DateTimeOriginal`) and moves the file there. If no capture date is available, the modification date is used instead. Use `--redo` to reverse the process.

## OS
Python version: Windows, macOS, Linux  
Executable: Windows

## Installation (only for the Python version)
Python installation:  
[Python for Windows](https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe)  
[Python for macOS](https://www.python.org/ftp/python/3.13.0/python-3.13.0-macos11.pkg)

Required Python packages:
- Pillow: `pip install pillow`

## Usage
Command for the Python package:
`python /path/to/photosort.py`

Command for the executable (exe):
`X:\path\to\photosort.exe`

Run `--help` for more information.

## Notes
It is possible that antivirus software may block the executable, as it accesses personal data (the image files) on your PC. Try using the Python version instead or mark the executable as trusted.
