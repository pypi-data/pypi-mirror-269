import csv

loaded_zip_data = None


def load_zip_data(file_path):
    """
    Loads ZIP code data from a CSV file into a global dictionary if it is not already loaded.

    Parameters:
        file_path (str): The full path to the CSV file containing ZIP code data.

    Returns:
        dict: A dictionary where the keys are ZIP codes and the values are dictionaries with latitude and longitude.
    """
    global loaded_zip_data
    if loaded_zip_data is None:
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(
                csvfile,
                fieldnames=[
                    "country_code",
                    "postal_code",
                    "place_name",
                    "admin_name1",
                    "admin_code1",
                    "admin_name2",
                    "admin_code2",
                    "admin_name3",
                    "admin_code3",
                    "latitude",
                    "longitude",
                    "accuracy",
                ],
                delimiter="\t",
            )
            loaded_zip_data = {
                row["postal_code"]: {
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                }
                for row in reader
            }
    return loaded_zip_data


def get_loaded_zip_data():
    """
    Accesses the globally loaded ZIP code data.

    Returns:
        dict: The dictionary containing loaded ZIP code data.
    """
    global loaded_zip_data
    return loaded_zip_data
