# Download file from URL
This fairly simple script will download a file from a given URL

Usage: `python dl.py <FILE URL>`

## Compiling for convenience
To make it easy to run for can compile to execuatble and place in local bin directory accessable from your PATH

*You will need "pyinstaller" python package installed either globally or in you virtual environment*

To compile: `pyinstaller --onefile dl.py`
The executable file will be in the '/dist' directory

Usage: `dl <FILE URL>`