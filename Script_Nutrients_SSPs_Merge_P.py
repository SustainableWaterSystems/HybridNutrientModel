



import pandas as pd
import numpy as np 
from matplotlib import pyplot as plt
from numpy import hstack
import geopandas as gpd
import mapclassify
import netCDF4 as nc
import cartopy.crs as ccrs
from pylab import *
from scipy import ndimage
import cartopy
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
from datetime import date
import xarray




for SSP in ['SSP1','SSP2','SSP3','SSP4','SSP5']:



  section1 = nc.Dataset('/archive/depfg/graha010/Analysis_Of_Nutrients/FUTURE_' + SSP + '_Hybrid_TP_2011_2015_WithMB.nc')
  section2 = nc.Dataset('/archive/depfg/graha010/Analysis_Of_Nutrients/FUTURE_' + SSP + '_Hybrid_TP_WithMB.nc')
  combined_data = np.concatenate([section1['HybTP_MB'][:,:,:],section2['HybTP_MB'][:,:,:]],axis=0)


  #print(section1['HybTP_MB'].shape)
  #print(section2['HybTP_MB'].shape)
  #print(combined_data.shape)



  misc = nc.Dataset('/archive/depfg/graha010/duncan_copied_additional/hist-hydrology_monthly_variable_2011_2015.nc')
  time1 = misc['time'][:]
  lat = misc['lat'][:]
  lon = misc['lon'][:]
  
  
  if SSP == 'SSP1':
    misc = nc.Dataset('/archive/depfg/graha010/duncan_copied_scenarios/rcp4.5-hydrology_monthly_variable_2016_2099.nc')
  elif SSP == 'SSP2':
    misc = nc.Dataset('/archive/depfg/graha010/duncan_copied_future/rcp6.0-hydrology_monthly_variable_2016_2099.nc')
  elif SSP == 'SSP3':
    misc = nc.Dataset('/archive/depfg/graha010/duncan_copied_future/rcp6.0-hydrology_monthly_variable_2016_2099.nc')
  elif SSP == 'SSP4':
    misc = nc.Dataset('/archive/depfg/graha010/duncan_copied_future/rcp6.0-hydrology_monthly_variable_2016_2099.nc')
  elif SSP == 'SSP5':
    misc = nc.Dataset('/archive/depfg/graha010/duncan_copied_scenarios/rcp8.5-hydrology_monthly_variable_2016_2099.nc')


  time2 = misc['time'][:]
  lat = misc['lat'][:]
  lon = misc['lon'][:]



  #print(time1)
  #print(time2)


  combined_time = np.concatenate([time1,time2])


  #print(time1.shape)
  #print(time2.shape)
  #print(combined_time.shape)



  data = xarray.DataArray(combined_data, coords=[('time', combined_time), ('lat', lat), ('lon', lon)], name='Pconc')
  
  data.attrs['name'] = 'Total Phosphorus (IMAGE-GNM with Random Forest and Mass Balance)'
  data.attrs['units'] = 'mg/l'
  data.time.attrs['name'] = 'time'
  data.time.attrs['units'] = 'days since 1800-01-01'
  data.lat.attrs['name'] = 'latitude'
  data.lat.attrs['units'] = 'degrees_north'
  data.lon.attrs['name'] = 'longitude'
  data.lon.attrs['units'] = 'degrees_east'



  ds = data.to_dataset()




  ds.attrs['comment'] = 'IMAGE-GNM with Random Forest and Mass Balance has output for selected months. The date of the output is valid for the specified month'
  ds.attrs['Conventions'] = 'CF-1.7'
  ds.attrs['license'] = 'The Creative Commons License (CC BY 4.0) applies to all of the IMAGE-GNM data. (see https://creativecommons.org/licenses/by/4.0/)'
  ds.attrs['creator_name'] = 'Duncan Graham, Arthur Beusen, Marc Bierkens, Michelle van Vliet'
  ds.attrs['creator_email'] = 'd.j.graham@uu.nl'
  ds.attrs['comments'] = 'If this data set is a major contribution to your research, we would like to be coauthor on any manuscript. If the data is being included in a published manuscript, we would like to see a preprint before submission to make sure the data description is correct'
  ds.attrs['disclaimer'] = 'These data can be used freely for research purposes provided that the work is properly cited. Great care was exerted to prepare these data. Notwithstanding, use of the data is the sole responsibility of the user. This data is made available in the hope that it will be useful, but WITHOUT ANY WARRANTY,  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE'
  ds.attrs['summary'] = 'A full run of IMAGE-GNM with Random Forest and Mass Balance contains grid format data with a spatial resolution of 0.5 by 0.5 degree for all the months'
  ds.attrs['data_type'] = 'grid format with a spatial resolution of 0.5 by 0.5 degree and global extent'
  ds.attrs['references'] = 'Graham et al. (2026), https://doi.org/10.5281/zenodo.20625547'
  ds.attrs['publisher_name'] = 'Utrecht University, The Netherlands'
  ds.attrs['institution'] = 'Utrecht University, The Netherlands'
  ds.attrs['date_created'] = 'June 10 2026'
  if SSP == 'SSP1':
    ds.attrs['description'] = 'SSP1 run with RCP 4.5.'
  elif SSP == 'SSP2':
    ds.attrs['description'] = 'SSP2 run with RCP 6.0.'
  elif SSP == 'SSP3':
    ds.attrs['description'] = 'SSP3 run with RCP 6.0.'
  elif SSP == 'SSP4':
    ds.attrs['description'] = 'SSP4 run with RCP 6.0.'
  elif SSP == 'SSP5':
    ds.attrs['description'] = 'SSP5 run with RCP 8.5.'







  print('Saving')
  ds.to_netcdf('/archive/depfg/graha010/Analysis_Of_Nutrients/Combined_FUTURE_' + SSP + '_Hybrid_Pconc_WithMB.nc')
  print('Saved')









