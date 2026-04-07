

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


# You can check these against scripts 3rd, 6th, 7th, 8th, 9th, 10th


for scenario in ['SSP1','SSP2','SSP3','SSP4','SSP5']:


  if scenario == 'SSP1':
    hydrology_monthly = nc.Dataset('/archive/depfg/graha010/duncan_copied_scenarios/rcp4.5-hydrology_monthly_variable_2016_2099.nc')
  elif scenario == 'SSP2':
    hydrology_monthly = nc.Dataset('/archive/depfg/graha010/duncan_copied_future/rcp6.0-hydrology_monthly_variable_2016_2099.nc')
  elif scenario == 'SSP3':
    hydrology_monthly = nc.Dataset('/archive/depfg/graha010/duncan_copied_future/rcp6.0-hydrology_monthly_variable_2016_2099.nc')
  elif scenario == 'SSP4':
    hydrology_monthly = nc.Dataset('/archive/depfg/graha010/duncan_copied_future/rcp6.0-hydrology_monthly_variable_2016_2099.nc')
  elif scenario == 'SSP5':
    hydrology_monthly = nc.Dataset('/archive/depfg/graha010/duncan_copied_scenarios/rcp8.5-hydrology_monthly_variable_2016_2099.nc')
  discharge = hydrology_monthly['discharge']
  discharge = discharge[:,:,:]
  print(discharge.shape)
  discharge = discharge*1000000000000/12

  hybrid_tp = nc.Dataset('/archive/depfg/graha010/Analysis_Of_Nutrients/FUTURE_' + scenario + '_Hybrid_TP.nc')
  hybrid_tp = hybrid_tp['Hybrid_TP'][:,:,:]
  print(hybrid_tp.shape)


  monthly_load = hybrid_tp*discharge






  print(monthly_load.shape)
  print(np.nanmean(np.nanmean(monthly_load[0,:,:])))
  #exit()




  # Get annual discharge
  empty = []
  for ii in range(0,discharge.shape[0],12):
    extract = discharge[ii:ii+12,:,:]
    extract = np.nansum(extract,axis=0)
    empty.append(extract)
    print(ii)
  
  
  print(np.nanmean(np.nanmean(empty[0])))
  #exit()
  
  
  
  # Get annual phos
  if scenario == 'SSP1':
    phosphorus = nc.Dataset('/archive/depfg/graha010/duncan_copied_scenarios/Output-IMAGE_GNM-SSP1_oct2020_yearly-Phosphorus_Rivers_Pconc-v2.nc')
  elif scenario == 'SSP2':
    phosphorus = nc.Dataset('/archive/depfg/graha010/duncan_copied_future/Output-IMAGE_GNM-SSP2_oct2020_year-Phosphorus_Rivers_Pconc-v2.nc')
  elif scenario == 'SSP3':
    phosphorus = nc.Dataset('/archive/depfg/graha010/duncan_copied_scenarios/Output-IMAGE_GNM-SSP3_oct2020_yearly-Phosphorus_Rivers_Pconc-v2.nc')
  elif scenario == 'SSP4':
    phosphorus = nc.Dataset('/archive/depfg/graha010/duncan_copied_scenarios/Output-IMAGE_GNM-SSP4_oct2020_yearly-Phosphorus_Rivers_Pconc-v2.nc')
  elif scenario == 'SSP5':
    phosphorus = nc.Dataset('/archive/depfg/graha010/duncan_copied_scenarios/Output-IMAGE_GNM-SSP5_oct2020_yearly-Phosphorus_Rivers_Pconc-v2.nc')
  ds_4 = phosphorus['Pconc'][46:-1,:,:]
  print(np.nanmean(np.nanmean(ds_4[0,:,:])))
  #exit()


  # Get yearly load (actual)
  yearly_actual = []
  for jj in range(0,ds_4.shape[0]):
    yearly_load = ds_4[jj,:,:] * empty[jj]
    yearly_actual.append(yearly_load)
    print(jj)
  

  print(np.nanmean(np.nanmean(yearly_actual[0])))
  #exit()
  
  # Get year load (estimated)
  yearly_estimated = []
  for kk in range(0,monthly_load.shape[0],12):
    part_of_data = monthly_load[kk:kk+12,:,:]
    part_of_data = np.nansum(part_of_data,axis=0)
    yearly_estimated.append(part_of_data)
    print(kk)
  
  
  print(np.nanmean(np.nanmean(yearly_estimated[0])))
  #exit()

  #check = yearly_actual[0]
  #check_2 = yearly_estimated[0]
  #print(np.nansum(check > 0))


  print(len(yearly_actual))
  print(len(yearly_estimated))


  all_values = []
  for ll in range(0,len(yearly_actual)):

    actual = yearly_actual[ll]
    estimated = yearly_estimated[ll]
  
    correction_factor = actual/estimated
  
    all_values.append(correction_factor)
  


  print(np.nanmean(np.nanmean(all_values[0])))


  all_project = []
  for mm in range(0,len(all_values)):
    new_extract = all_values[mm]
    project = np.tile(new_extract,(12,1,1))
    all_project.append(project)
  
  all_project = np.concatenate(all_project,axis=0)



  print(monthly_load.shape)
  print(all_project.shape)


  corrected_load = monthly_load*all_project


  print(np.nanmean(np.nanmean(monthly_load[0,:,:])))
  print(np.nanmean(np.nanmean(corrected_load[0,:,:])))





  corrected_concentration = corrected_load / discharge



  #check = corrected_concentration[0,:,:]
  #check_2 = hybrid_tp[0,:,:]
















  ## Also store the lat/lon
  if scenario == 'SSP1':
    misc = nc.Dataset('/archive/depfg/graha010/duncan_copied_scenarios/rcp4.5-hydrology_monthly_variable_2016_2099.nc')
  elif scenario == 'SSP2':
    misc = nc.Dataset('/archive/depfg/graha010/duncan_copied_future/rcp6.0-hydrology_monthly_variable_2016_2099.nc')
  elif scenario == 'SSP3':
    misc = nc.Dataset('/archive/depfg/graha010/duncan_copied_future/rcp6.0-hydrology_monthly_variable_2016_2099.nc')
  elif scenario == 'SSP4':
    misc = nc.Dataset('/archive/depfg/graha010/duncan_copied_future/rcp6.0-hydrology_monthly_variable_2016_2099.nc')
  elif scenario == 'SSP5':
    misc = nc.Dataset('/archive/depfg/graha010/duncan_copied_scenarios/rcp8.5-hydrology_monthly_variable_2016_2099.nc')
  time = misc['time'][:]
  lat = misc['lat'][:]
  lon = misc['lon'][:]





  data = xarray.DataArray(corrected_concentration, coords=[('time', time), ('lat', lat), ('lon', lon)], name='HybTP_MB')
  
  data.attrs['name'] = 'Total Phosphorus (IMAGE-GNM with Random Forest and Mass Balance)'
  data.attrs['units'] = 'mg/l'
  data.time.attrs['name'] = 'time'
  data.time.attrs['units'] = 'days since 1800-01-01'
  data.lat.attrs['name'] = 'latitude'
  data.lat.attrs['units'] = 'degrees_north'
  data.lon.attrs['name'] = 'longitude'
  data.lon.attrs['units'] = 'degrees_east'

  print('Saving')
  data.to_netcdf('/archive/depfg/graha010/Analysis_Of_Nutrients/FUTURE_' + scenario + '_Hybrid_TP_WithMB.nc')
  print('Saved')





















