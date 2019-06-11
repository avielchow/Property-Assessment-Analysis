import pandas as pd
import numpy as np
from scipy import stats
import pylab as pl
import seaborn as sns
import matplotlib.pyplot as plt

'''Magrath Heights Area - 254848500 in 2012 to Magrath Heights'''
'''Terwillegar South - 1145614500 to 2012 to South Terwillegar'''

def calc_slope(row):
    a = stats.linregress(x=[1,2,3,4,5,6,7], y=row)
    return a.slope



filepath = '\\Coding\\DataAnalystInterview\\Neighbourhoods.csv'
Neighbourhoods = pd.read_csv(filepath, header = None, sep = ',')

filepath1 = '\\Coding\\DataAnalystInterview\\NeighbourhoodTableChange.csv'
NeighbourhoodTableChange = pd.read_csv(filepath1, index_col = 0, header = 0, sep = ',')

filepath2 = '\\Coding\\DataAnalystInterview\\NeighbourhoodAssessments.csv'
NeighbourhoodTable = pd.read_csv(filepath2, index_col = 0, header = 0, sep = ',')


'''Which Neighbourhoods Matter?'''

#Box Plot - Distribution Check
sns.boxplot(x = Neighbourhoods[1].values.tolist())

#Which Quantiles to consider - 0.1 to 0.2, 0.2 - 0.9, 0.9-1.0
#~150 million - 500 million, 500 million - 2 billion

Distribution = (Neighbourhoods.quantile([0.25, 0.75, 1]))

'''Interquartile Neighbourhoods by lowest Percent Change'''
#"Interquartile" closer to 20% - 85%
Interquartile = Neighbourhoods[Neighbourhoods[1] > 1.5*(10**8)]
Interquartile = Interquartile[Interquartile[1] < 6*(10**8)]
Interquartile = Interquartile[0].tolist()

Interquartile = NeighbourhoodTableChange[NeighbourhoodTableChange.index.isin(Interquartile)]
Interquartile['Total % Change'] = Interquartile['Total % Change'].abs().round(4)
Interquartile.sort_values(by='Total % Change', ascending = True, inplace = True)


Interquartile = (Interquartile.head(10).index.tolist())
InterquartileAnswer = NeighbourhoodTable[NeighbourhoodTable.index.isin(Interquartile)]


'''Top Quantile'''

Topquartile = Neighbourhoods[Neighbourhoods[1] >= 6*(10**8)]
Topquartile = Topquartile[0].tolist()

Topquartile = NeighbourhoodTableChange[NeighbourhoodTableChange.index.isin(Topquartile)]
Topquartile['Total % Change'] = Topquartile['Total % Change'].abs().round(4)
Topquartile.sort_values(by='Total % Change', ascending = True, inplace = True)


Topquartile = Topquartile.head(10).index.tolist()
TopquartileAnswer = NeighbourhoodTable[NeighbourhoodTable.index.isin(Topquartile)]


'''Regression plots'''

Top = TopquartileAnswer.T.plot(figsize= (12,7))
Top.set_xlabel('Assessment Year')
Top.set_ylabel('Total Assessed Value of the Neighbourhood * 10^9')

Middle = InterquartileAnswer.T.plot(figsize = (12,7))
Middle.set_xlabel('Assessment Year')
Middle.set_ylabel('Total Assessed Value of the Neighbourhood * 10^8')


'''Regression Slope Sanity Check'''

NeighbourhoodTable['Slope'] = NeighbourhoodTable.apply(calc_slope,axis = 1)
InterquartileCheck = NeighbourhoodTable[NeighbourhoodTable.index.isin(Interquartile)]
InterquartileCheck.sort_values(by='Slope', ascending = True, inplace = True)



TopquartileCheck = NeighbourhoodTable[NeighbourhoodTable.index.isin(Topquartile)]
TopquartileCheck.sort_values(by='Slope', ascending = True, inplace = True)







