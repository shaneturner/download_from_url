import sys
import os
import requests
from tqdm import tqdm

def get_filename_from_cd(cd):
    """
    Get filename from content-disposition header, handling additional parameters correctly.
    """
    if not cd:
        return None
    # Split the content-disposition header into parts and find the filename
    parts = cd.split(';')
    for part in parts:
        part = part.strip()
        if part.startswith('filename*='):
            # Extended filename syntax (RFC 5987)
            # Example: filename*=UTF-8''My%20Document.pdf
            value = part.split('\'', 2)[2]
            return requests.utils.unquote(value)
        elif part.startswith('filename='):
            # Basic filename syntax
            # Example: filename="My Document.pdf"
            value = part[9:].strip('"')
            return value
    return None


def download_file(url):
    """
    Download file from a given URL with streaming.
    """
    response = requests.get(url, stream=True)
    total = int(response.headers.get('content-length', 0))
    filename = get_filename_from_cd(response.headers.get('content-disposition'))

    if not filename:
        filename = url.split("/")[-1]

    # Check if the file exists and compare its size
    if os.path.exists(filename) and os.path.getsize(filename) == total:
        print(f"File already exists and is complete: {filename}")
        return

    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        download_url = sys.argv[1]
        download_file(download_url)
    else:
        print("Usage: dl <URL>")
