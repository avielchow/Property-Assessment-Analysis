import pandas as pd
import numpy as np
import scipy.stats as stats
import pylab as pl
import re
import seaborn as sns


pd.set_option('display.max_columns', 15)
pd.set_option('display.max_rows', 40)

column_types = {
 'Account Number':'int32',
 'Assessment Year': 'int16',
 'Neighbourhood': 'category',
 'Assessed Value':'object'
}

columns = ['Account Number','Assessment Year','Neighbourhood','Assessed Value']
filepath = '\\Coding\\DataAnalystInterview\\AssessmentData.csv'

'''Reduces size from 255mb to ~30mb by converting datatypes and dropping columns'''
Data = pd.read_csv(filepath, usecols = columns, dtype = column_types, header = 0, sep = ',')
Data.rename(columns = {'Assessed Value':'Assessed_Value'}, inplace=True)
Data['Assessed_Value'] = Data.Assessed_Value.str.replace(',','').astype('float').astype('int32')

'''Pivot Table - Neighborhood vs sum of assessments by year'''

NeighbourhoodTable = pd.pivot_table(Data, index = "Neighbourhood", columns = "Assessment Year", values = "Assessed_Value", aggfunc = [np.sum], fill_value = 0)

''' RenamedNeighbourhoods = new or renamed neighborhoods with no assessments in any year from 2012 - 2018'''

RenamedNeighbourhoods = (NeighbourhoodTable[NeighbourhoodTable['sum'].all(axis=1) != True])
NeighbourhoodTable = (NeighbourhoodTable[NeighbourhoodTable['sum'].all(axis=1) != False])

#Reviewed Renamed Neighbourhoods to determine areas that would affect results. These are renamed areas that have high impact missing data
'''Magrath Heights Area - 254848500 in 2012 to Magrath Heights'''
'''Terwillegar South - 1145614500 to 2012 to South Terwillegar'''

NeighbourhoodTable.loc['MAGRATH HEIGHTS', ('sum', 2012)] += 254848500
NeighbourhoodTable.loc['SOUTH TERWILLEGAR', ('sum', 2012)] += 1145614500

'''Table by Percentage Change'''

NeighbourhoodTableChange = NeighbourhoodTable.pct_change(axis=1)
NeighbourhoodTableChange.columns = NeighbourhoodTableChange.columns.droplevel()
del NeighbourhoodTableChange.index.name
del NeighbourhoodTableChange[2012]
NeighbourhoodTableChange.columns = ['2012-2013','2013-2014', '2014-2015', '2015-2016', '2016-2017', '2017-2018']

'''Changes to Neighbourhood Table'''
NeighbourhoodTable = NeighbourhoodTable.xs('sum', axis = 1)
del NeighbourhoodTable.index.name
del NeighbourhoodTable.columns.name


#Sum the Total % Change. Decided not to take the absolute value of change because 5 years increasing steadily is
#very different from 5 years increasing and decreasing but ending in the same place. Check for variation at the end

NeighbourhoodTableChange['Total % Change'] = NeighbourhoodTableChange.sum(axis=1)

NeighbourhoodTableChange = NeighbourhoodTableChange.sort_values(by='Total % Change')
Neighbourhoods = NeighbourhoodTable.mean(axis=1).astype(int)


#NeighbourhoodTable: Table with Raw Assessment Values and Sum of all Assessment Values for Neighbourhoods with data from 2012-2018
NeighbourhoodTable.to_csv(r'\\Coding\\DataAnalystInterview\\NeighbourhoodAssessments.csv')

#RenamedNeighbourhoodsL: Table with Raw Assessment Values of Neighbourhoods with missing 2012 - 2018 data
RenamedNeighbourhoods.to_csv(r'\\Coding\\DataAnalystInterview\\RenamedNeighbourhoods.csv')

#NeighbourhoodTableChange: Table with %Change in all years with data and Standard Deviation
NeighbourhoodTableChange.to_csv(r'\\Coding\\DataAnalystInterview\\NeighbourhoodTableChange.csv')

#Neighbourhoods: Table with Average Assessments from 2012-2018 in each Neighborhood to segment the analysis
Neighbourhoods.to_csv(r'\\Coding\\DataAnalystInterview\\Neighbourhoods.csv')






'''print (NeighbourhoodTable.info())'''
'''print (NeighbourhoodTable)'''
'''print (NeighbourhoodTable.std(axis=1))'''
'''print (Data.loc[Data['Neighbourhood'] == 'MACTAGGART AREA'])'''
'''print (set(Data['Neighbourhood']))'''
'''RenamedNeighbourhoods = (NeighbourhoodTable['sum'][:] != 0).all(axis=1).dropna()'''
#NeighbourhoodTable.to_csv(r'C:\Users\aviel\Desktop\Coding\Data Analyst Interview\NeighbourhoodAssessments.csv')
#RenamedNeighbourhoods.to_csv(r'C:\Users\aviel\Desktop\Coding\Data Analyst Interview\RenamedNeighbourhoods.csv')




