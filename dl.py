import sys
import argparse
import requests
import re
from tqdm import tqdm
import os
from urllib.parse import urlparse, unquote

def is_url(string):
    """
    Check if a string is a valid URL.
    """
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except:
        return False

def download_file(url, directory=".", position=0):
    """
    Download a file from a URL, showing a progress bar during download.
    Skips download if file already exists with the same size.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True, allow_redirects=True)

        # Try to extract the filename from the Content-Disposition header
        content_disposition = response.headers.get('content-disposition')
        if content_disposition:
            # Updated regular expression to accurately capture the filename
            matches = re.findall('filename="?([^"]+)"?;?', content_disposition)
            if matches:
                filename = matches[0]
            else:
                # Fallback to URL if no match in Content-Disposition
                filename = unquote(urlparse(response.url).path.split('/')[-1])
        else:
            # Fallback method: Extract the filename from the URL after following any redirects
            filename = unquote(urlparse(response.url).path.split('/')[-1])

        # Default filename if none is found
        if not filename:
            filename = "downloaded_file"

        file_path = os.path.join(directory, filename)

        # Check if file exists and has the same size
        if os.path.exists(file_path) and os.path.getsize(file_path) == int(response.headers.get('content-length', 0)):
            print(f"File already exists and has the same size. Skipping: {filename}")
            return

        # Download the file with a progress bar
        with open(file_path, "wb") as file, tqdm(
                desc=filename,
                total=int(response.headers.get('content-length', 0)),
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
                position=position
            ) as bar:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)
    except Exception as e:
        print(f"Error downloading file: {url}. Error: {e}")

# Rest of your script...

def download_from_list(file_path, directory="."):
    """
    Read URLs from a file and download each file, displaying a progress bar for each.
    """
    try:
        with open(file_path, 'r') as file:
            urls = file.read().splitlines()

        file_bar_position = 0  # Position for file progress bars, reused for each file
        for url in urls:
            if is_url(url):
                download_file(url, directory, position=file_bar_position)

    except Exception as e:
        print(f"Error processing file: {file_path}. Error: {e}")

def main():
    # Parsing command-line arguments
    parser = argparse.ArgumentParser(description="Download files from URLs.")
    parser.add_argument("input", help="URL or file containing URLs to download")
    args = parser.parse_args()

    if args.input is None:
        parser.error("No input provided. Please provide a URL or a file path.")

    # Determine if the input is a URL or a file path
    if is_url(args.input):
        download_file(args.input)
    elif os.path.isfile(args.input):
        download_from_list(args.input)
    else:
        parser.error(f"Input is neither a valid URL nor an existing file: {args.input}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        download_url = sys.argv[1]
        download_file(download_url)
    else:
        print("Usage: dl <URL> | <FILENAME_WITH_URL_LIST>")
