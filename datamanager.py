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
                                usecols=["Latitude", "Longtitude"])

    wifi_data = pd.read_csv(os.path.join(WIFI_DIR, zone, 'complete.csv'),
                            names=['time', 'bssid', 'channel', 'quality', 'rssi', 'essid'])

    locations['time'] = pd.DataFrame(data=wifi_data['time'].unique())
    result = pd.merge(locations, wifi_data, on='time')
    result.columns = ['lat', 'lon', 'time', 'bssid', 'channel', 'quality', 'rssi', 'essid']
    return result, locations

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

def load_wifi_loc_data(zone, alternative_folder=''):
    """
    Loads the WiFi location data to a pandas dataframe

    Parameters:
        zone: str
            the zone to read for

    Returns:
        a pandas dataframe with the data loaded in
    """
    return pd.read_csv(os.path.join(WIFI_DIR, alternative_folder, zone, 'wifi_loc.csv'))
