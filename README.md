# Download file from URL
This fairly simple script will download a file from a given URL

Install packages `pip install -r requirements.txt`

Usage: `python dl.py <FILE URL> | <FILE_WITH_URL_LIST>`

## Compiling for convenience
To make it easy to run for can compile to execuatble and place in local bin directory accessable from your PATH

*You will need "pyinstaller" python package installed either globally or in you virtual environment*

### Note: You need system build packages installed from this to compile without errors
*On Ubuntu/Debian:`sudo apt install build-essential`*
*Then install with pip: `pip install pyinstaller`*

To compile: `pyinstaller --onefile dl.py`
The executable file will be in the '/dist' directory
To make it generally available, move the executable file 'dl' to somewhere on your local PATH

Usage: `Usage: dl <URL> | <FILENAME_WITH_URL_LIST>`
