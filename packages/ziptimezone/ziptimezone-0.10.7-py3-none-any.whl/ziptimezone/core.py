from timezonefinder import TimezoneFinder
import csv
from .data_manager import get_data_file_path
from .mappings import map_timezone_to_region
'''
def load_zip_data():
    """
    Loads ZIP code data from a CSV file into a dictionary.

    Returns:
        dict: A dictionary where the keys are ZIP codes and the values are dictionaries with
              latitude and longitude.
    """
    file_path = get_data_file_path()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['country_code', 'postal_code', 'place_name', 'admin_name1',
                                                     'admin_code1', 'admin_name2', 'admin_code2', 'admin_name3',
                                                     'admin_code3', 'latitude', 'longitude', 'accuracy'], delimiter='\t')
        zip_data = {row['postal_code']: row for row in reader}
    return zip_data
'''
loaded_zip_data = None

def load_zip_data():
    """
    Loads ZIP code data from a CSV file into a dictionary if it is not already loaded.

    Returns:
        dict: A dictionary where the keys are ZIP codes and the values are dictionaries with
              latitude and longitude.
    """
    global loaded_zip_data
    if loaded_zip_data is not None:
        return loaded_zip_data

    file_path = get_data_file_path()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['country_code', 'postal_code', 'place_name', 'admin_name1',
                                                     'admin_code1', 'admin_name2', 'admin_code2', 'admin_name3',
                                                     'admin_code3', 'latitude', 'longitude', 'accuracy'], delimiter='\t')
        loaded_zip_data = {row['postal_code']: row for row in reader}
    return loaded_zip_data

def get_lat_long_for_zip(zip_code, country='US'):
    """
    Retrieve the latitude and longitude for a given ZIP code.

    Parameters:
        zip_code (str): The ZIP code for which geographic coordinates are requested.
        country (str): Country code to refine the search, default is 'US'.

    Returns:
        tuple: A tuple containing latitude and longitude (float, float) if found, otherwise (None, None).

    Raises:
        ValueError: If the zip_code is not recognized.
    """
    
    if not isinstance(zip_code, str) or zip_code.strip() == '':
        # Return None if the zip_code is not a string or is an empty string.
        return None, None
    
    zip_data = load_zip_data()
    location = zip_data.get(zip_code)
    
    if location is not None and location['latitude'] is not None and location['longitude'] is not None: #pd.isna(location.latitude) and not pd.isna(location.longitude):
        return location['latitude'], location['longitude']
    else:
        return None, None
    
def get_timezone_by_zip(zip_code):
    """
    Retrieve the timezone based on the provided ZIP code from locally stored data.

    This function uses geographic coordinates obtained from a ZIP code stored in a local file
    to determine the corresponding timezone using the TimezoneFinder library.

    Parameters:
        zip_code (str): The ZIP code for which the timezone is requested.

    Returns:
        str: The timezone string (e.g., 'America/New_York') if found,
             returns 'Unknown' if the timezone cannot be determined.

    Raises:
        ValueError: If no geographic coordinates can be determined for the given ZIP code.
    """
    latitude, longitude = get_lat_long_for_zip(zip_code)
    if latitude and longitude:
        tf = TimezoneFinder(in_memory=True)
        timezone = tf.timezone_at(lat=float(latitude), lng=float(longitude))
        if timezone:
            return map_timezone_to_region(timezone)
        else:
            return 'Unknown'
    else:
        #raise ValueError(f"No valid geographic coordinates found for ZIP code {zip_code}.")
        return f"No valid geographic coordinates for ZIP Code {zip_code} in US"