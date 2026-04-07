


import pandas as pd
import numpy as np 
import netCDF4 as nc




## Hydrology
hydrology_monthly = nc.Dataset('/archive/depfg/graha010/duncan_copied/hist-hydrology_monthly_variable_1970_2010.nc')


time = hydrology_monthly['time']
#print(time.shape)
#print(time[0])
#print(time[491])

lat_all = pd.DataFrame(hydrology_monthly['lat'][:],columns=['Lat'])
lon_all = pd.DataFrame(hydrology_monthly['lon'][:],columns=['Lon'])

test = pd.DataFrame(hydrology_monthly['discharge'][0,:,:])
lat_copy = pd.DataFrame(hydrology_monthly['lat'][:])
lon_copy = pd.DataFrame(hydrology_monthly['lon'][:])
lat_copy = pd.concat([lat_copy]*len(test.columns), axis=1, ignore_index=True)
lon_copy = lon_copy.T
lon_copy = pd.concat([lon_copy]*len(test), axis=0, ignore_index=True)
#print(lat_copy)
#print(lon_copy)

test_2 = hydrology_monthly['discharge'][:,:,:]
    
    

discharge = hydrology_monthly['discharge'][:,:,:]
watertemperature = hydrology_monthly['watertemperature'][:,:,:]
precipitation = hydrology_monthly['precipitation'][:,:,:]



## Monitoring data
observations_tp = pd.read_csv('/archive/depfg/graha010/Analysis_Of_Nutrients/monthly_phosphorus.csv',sep=';')
observations_tp['YrMth'] = observations_tp['Day'].str[2:7]
data_lat = pd.DataFrame(observations_tp['Lat']).drop_duplicates().reset_index(drop=True)
data_lon = pd.DataFrame(observations_tp['Lon']).drop_duplicates().reset_index(drop=True)




dates = pd.date_range('1970-01-01','2010-12-01', freq='MS').strftime("%y-%m").tolist()
dates = pd.DataFrame(dates,columns=['YrMth'])
#print(dates.shape)
#print(dates.iloc[0])
#print(dates.iloc[491])
dates['YrMth_indexed'] = dates.index



observations_tp = observations_tp.merge(dates,how='left',on=['YrMth'])
observations_tp = observations_tp.dropna()
observations_tp = observations_tp.reset_index(drop=True)
observations_tp['YrMth_indexed'] = observations_tp['YrMth_indexed'].astype(int)




data_lat_new = pd.DataFrame()
for ii in range(0,len(data_lat)):
  value = data_lat.iloc[ii]
  compare = abs(pd.DataFrame(lat_all['Lat']) - value)
  minimum = compare.idxmin()
  new_value = lat_all.iloc[minimum]
  data_lat_new = pd.concat([data_lat_new,new_value])
  #print(ii)
data_lat_new = data_lat_new.reset_index(drop=True)



data_lat['Lat_converted'] = data_lat_new



data_lon_new = pd.DataFrame()
for ii in range(0,len(data_lon)):
  value = data_lon.iloc[ii]
  compare = abs(pd.DataFrame(lon_all['Lon']) - value)
  minimum = compare.idxmin()
  new_value = lon_all.iloc[minimum]
  data_lon_new = pd.concat([data_lon_new,new_value])
  #print(ii)
data_lon_new = data_lon_new.reset_index(drop=True)



data_lon['Lon_converted'] = data_lon_new


#print(observations_tp)
observations_tp = observations_tp.merge(data_lat,how='left',on=['Lat'])
observations_tp = observations_tp.merge(data_lon,how='left',on=['Lon'])
#print(observations_tp)





observations_MERGED_ALL = pd.DataFrame()

