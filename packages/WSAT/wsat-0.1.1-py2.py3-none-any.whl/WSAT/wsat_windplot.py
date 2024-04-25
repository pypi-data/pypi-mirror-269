# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 09:39:01 2024

@author: simon
"""
import warnings
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def plot_wind_map(wind_data):
    """
    Plot wind map using wind data.

    Parameters:
        wind_data (dict): Dictionary containing wind data with lat, lon.

    Returns:
        None
    """
    # Extract wind data
    lat = wind_data['latitude']
    lon = wind_data['longitude']
    wind_speed = wind_data['speed']
    wind_direction = wind_data['direction']
    # Calculate mean wind speed and wind components
    warnings.filterwarnings("ignore", message="Mean of empty slice", category=RuntimeWarning)
    mean_wind_speed = np.nanmean(wind_speed, axis=0)
    u_comp = wind_speed * np.cos(np.deg2rad(270 - wind_direction))
    v_comp = wind_speed * np.sin(np.deg2rad(270 - wind_direction))
    mean_u = np.nanmean(u_comp, axis=0)
    mean_v = np.nanmean(v_comp, axis=0)
    x_lon,y_lat = np.meshgrid(lon,lat)

    # Plot wind map with basemap
    plt.figure(figsize=(10, 8))
    b_map = Basemap(projection='cyl',llcrnrlon=np.min(lon),llcrnrlat=np.min(lat),
                    urcrnrlon=np.max(lon),urcrnrlat=np.max(lat),epsg=4326,resolution='f')
    b_map.shadedrelief()
    b_map.drawcoastlines()
    b_map.drawcountries(linewidth=1, linestyle='solid', color='k')
    plt.title("Shaded relief image as background map", fontsize=18)
    plt.pcolor(x_lon, y_lat, mean_wind_speed, cmap='plasma')
    plt.gca().tick_params(labelsize=18)
    plt.clim(0, 20)  # Colormap limit
    plt.colorbar(label='Wind speed m/s')
    step = 15
    plt.quiver(x_lon[::step, ::step], y_lat[::step, ::step],
               mean_u[::step, ::step], mean_v[::step, ::step], mean_wind_speed[::step, ::step],
               cmap="gist_gray", units='xy')
    plt.title('Wind map with Basemap', fontsize=18)
    plt.xlabel('Longitude', fontsize=14)
    plt.ylabel('Latitude', fontsize=14)
    plt.show()
