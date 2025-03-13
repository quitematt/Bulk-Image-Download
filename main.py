import os
import requests
import logging
from urllib.parse import urlparse

def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file), # Log to file
            logging.StreamHandler() # Log to console
        ]
    )

def download_images(url_file, output_folder="downloaded_images", log_file="log.txt"):
    
    setup_logging(log_file)
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Read URLs from the text file
    with open(url_file, "r") as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()
        if not url:
            logging.info("Skipped an empty line in the URL file.")
            continue
        
        try:
            # Extract filename from URL (remove query parameters)
            parsed_url = urlparse(url)
            file_name = os.path.basename(parsed_url.path)
            
            if not file_name:
                logging.warning(f"Skipped: {url} (No valid filename)")
                continue
            
            image_path = os.path.join(output_folder, file_name)
            
            logging.info(f"Downloading: {url}")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(image_path, "wb") as image_file:
                for chunk in response.iter_content(1024):
                    image_file.write(chunk)

            logging.info(f"Successfully downloaded: {file_name}")

        except requests.HTTPError as http_err:
            logging.error(f"HTTP error for {url}: {http_err}")
        except requests.RequestException as req_err:
            logging.error(f"Network error for {url}: {req_err}")
        except Exception as err:
            logging.error(f"Unexpected error for {url}: {err}")

if __name__ == "__main__":
    url_list_file = "urls.txt"  # Change this if needed
    download_images(url_list_file)