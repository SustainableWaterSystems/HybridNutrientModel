


import netCDF4 as nc
import numpy as np
import pandas as pd 
from sklearn.ensemble import RandomForestRegressor
import joblib
from datetime import datetime
import xarray


for scenario in ['SSP1','SSP2','SSP3','SSP4','SSP5']:


  ## Load the random forest 
  model = joblib.load("/archive/depfg/graha010/Analysis_Of_Nutrients/ML_model_tn.joblib")


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



  # discharge 
  ds_1 = hydrology_monthly['discharge'][:,:,:]

  # watertemperature    
  ds_2 = hydrology_monthly['watertemperature'][:,:,:]

  # precipitation
  ds_3 = hydrology_monthly['precipitation'][:,:,:]

  # annual nitro
  if scenario == 'SSP1':
    nitrogen = nc.Dataset('/archive/depfg/graha010/duncan_copied_scenarios/Output-IMAGE_GNM-SSP1_oct2020_yearly-Nitrogen_Rivers_Nconc-v2.nc')
  elif scenario == 'SSP2':
    nitrogen = nc.Dataset('/archive/depfg/graha010/duncan_copied_future/Output-IMAGE_GNM-SSP2_oct2020_year-Nitrogen_Rivers_Nconc-v2.nc')
  elif scenario == 'SSP3':
    nitrogen = nc.Dataset('/archive/depfg/graha010/duncan_copied_scenarios/Output-IMAGE_GNM-SSP3_oct2020_yearly-Nitrogen_Rivers_Nconc-v2.nc')
  elif scenario == 'SSP4':
    nitrogen = nc.Dataset('/archive/depfg/graha010/duncan_copied_scenarios/Output-IMAGE_GNM-SSP4_oct2020_yearly-Nitrogen_Rivers_Nconc-v2.nc')
  elif scenario == 'SSP5':
    nitrogen = nc.Dataset('/archive/depfg/graha010/duncan_copied_scenarios/Output-IMAGE_GNM-SSP5_oct2020_yearly-Nitrogen_Rivers_Nconc-v2.nc')
  ds_4 = nitrogen['Nconc'][46:-1,:,:]



  ## Repeat each annual slice 12x
  project_ALL = []
  for kk in range(0,ds_4.shape[0]):
    project = np.tile(ds_4[kk,:,:],(12,1,1))
    project_ALL.append(project)
    print(kk)
  project_ALL = np.concatenate(project_ALL,axis=0)



  
  shape_store_0 = ds_1.shape[0]
  shape_store_1 = ds_1.shape[1]
  shape_store_2 = ds_1.shape[2]


  ## Update phosphorus 
  hybrid_all = np.empty([shape_store_0,shape_store_1,shape_store_2],dtype=float)
  
  for ii in range(0,shape_store_0):      

    DISCHARGE = ds_1[ii,:,:]
    WATERTEMP = ds_2[ii,:,:]
    PRECIP = ds_3[ii,:,:]
    ANNUAL_NITRO = project_ALL[ii,:,:]
    
    DISCHARGE = np.reshape(DISCHARGE, shape_store_1*shape_store_2)
    WATERTEMP = np.reshape(WATERTEMP, shape_store_1*shape_store_2)
    PRECIP = np.reshape(PRECIP, shape_store_1*shape_store_2)
    ANNUAL_NITRO = np.reshape(ANNUAL_NITRO, shape_store_1*shape_store_2)
  
    DISCHARGE = np.nan_to_num(DISCHARGE)
    WATERTEMP = np.nan_to_num(WATERTEMP)
    PRECIP = np.nan_to_num(PRECIP)
    ANNUAL_NITRO = np.nan_to_num(ANNUAL_NITRO)

    # Correct order
    X = np.c_[DISCHARGE,WATERTEMP,PRECIP,ANNUAL_NITRO]

    predicted = model.predict(X)
    hybrid_TN = predicted
    hybrid_TN = np.reshape(hybrid_TN,(shape_store_1,shape_store_2))

    hybrid_all[ii,:,:] = hybrid_TN
    print(ii)
    
  



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





  data = xarray.DataArray(hybrid_all, coords=[('time', time), ('lat', lat), ('lon', lon)], name='Hybrid_TN')
  
  data.attrs['name'] = 'Total Nitrogen (IMAGE-GNM with Random Forest)'
  data.attrs['units'] = 'mg/l'
  data.time.attrs['name'] = 'time'
  data.time.attrs['units'] = 'days since 1800-01-01'
  data.lat.attrs['name'] = 'latitude'
  data.lat.attrs['units'] = 'degrees_north'
  data.lon.attrs['name'] = 'longitude'
  data.lon.attrs['units'] = 'degrees_east'

  data.to_netcdf('/archive/depfg/graha010/Analysis_Of_Nutrients/FUTURE_' + scenario + '_Hybrid_TN.nc')


  print('Note: First attempt at future hybrid TN, nice, great')


