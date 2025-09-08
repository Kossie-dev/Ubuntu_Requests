import requests
import os
import sys
import uuid
from urllib.parse import urlparse

def download_image(url):
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    directory="Fetched_Images"
    try:
        os.makedirs(directory, exist_ok=True)
        print(f"Directory '{directory}' created or already exists.")
    except OSError as e:
        print(f"Error creating directory '{directory}': {e}", file=sys.stderr)
        return
    
    try:
        parsed_url=urlparse(url)
        path=parsed_url.path
        filename= os.path.basename(path)
        if not filename:
            filename=f"image_{uuid.uuid4().hex}.jpg"
    except Exception as e:
        print(f"Error parsing URL '{url}': {e}", file=sys.stderr)
        return
    
    filepath=os.path.join(directory, filename)

    print(f"Attempting to download image from: {url}")
    print(f"Saving to: {filepath}")

    try:
        response=requests.get(url, stream=True)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded and saved: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"HTTP Error: Could not download image. Details: {e}", file=sys.stderr)
    except IOError as e:  
        print(f"File I/O Error: Could not save image. Details: {e}", file=sys.stderr)
    
if __name__ == "__main__":
    image_url = input("Enter the image URL to download: ").strip()
    if not image_url:
        print("No URL provided. Exiting.", file=sys.stderr)
    else:
        download_image(image_url)