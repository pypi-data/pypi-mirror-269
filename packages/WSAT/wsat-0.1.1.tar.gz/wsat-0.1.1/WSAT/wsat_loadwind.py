# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 17:40:52 2024

@author: simon
"""

import os
import numpy as np
from netCDF4 import Dataset

def load_wind(file_paths, lat_params, lon_params, wind_names):
    """
    Load wind data from NetCDF files.

    Parameters:
        file_paths (str): Path to the directory containing NetCDF files.
        lat_params (tuple): Tuple containing (lat_name, lat_range).
        lon_params (tuple): Tuple containing (lon_name, lon_range).
        wind_names (tuple): Tuple containing (wind_speed_name, wind_direction_name).

    Returns:
        wind_data (dict): Dicti½onary containing wind data with lat, lon.
    """
    lat_name, lat_range = lat_params
    lon_name, lon_range = lon_params
    ws_name, wd_name = wind_names
    wind_data = {'latitude': [], 'longitude': [], 'speed': [], 'direction': []}

    # Load latitude and longitude
    with Dataset(os.path.join(file_paths, os.listdir(file_paths)[0]),'r',format='NETCDF4') as nc_da:
        latitudes = nc_da.variables[lat_name][:]
        longitudes = nc_da.variables[lon_name][:]
        # Determine indices for latitude and longitude ranges
        lat_indices = slice(None)
        lon_indices = slice(None)
        if lat_range is not None:
            min_lat, max_lat = lat_range
            lat_indices = np.where((latitudes >= min_lat) & (latitudes <= max_lat))[0]
            latitudes = latitudes[lat_indices]
        if lon_range is not None:
            min_lon, max_lon = lon_range
            lon_indices = np.where((longitudes >= min_lon) & (longitudes <= max_lon))[0]
            longitudes = longitudes[lon_indices]

    # Get list of filenames in the directory
    filenames = os.listdir(file_paths)
    for filename in filenames:
        # Construct full path to each file
        file_path = os.path.join(file_paths, filename)
        with Dataset(file_path, 'r', format='NETCDF4') as dataset:
            # Subset wind components based on latitude and longitude ranges
            wind_speed = dataset.variables[ws_name][:, lat_indices, lon_indices]
            wind_direction = dataset.variables[wd_name][:, lat_indices, lon_indices]
            # Append wind data to the dictionary
            wind_data['speed'].append(wind_speed)
            wind_data['direction'].append(wind_direction)
    wind_data['latitude'].append(latitudes)
    wind_data['longitude'].append(longitudes)
    # Convert lists to numpy arrays
    wind_data['latitude'] = np.concatenate(wind_data['latitude'])
    wind_data['longitude'] = np.concatenate(wind_data['longitude'])
    wind_data['speed'] = np.concatenate(wind_data['speed'])
    wind_data['direction'] = np.concatenate(wind_data['direction'])
    #check the data
    check_data = np.all(np.isnan(wind_data['speed']))
    if check_data:
        print('No data available in specified longitude, latitude range')
    return wind_data
