#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 23:55:03 2018

@author: igor
Question 2
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
#import os
#os.getcwd() # this is to check the current working directory
#os.chdir("/home/igor/EPAT/strat6-python/")
gold = pd.read_csv('Gold ETF.csv', parse_dates=['Date'], index_col=['Date'], thousands=',')
junior = pd.read_csv('Junior ETF.csv', parse_dates=['Date'], index_col=['Date'], thousands=',')
nifty = pd.read_csv('Nifty ETF.csv', parse_dates=['Date'], index_col=['Date'], thousands=',')
# initial allocation of the capital
capital_t0 = 100 #initial capital
w_gold = 0.3
w_junior = 0.2
w_nifty = 0.5

#calculate returns (continious returns)
goldRet = pd.DataFrame(np.log(gold["Close"] / gold["Close"].shift(1)))
goldRet.columns=["Gold return"]
juniorRet = pd.DataFrame(np.log(junior["Close"] / junior["Close"].shift(1)))
juniorRet.columns=["Junior return"]
niftyRet = pd.DataFrame(np.log(nifty["NAV"] / nifty["NAV"].shift(1)))
niftyRet.columns=["Nifty return"]

# align all return data
data = pd.concat([goldRet,juniorRet,niftyRet], axis=1)
data.fillna(0, inplace=True)
#chart data
plt.figure(figsize=(10, 5))
goldLine = plt.plot(goldRet.cumsum(), label='Gold ETF')
juniorLine = plt.plot(juniorRet.cumsum(), label='Junior ETF')
niftyLine = plt.plot(niftyRet.cumsum(), label='Nifty ETF')
plt.legend() #[goldLine,juniorLine,niftyLine]
plt.grid(True)
plt.title("ETF Performance")
plt.xlabel('Time')
plt.ylabel('Return %')
plt.show() # will display the current figure that you are working on

# Strtaegy calculation
def strategy():
    #initial step
    goldCap = w_gold * capital_t0
    juniorCap = w_junior * capital_t0
    niftyCap = w_nifty * capital_t0
    portfolio = pd.DataFrame() # resulting portfolio performance
    
    for year in [2016,2017]:
        for quarter in [1,2,3,4]:
            # make a window for the quarter
            selector = np.where(( (data.index.year == year) & \
                                 (((data.index.month - 1) // 3 + 1) == quarter)), True, False)
            # estimate portfolio performance
            a = np.exp(data.loc[selector][['Gold return','Junior return','Nifty return']].cumsum()) * [goldCap,juniorCap,niftyCap]
            a['Portfolio'] = a['Gold return'] + a['Junior return'] + a['Nifty return']
            # add quarter perfomance data to the history
            portfolio = pd.concat([portfolio, a], axis=0)
            # rebalance - the last row (tail) keeps the latest value of the portfolio
            goldCap = a.tail(1).iloc[0]['Gold return']
            juniorCap = a.tail(1).iloc[0]['Junior return']
            niftyCap = a.tail(1).iloc[0]['Nifty return']
            # rebalance to the standard weights
            p = goldCap + juniorCap + niftyCap
            goldCap = p * w_gold
            juniorCap = p * w_junior
            niftyCap = p * w_nifty
    return portfolio

def print_annualized_performance(p, year):
    p2 = np.log(p / p.shift(1))[p.index.year == year] 
    sigma_p = p2['Portfolio'].std()*(p2['Portfolio'].count())**0.5 # annualized stdev
    # annualized return 
    return_p = p2['Portfolio'].sum()
    return_p2 = np.exp(return_p) - 1
    free_p = 2.10 / 100
    sharpe = (return_p - free_p)/sigma_p
    print("Performance for {0}:".format(year))
    print("Anuual Continously Compounded Return {0}%".format(return_p*100))
    print("Anuual Return {0}%".format(return_p2*100))
    print("Std: {0}%".format(sigma_p*100))
    print("Sharpe: {0}".format(sharpe))

p = strategy()
p.sort_index()
p.plot()
#calculate portfolio return
print_annualized_performance(p, 2016)
print_annualized_performance(p, 2017)

'''portfolio performance
Performance for 2016:
Anuual Continously Compounded Return 6.895766853396358%
Anuual Return 7.139085464281658%
Std: 10.02078661662958%
Sharpe: 0.4785818755423593

Performance for 2017:
Anuual Continously Compounded Return 21.57675422680396%
Anuual Return 24.081390868639495%
Std: 6.528105317287844%
Sharpe: 2.9835232858797904