for jj in range(0,test_2.shape[0]):
  
  extract_q = discharge[jj,:,:]
  extract_tw = watertemperature[jj,:,:]
  extract_precip = precipitation[jj,:,:]
  
  extract_lat = lat_copy
  extract_lon = lon_copy
  
  extract_q = np.reshape(extract_q,extract_q.shape[0]*extract_q.shape[1])
  extract_tw = np.reshape(extract_tw,extract_tw.shape[0]*extract_tw.shape[1])
  extract_precip = np.reshape(extract_precip,extract_precip.shape[0]*extract_precip.shape[1])
  extract_lat = np.reshape(extract_lat,extract_lat.shape[0]*extract_lat.shape[1])
  extract_lon = np.reshape(extract_lon,extract_lon.shape[0]*extract_lon.shape[1])
  
  extract_q = pd.DataFrame(extract_q,columns=['q'])
  extract_tw = pd.DataFrame(extract_tw,columns=['tw'])
  extract_precip = pd.DataFrame(extract_precip,columns=['precip'])
  extract_lat = pd.DataFrame(extract_lat,columns=['Lat_converted'])
  extract_lon = pd.DataFrame(extract_lon,columns=['Lon_converted'])
  
  extract_all = pd.concat([extract_q,extract_tw,extract_precip,extract_lat,extract_lon],axis=1)
  extract_all['YrMth_indexed'] = jj
  extract_all = extract_all.dropna()
  extract_all = extract_all.reset_index(drop=True)
  
  observations_MERGED = observations_tp.merge(extract_all,on=['Lat_converted','Lon_converted','YrMth_indexed'],how='left')
  observations_MERGED = observations_MERGED.dropna()
  observations_MERGED_ALL = pd.concat([observations_MERGED_ALL, observations_MERGED])
  
  print(jj)

print(observations_MERGED_ALL)











## NOW INCLUDING THE ANNUAL PHOSPHORUS
phosphorus = nc.Dataset('/archive/depfg/graha010/duncan_copied/Output-IMAGE_GNM-SSP2_oct2020-Phosphorus_Rivers_Pconc-v2.nc')
#print(phosphorus['time'])
#print(phosphorus['time'].shape)
#print(phosphorus['time'][0])
phosphorus = phosphorus['Pconc'][:,:,:]

observations_MERGED_ALL['Year'] = observations_MERGED_ALL['Day'].str[0:4].astype(int)
tmp = pd.DataFrame(range(1980,2011),columns=['Year'])
tmp['Year_indexed'] = tmp.index
#print(tmp)
#print(tmp.shape)

#print(observations_tp)
observations_MERGED_ALL = observations_MERGED_ALL.merge(tmp,how='left',on=['Year'])
observations_MERGED_ALL['Year_indexed'] = observations_MERGED_ALL['Year_indexed'].astype(int)
#print(observations_tp)








y = pd.DataFrame()

for ii in range(0,phosphorus.shape[0]):
  
  extract_phos = phosphorus[ii,:,:]
  
  extract_lat = lat_copy
  extract_lon = lon_copy
  
  extract_phos = np.reshape(extract_phos,extract_phos.shape[0]*extract_phos.shape[1])
  extract_lat = np.reshape(extract_lat,extract_lat.shape[0]*extract_lat.shape[1])
  extract_lon = np.reshape(extract_lon,extract_lon.shape[0]*extract_lon.shape[1])
  
  extract_phos = pd.DataFrame(extract_phos,columns=['phos'])
  extract_lat = pd.DataFrame(extract_lat,columns=['Lat_converted'])
  extract_lon = pd.DataFrame(extract_lon,columns=['Lon_converted'])
  
  extract_all = pd.concat([extract_phos,extract_lat,extract_lon],axis=1)
  extract_all['Year_indexed'] = ii
  extract_all = extract_all.dropna()
  extract_all = extract_all.reset_index(drop=True)
  
  x = observations_MERGED_ALL.merge(extract_all,on=['Lat_converted','Lon_converted','Year_indexed'],how='left')
  x = x.dropna()
  y = pd.concat([y, x])
  
  print(ii)

print(y)


y.to_csv('/archive/depfg/graha010/Analysis_Of_Nutrients/Training_Phos.csv',sep=';',index=False)

print('saved')







