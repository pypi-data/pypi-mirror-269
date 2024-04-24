# data_manager.py
import os
import requests
import zipfile
import logging
import shutil
from .globals import load_zip_data, get_loaded_zip_data

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def download_and_extract_zip_data(data_url, data_directory):
    """
    Downloads and extracts ZIP code data, then loads it into memory.

    Parameters:
        data_url (str): URL from which to download the ZIP file.
        data_directory (str): Directory to store and extract data.
    """
    file_path = os.path.join(data_directory, "US.txt")
    if not os.path.exists(file_path):
        zip_path = file_path + ".zip"
        logging.info("Downloading ZIP code data...")
        try:
            response = requests.get(data_url)
            response.raise_for_status()
            with open(zip_path, "wb") as f:
                f.write(response.content)
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(data_directory)
            os.remove(zip_path)
            logging.info("Data downloaded and extracted successfully.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return

    load_zip_data(file_path)  # Load data into the global variable


def get_data_file_path():
    """
    Constructs the file path for storing the data file within the package.

    Returns:
        str: The file path where the data file should be stored. This path points to a directory 'data' at the same level as this script.
    """
    data_directory = os.path.join(os.path.dirname(__file__), "..", "ziptimezone_data")
    os.makedirs(data_directory, exist_ok=True)
    return data_directory


def refresh_data_if_needed():
    """
    Ensures that ZIP code data is loaded upon initial import or application startup.
    This can also be called later if needed. Deletes existing data directory if it exists,
    and re-downloads and extracts the ZIP file.
    """
    data_directory = get_data_file_path()

    # Check if the directory exists and remove it if it does
    if os.path.exists(data_directory):
        shutil.rmtree(data_directory)
        print(f"Existing data directory {data_directory} removed.")

    # Recreate the directory
    os.makedirs(data_directory, exist_ok=True)
    print(f"Data directory {data_directory} created.")

    # URL for the ZIP file to download
    data_url = "https://download.geonames.org/export/zip/US.zip"

    # Download and extract the ZIP file
    download_and_extract_zip_data(data_url, data_directory)
    print("Data downloaded and extracted successfully.")


if __name__ != "__main__":
    refresh_data_if_needed()
