import pandas as pd
import os

COORDS_DIR = os.path.join('.', 'data', 'gps')
WIFI_DIR = os.path.join('.', 'data', 'wifi')

def combine_data(zone, coords_file='coords.xlsx'):
    """
    Combines the WIFI data from complete.csv files and matches them to locations
    from the coordinate data.

    Parameters:
        zone: str
            the name of the zone. eg. whitfeld-1

        coords_file: str
            the location of the coordinate excel sheet

    Returns:
        data: pandas.dataframe
            A dataframe with the data combined
    """
    locations = pd.read_excel(os.path.join(COORDS_DIR, coords_file),
                                sheet_name=zone,
                                usecols=["lat", "lon"]).to_numpy()

    data_folder = os.path.join(WIFI_DIR, zone)
    data_filenames = sorted(os.listdir(data_folder))
    iterations = len(data_filenames) if len(data_filenames) < locations.shape[0] else locations.shape[0]
    data = []
    for i in range(iterations):
        measurements = pd.read_csv(
            os.path.join(data_folder, data_filenames[i]),
            names = ['time', 'bssid', 'quality', 'rssi', 'essid']
        ).to_numpy()

        loc = list(locations[i])

        for measurement in measurements:
            data.append(loc + list(measurement))

    return pd.DataFrame(data,
        columns=['lat', 'lon', 'time', 'bssid', 'quality', 'rssi', 'essid']
    )

def save_wifi_loc_data(dataframe, zone):
    """
    Saves the combined data to it's respective data location as 'wifi_loc.csv'.

    Parameters:
        dataframe: pandas.dataframe
            the dataframe to save

        zone: str
            the zone of the data that was recorded
    """
    dataframe.to_csv(os.path.join(WIFI_DIR, zone, 'wifi_loc.csv'), index=False)

def load_wifi_zone_data(zone, alternative_folder=''):
    """
    Loads the WiFi location data to a pandas dataframe

    Parameters:
        zone: str
            the zone to read for

        alternative_folder: str (optional)
            If data needs to be loaded from a different folder besides the one
            planned. Primarily used for testing.

    Returns:
        a pandas dataframe with the data loaded in
    """
    return pd.read_csv(os.path.join(WIFI_DIR, alternative_folder, zone, 'wifi_loc.csv'))

def load_wifi_at_location(location, alternative_folder=''):
    """
    Loads all of the wifi data for a location by combinining the measurements
    from the zones.

    Parameters:
        location: str
            Name of the location to load data for.
            eg. whitfeld to load all of the data for Whitfeld Oval.

    Returns:
        a pandas dataframe with all of the zone data for a location combined
        together
    """
    return pd.concat(
        [load_wifi_zone_data(x, alternative_folder=alternative_folder)
            for x in os.listdir(WIFI_DIR)
                if os.path.isdir(os.path.join(WIFI_DIR, x)) and location in x]
    ).reset_index()
