





import netCDF4 as nc
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from dateutil.relativedelta import *
from sklearn.ensemble import RandomForestRegressor
import joblib
from datetime import datetime
from sklearn.model_selection import train_test_split
import geopandas as gpd
from shapely.geometry import Point




## Load the training data ##

data_all = pd.read_csv('/archive/depfg/graha010/Analysis_Of_Nutrients/Training_Phos.csv',sep=';')





## NOTE (Screening the uppermost anomalies):
print('Incorporating percentile process')
data_all = data_all.loc[data_all['Value'] < data_all['Value'].quantile(0.995)] 
print('Percentile process confirmed')


print(data_all['phos'].min())
print(data_all['phos'].max())
print(data_all['Value'].min())
print(data_all['Value'].max())







## Check the length of the data at this point         
data_all = data_all.dropna()
print('The length of data_all here is ' + str(len(data_all)))



## Extract samples for machine learning ##
X = data_all[['q','tw','precip','phos','Lat','Lon','Day','Station']]
y = data_all['Value']


print(X)
print(y)

gdf = gpd.read_file('/archive/depfg/graha010/Basins/Basins_Global.shp')

locations = X[['Lat','Lon']]
locations = locations.drop_duplicates()

geometry = [Point(xy) for xy in zip(locations['Lon'], locations['Lat'])]
points_gdf = gpd.GeoDataFrame(locations,geometry=geometry)
points_gdf.set_crs(gdf.crs,inplace=True)
joined = gpd.sjoin(points_gdf, gdf[['HYBAS_ID','geometry']],how='left',predicate='intersects')
result = joined[['Lat','Lon','HYBAS_ID']]
X = X.merge(result,on=['Lat','Lon'],how='left')
X['Decade'] = X['Day'].str[0:3]
X['Decade'].loc[X['Decade'] == '201'] = '200'
X['Decade'] = X['Decade'].astype(str)
print(X)
print(y)


X['HYBAS_ID'] = X['HYBAS_ID'].fillna('Unknown')
strat_columns = ['HYBAS_ID','Decade']
valid_ids = X[strat_columns].value_counts()
valid_ids = valid_ids[valid_ids >= 2].index
valid_mask = X.set_index(strat_columns).index.isin(valid_ids)

X = X.reset_index(drop=True)
y = y.reset_index(drop=True)
X = X[valid_mask]
y = y[valid_mask]
print(X)
print(y)


#X = np.array(X)
#y = np.array(y)

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=X[['HYBAS_ID','Decade']])





## Another check
print('Number of training points is ' + str(len(x_train)))



## Train the model using xtrain[:,0:4] and y_train ##
print('Training started')
print(datetime.now())
model = RandomForestRegressor()
model.fit(x_train.iloc[:,0:4],y_train)
joblib.dump(model,'/archive/depfg/graha010/Analysis_Of_Nutrients/ML_model_tp.joblib')
print('Training finished')
print(datetime.now())




## Predict the residuals and save
x_test = pd.DataFrame(x_test,columns=['q','tw','precip','phos','Lat','Lon','Day','Station'])
x_test = x_test.reset_index(drop=True)

discharge = np.array(x_test['q'])
waterTemp = np.array(x_test['tw'])
precip = np.array(x_test['precip'])
phos = np.array(x_test['phos'])


print('Predicting started')
print(datetime.now())
predicted = model.predict(np.c_[discharge,waterTemp,precip,phos])
print('Predicting finished')
print(datetime.now())

  
x_test['MonthlyTP'] = predicted
x_test.to_csv('/archive/depfg/graha010/Analysis_Of_Nutrients/phos_testing_sample.csv',index=False)


#x_train = pd.DataFrame(x_train,columns=['q','tw','precip','phos','Lat','Lon','Day','Station'])
#x_train.to_csv('/archive/depfg/graha010/Analysis_Of_Nutrients/phos_training_sample.csv',index=False)


y_test = pd.DataFrame(y_test,columns=['Value'])
y_test.to_csv('/archive/depfg/graha010/Analysis_Of_Nutrients/phos_Y_testing_sample.csv',index=False)







