# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 10:38:57 2024

@author: simon
"""

import numpy as np
import matplotlib.pyplot as plt
from windrose import WindroseAxes

def extra_plots(wind_data):
    """
    Plot Windrose and SAR_scene using wind data. 
    
    Parameters:
        wind_data (dict): Dictionary containing wind data with lat, lon.

    Returns:
        None
    """
    # Extract wind data
    latitudes = wind_data['latitude']
    longitudes = wind_data['longitude']
    wind_speed = wind_data['speed']
    wind_dir = wind_data['direction']
    x_lon,y_lat = np.meshgrid(longitudes,latitudes)
    # Create outlier mask
    outlier_mask = np.ma.masked_where(wind_speed <  30, wind_speed).mask
    # Create valid mask
    valid_mask = np.logical_not(outlier_mask)
    # Apply valid mask to the original scene
    valid_ws = np.ma.masked_where(valid_mask, wind_speed)
    sar_scene = np.nansum(valid_ws,0) # calculating SAR scenes
    plt.pcolor(x_lon,y_lat,sar_scene,cmap = "viridis")
    plt.colorbar()
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    # Removing NaN values from wind speed array
    w_speed = wind_speed[~np.isnan(wind_speed)]
    # Removing NaN values from wind direction array
    w_direction = wind_dir[~np.isnan(wind_dir)]
    ax_rose = WindroseAxes.from_ax()
    ax_rose.bar(w_direction, w_speed,normed=True, bins=np.arange(0, 30, 2.5))
    ax_rose.set_legend()
    plt.show()
