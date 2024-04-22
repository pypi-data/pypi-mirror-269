import os
import concurrent.futures
from .core import get_timezone_by_zip
import logging

# Setup basic logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def process_zip_code(zip_code):
    """Helper function to process a single ZIP code and handle exceptions."""
    try:
        return zip_code, get_timezone_by_zip(zip_code)
    except Exception as e:
        logging.error(f"Error processing ZIP code {zip_code}: {str(e)}")
        return zip_code, None


def get_timezone_for_many_zips(zip_codes, max_workers=None):
    """
    Processes a list of ZIP codes in parallel using ThreadPoolExecutor,
    retrieving time zones for each. The number of workers can be customized based on the machine.

    Args:
        zip_codes (list of str): A list of ZIP codes.
        max_workers (int, optional): Maximum number of threads to use for parallel processing. If None, it defaults to the number of processors on the machine, times two.

    Returns:
        dict: A dictionary mapping ZIP codes to their corresponding time zones or None if an error occurred.
    """
    if max_workers is None:
        max_workers = (
            os.cpu_count() * 2
        )  # Sample heuristic: twice the number of cores, can be changed with testing and feedback

    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_zip = {
            executor.submit(process_zip_code, zip): zip for zip in zip_codes
        }
        for future in concurrent.futures.as_completed(future_to_zip):
            zip_code = future_to_zip[future]
            try:
                _, timezone = future.result()
                results[zip_code] = timezone
            except Exception as exc:
                logging.error(f"Exception for ZIP code {zip_code}: {exc}")
                results[zip_code] = None
    return results
