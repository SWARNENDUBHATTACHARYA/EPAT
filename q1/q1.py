# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#import openpyxl as px
import pandas as pd
#import os
#os.getcwd() # this is to check the current working directory
#os.chdir("/home/igor/EPAT/strat6-python/")
niftyTotal = pd.read_csv('NIFTY-TotalReturnsIndex.csv', parse_dates=['Date'], index_col=['Date'], thousands=',')
relaince = pd.read_csv('Reliance Nifty ETF.csv', parse_dates=['Date'], index_col=['Date'], thousands=',')
kotak = pd.read_csv('Kotak Nifty ETF.csv', parse_dates=['Date'], index_col=['Date'], thousands=',')
hdfc = pd.read_csv('HDFC Nifty ETF.csv', parse_dates=['Date'], index_col=['Date'], thousands=',')
uti = pd.read_csv('UTI Nifty ETF.csv', parse_dates=['Date'], index_col=['Date'], thousands=',')

# calculate daily returns
niftyTotalRet = niftyTotal["Total Returns Index"] /  niftyTotal["Total Returns Index"].shift(1)
relainceRet = relaince["NAV"] /  relaince["NAV"].shift(1)
relainceRet.rename("relainceRet")
kotakRet = kotak["NAV"] /  kotak["NAV"].shift(1)
hdfcRet = hdfc["Close"] /  hdfc["Close"].shift(1)
utiRet = uti["NAV"] /  uti["NAV"].shift(1)

#conctenate and align returns
data = pd.concat([niftyTotalRet,relainceRet, kotakRet, hdfcRet, utiRet], axis=1)
data.columns=['niftyTotal','relaince','kotak','hdfc','uti']

#Tracking error calculation
def calculateTrackingError(benchmark, var,  year):
    bYear = (var.index.year == year)
    diff = (benchmark - var)**2
    return (252**0.5)*(diff[bYear].sum() / (diff[bYear].count() - 1))**0.5

result = pd.DataFrame(columns=['Fund', '2016','2017'])
#result.set_index(['Fund'], inplace=True)
result.loc[0] = ['relaince',
                  calculateTrackingError(data['niftyTotal'], data['relaince'], 2016),
                  calculateTrackingError(data['niftyTotal'], data['relaince'], 2017)
                  ]
result.loc[1] = ['kotak',
                  calculateTrackingError(data['niftyTotal'], data['kotak'], 2016),
                  calculateTrackingError(data['niftyTotal'], data['kotak'], 2017)
                  ]
result.loc[2] = ['hdfc',
                  calculateTrackingError(data['niftyTotal'], data['hdfc'], 2016),
                  calculateTrackingError(data['niftyTotal'], data['hdfc'], 2017)
                  ]
result.loc[3] = ['uti',
                  calculateTrackingError(data['niftyTotal'], data['uti'], 2016),
                  calculateTrackingError(data['niftyTotal'], data['uti'], 2017)
                  ]
#r = {'Fund' : 'relaince', 
#               '2016': calculateTrackingError(data['niftyTotal'], data['relaince'], 2016), 
#               '2017' : calculateTrackingError(data['niftyTotal'], data['relaince'], 2017)}

#result.append(r, ignore_index=True)
result.sort_values(['2016','2017'], ascending=[True, True])

#b=calculateTrackingError(data['niftyTotal'], data['relaince'], 2016)
print(result)
#Fund	          2016	               2017
#relaince  0.03781765201625606	0.022470898571540016
#kotak	   0.05193383878326064	0.0387414314565038
#uti	       0.10223705333692946	0.08392457828317103
#hdfc      0.11566217727121621	0.05959374579655248

# increase in annualized TE from 2016 to 2017: none
# decrease in annualized TE from 2016 to 2017: all


