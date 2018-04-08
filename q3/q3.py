#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 17:53:22 2018

@author: igor
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

#import numpy as np
#import matplotlib.pyplot as plt
#import datetime
#import pandas_datareader.data as web
#from stocker import Stocker
#import os
#os.getcwd() # this is to check the current working directory
#os.chdir("/home/igor/EPAT/strat6-python/")

#end = datetime.datetime.now().date()
#start = end - pd.Timedelta(days=365*10)
#df = web.get_data_yahoo("AAPL", start, end)

def read_csv(file_name):
    stock = pd.read_csv(file_name, parse_dates=['Date'], index_col=['Date'], thousands=',')
    #stock['Return'] = np.log(stock['Close'] / stock['Close'].shift(1))
    return stock[(stock.index.year == 2016) | ((stock.index.year == 2017))]

junior = read_csv('Junior ETF.csv')
junior.columns = ['Junior']
nifty = read_csv('Nifty ETF.csv')
nifty.columns = ['Nifty']

stocks = pd.concat([
        read_csv('BHARTIARTL.NS.csv')['Close'],
        read_csv('COALINDIA.NS.csv')['Close'],
        read_csv('HCLTECH.NS.csv')['Close'],
        read_csv('HDFCBANK.NS.csv')['Close'],
        read_csv('INFY.csv')['Close'],
        read_csv('LTC.csv')['Close'],
        read_csv('NTPC.NS.csv')['Close'],
        read_csv('ONGC.NS.csv')['Close'],
        read_csv('RS.csv')['Close'],
        read_csv('TATAMOTORS.NS.csv')['Close']
        ], axis = 1)
# rename cols
stocks.columns = ['BHARTI','COAL','HCLTECH','HDFCB','INFY','LTC','NTPC','ONGG','RS','TATA']
# calculate daily return
#stocks['PORTFOLIO'] = stocks.sum(axis =1)
stock_ret = np.log(stocks / stocks.shift(1)) 
stock_ret.fillna(0, inplace=True)
# calculate buy & hold performance
stocks_cumsum_ret = stock_ret.cumsum() # single stocks
stocks_cumsum_ret.plot()
# total period return of buy & hold
ret = stocks_cumsum_ret.tail(1).iloc[0] # get the last row
# total portfolio return : invested 1usd into each stock
portfolio_ret = np.exp(ret).sum() / ret.count() - 1 # invested 1 usd into each --> count() == total invested capital 
# portfolio daily return
p = pd.DataFrame(np.exp(stocks_cumsum_ret).sum(axis = 1), columns=['Portfolio']) # portfolio
p['Daily return'] = np.log(p / p.shift(1)) #daily portfolio return

# REGRESSION

data = pd.concat([p['Daily return'],nifty, junior], axis = 1) # align data
data.fillna(0, inplace=True)
y = data['Daily return'] 
x = data[['Nifty','Junior']]
x = sm.add_constant(x) # add const
model = sm.OLS(y, x).fit()
predictions = model.predict(x)
print(model.summary())

# Draw
plt.figure(figsize=(10, 5))
plt.plot(predictions, label='predictions')
plt.plot(y, label='Portfolio returns')
plt.legend() #[goldLine,juniorLine,niftyLine]
plt.grid(True)
plt.title("Multiple regression")
plt.xlabel('Time')
plt.ylabel('Return %')
plt.show() # will display the current figure that you are working on

# RESULTS
#B1 = 2.332e-06 // Nifty
#B2 = -9.54e-06 // Junior
# R^2 = 0 => 100% of portfolio variance is not explained by Nifty and Junior variation
'''
 OLS Regression Results                            
==============================================================================
Dep. Variable:           Daily return   R-squared:                       0.000
Model:                            OLS   Adj. R-squared:                 -0.003
Method:                 Least Squares   F-statistic:                    0.1089
Date:                Sun, 08 Apr 2018   Prob (F-statistic):              0.897
Time:                        20:58:42   Log-Likelihood:                 1832.6
No. Observations:                 518   AIC:                            -3659.
Df Residuals:                     515   BIC:                            -3646.
Df Model:                           2                                         
Covariance Type:            nonrobust                                         
==============================================================================
                 coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------
const          0.0006      0.001      0.390      0.697      -0.002       0.003
Nifty       2.332e-06    7.9e-06      0.295      0.768   -1.32e-05    1.78e-05
Junior      -9.54e-06   2.67e-05     -0.358      0.721   -6.19e-05    4.29e-05
==============================================================================
Omnibus:                       38.396   Durbin-Watson:                   1.782
Prob(Omnibus):                  0.000   Jarque-Bera (JB):               79.583
Skew:                          -0.433   Prob(JB):                     5.23e-18
Kurtosis:                       4.713   Cond. No.                     4.25e+03
==============================================================================
'''