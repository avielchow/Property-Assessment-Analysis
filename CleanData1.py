import pandas as pd
import numpy as np
import scipy.stats as stats
import pylab as pl
import re
import seaborn as sns


pd.set_option('display.max_columns', 15)
pd.set_option('display.max_rows', 40)


columns = ['Lot Size', 'Assessment Year','Garage','Neighbourhood','Assessed Value', 'Assessment Class', 'Actual Year Built','Zoning', 'Legal Description']
filepath = 'Coding\\DataAnalystInterview\\AssessmentData.csv'

'''Reduces size from 255mb to 11mb converting datatypes and dropping columns'''
Data = pd.read_csv(filepath, usecols = columns, header = 0, sep = ',')

Data = Data.dropna()
Data.rename(columns = {'Assessed Value':'Assessed_Value','Assessment Class':'Assessment_Class','Actual Year Built':'Actual_Year_Built','Lot Size':'Lot_Size'}, inplace=True)

Data['Assessed_Value'] = Data.Assessed_Value.str.replace(',','').astype('float').astype('int32')
Data['Lot_Size'] = Data.Lot_Size.str.replace(',','').astype('float').astype('int32')


''' RenamedNeighbourhoods = new or renamed neighborhoods with no assessments in any year from 2012 - 2018'''

Data2019 = Data[Data['Assessment Year'] == 2018]
ResidentialData = Data2019[Data2019['Assessment_Class'] == 'Residential']
del ResidentialData['Assessment_Class']
del ResidentialData['Assessment Year']


ResidentialData['Garage'] = ResidentialData['Garage'].astype('category')
ResidentialData['Neighbourhood'] = ResidentialData['Neighbourhood'].astype('category')
ResidentialData['Zoning'] = ResidentialData['Zoning'].astype('category')
ResidentialData['Actual_Year_Built'] = ResidentialData['Actual_Year_Built'].astype('category')

ResidentialData['PricePerSquareMeter'] = ResidentialData['Assessed_Value']/ResidentialData['Lot_Size']

ResidentialData = ResidentialData[ResidentialData['Assessed_Value'] > 50000]
ResidentialData = ResidentialData[ResidentialData['Assessed_Value'] < 1500000]

ResidentialDataCondo = ResidentialData[ResidentialData['Legal Description'].str.contains('Unit')]
ResidentialDataHouse = ResidentialData[~ResidentialData['Legal Description'].str.contains('Unit')]

del ResidentialDataCondo['Legal Description']
del ResidentialDataHouse['Legal Description']

ResidentialDataHouse.to_csv(r'\\Coding\\DataAnalystInterview\\MarketValue\\ResidentialHouse2019Data.csv', index = False)
ResidentialDataCondo.to_csv(r'\\Coding\\DataAnalystInterview\\MarketValue\\ResidentialCondo2019Data.csv', index = False)

'''
sns.boxplot(x = ResidentialData['Assessed_Value'].values.tolist())
Distribution = ResidentialData['Assessed_Value'].quantile([0.1, 0.25, 0.75, 0.9, 1])
print(Distribution)
'''