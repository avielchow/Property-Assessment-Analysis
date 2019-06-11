import pandas as pd
import numpy as np
import scipy.stats as stats
import pylab as pl
import re
import seaborn as sns
import matplotlib.pyplot as plt
import random

sns.set(font_scale = 1.5)

pd.set_option('display.max_columns', 15)
pd.set_option('display.max_rows', 40)

filepath = '\\Coding\\DataAnalystInterview\\MarketValue\\ResidentialHouse2019Data.csv'
filepath1 = '\\Coding\\DataAnalystInterview\\MarketValue\\ResidentialCondo2019Data.csv'
DataHouse = pd.read_csv(filepath, header = 0, sep = ',')
DataCondo = pd.read_csv(filepath1,header=0,sep=',')

filepath2 = '\\Coding\\DataAnalystInterview\\Neighbourhoods.csv'
Neighbourhoods = pd.read_csv(filepath2, header = None, sep = ',')
Interquartile = Neighbourhoods[Neighbourhoods[1] > 1.5*(10**8)]
Interquartile = Interquartile[Interquartile[1] < 6*(10**8)]
Interquartile = Interquartile[0].tolist()
Interquartilesample = random.choices(Interquartile, k=5)
print (Interquartilesample)


#Lotsize vs assesed value without removing outliers. Determined Condo v. House using "unit" in legal description

plt.figure()
#sns.scatterplot(x='Lot_Size',y='Assessed_Value',data=DataHouse)

plt.figure()
#sns.scatterplot(x='Lot_Size',y='Assessed_Value',data=DataCondo)

'''Removing lot size outliers/Year Built Outliers'''

DataHouse = pd.read_csv(filepath, header = 0, sep = ',')
DistributionHouse = (DataHouse['Lot_Size'].quantile([0.1, 0.25, 0.75, 1]))
(tophouse,bottomhouse) = 623 +((623-394) * 1.5), 394 - ((623-394) * 1.5)

test = (DataHouse['Assessed_Value'].quantile([0.1, 0.25, 0.75, 1]))
print(test)

DataHouse = DataHouse[DataHouse['Lot_Size'] > bottomhouse]
DataHouse = DataHouse[DataHouse['Lot_Size'] < tophouse]
DataHouse = DataHouse[DataHouse['Actual_Year_Built'] > 1600]

DataHouseNeighbourhood = DataHouse[DataHouse['Neighbourhood'].isin(Interquartilesample)]

'''HOUSES Lot Size vs. Assessed Value'''

plt.figure()
sns.lmplot(x='Lot_Size',y='Assessed_Value', hue = 'Neighbourhood',data=DataHouseNeighbourhood, height = 10)
plt.ylim(0,)
plt.xlim(0,)
#P-Value is the test that the hypothesis is Null (slope = 0) R-Value is the correlation. This gives a weak R and a strong P
slope, intercept, r_value, p_value, std_err = stats.linregress(DataHouseNeighbourhood['Lot_Size'],DataHouseNeighbourhood['Assessed_Value'])
print ('DataNeighborhood : lotsize v. assessed value', slope, intercept, r_value, p_value, std_err)

plt.figure()
sns.lmplot(x='Lot_Size',y='Assessed_Value',data=DataHouse, height = 10)
#P-Value is the test that the hypothesis is Null (slope = 0) R-Value is the correlation. This gives a weak R and a strong P
slope, intercept, r_value, p_value, std_err = stats.linregress(DataHouse['Lot_Size'],DataHouse['Assessed_Value'])
print ('DataHouse: lotsize v. assessed value', slope, intercept, r_value, p_value, std_err)


'''Economies of Scale, Lot Size vs. PPSF'''
plt.figure()
slope, intercept, r_value, p_value, std_err = stats.linregress(DataHouseNeighbourhood['Lot_Size'],DataHouseNeighbourhood['PricePerSquareMeter'])
print ('DataNeighborhood: Economies of Scale', slope, intercept, r_value, p_value, std_err)
sns.lmplot(x='Lot_Size',y='PricePerSquareMeter', hue = 'Neighbourhood', height = 10, data=DataHouseNeighbourhood)

plt.figure()
sns.lmplot(x='Lot_Size',y='PricePerSquareMeter',data=DataHouse, height = 10)
plt.ylim(0,)
plt.xlim(0,)
#P-Value is the test that the hypothesis is Null (slope = 0) R-Value is the correlation. This gives a weak R and a strong P
slope, intercept, r_value, p_value, std_err = stats.linregress(DataHouse['Lot_Size'],DataHouse['PricePerSquareMeter'])
print ('DataHouse: Economies of Scale', slope, intercept, r_value, p_value, std_err)

''' Year Built '''
plt.figure()
sns.lmplot(x='Actual_Year_Built',y='Assessed_Value',hue = 'Neighbourhood', height = 10, data=DataHouseNeighbourhood)
plt.ylim(0,)
plt.xlim(1940,2020)
slope, intercept, r_value, p_value, std_err = stats.linregress(DataHouseNeighbourhood['Actual_Year_Built'],DataHouseNeighbourhood['Assessed_Value'])
print ('DataNeighborhood: Actual Year Built', slope, intercept, r_value, p_value, std_err)

plt.figure()
sns.lmplot(x='Actual_Year_Built',y='Assessed_Value', data = DataHouse, height = 10)
plt.ylim(0,)
plt.xlim(1940,2020)
#P-Value is the test that the hypothesis is Null (slope = 0) R-Value is the correlation. This gives a weak R and a strong P
slope, intercept, r_value, p_value, std_err = stats.linregress(DataHouse['Actual_Year_Built'],DataHouse['Assessed_Value'])
print ('DataHouse: Actual Year Built', slope, intercept, r_value, p_value, std_err)

plt.figure()
sns.lmplot(x='Actual_Year_Built',y='Lot_Size', data = DataHouse, height = 10)
plt.ylim(0,)
plt.xlim(1940,2020)
#P-Value is the test that the hypothesis is Null (slope = 0) R-Value is the correlation. This gives a weak R and a strong P
slope, intercept, r_value, p_value, std_err = stats.linregress(DataHouse['Actual_Year_Built'],DataHouse['Lot_Size'])
print ('DataHouse: Actual Year Built', slope, intercept, r_value, p_value, std_err)
'''Neighbourhood Group'''

DataHouseNeighbourhood.boxplot('Assessed_Value','Neighbourhood',figsize=(27,8))

'''
dummy = pd.get_dummies(DataHouse['Neighbourhood'])
print(dummy.head())
dummy.to_csv(r'C:\\Users\\aviel\\Desktop\\Coding\\Data Analyst Interview\\MarketValue\\test.csv', index = False)
'''



