import os
import pandas as pd
import numpy as np
import datetime

def read_dataframe(path, sheet_name=None):
    '''
        Inputs:
        - path: file path leading to the price file, with daily data
        - sheet_name: name of the specific Excel sheet

        Output: 
        - prices: price file under a dataframe form
    '''
    prices = pd.read_excel(path, sheet_name=sheet_name)
    prices['Date'] = prices['Date'].apply(lambda x: datetime.datetime.fromordinal(datetime.datetime(1900, 1, 1).toordinal()+int(x)-2))
    prices.index = prices['Date']
    prices = prices.drop('Date', axis=1)
    prices = prices.drop(prices.columns[prices.isnull().mean()>0.99], axis=1)
    return prices 


def historicalvar(returns, alpha=1):
    '''
        Inputs:
        - returns: series or dataframe containing an asset's return
        - alpha: confidence interval level

        Output: historical VaR level at given confidence interval

    '''
    if isinstance(returns, pd.Series):
        return np.percentile(returns, alpha)
    elif isinstance(returns, pd.DataFrame):
        return returns.aggregate(historicalvar, alpha)
    else:
        raise TypeError('Expected returns to either be dataframe or pandas series')
    
def cVaR(returns, alpha=1):
    '''
        Inputs:
        - returns: series or dataframe containing an asset's return
        - alpha: confidence interval level

        Output: conditional VaR/expected shortfall level at given confidence interval
    '''
    if isinstance(returns, pd.Series):
        belowVaR = returns <= historicalvar(returns, alpha)
        return returns[belowVaR].mean()
    elif isinstance(returns, pd.DataFrame):
        return returns.aggregate(cVaR, alpha)
    else:
        return TypeError('Expected returns to either be dataframe or pandas series')
    
def rebase(value, current_days, final_days):
    rebasing_val = final_days/current_days
    rebased_value = value**np.sqrt(rebasing_val)
    return rebased_value

historical_depth = [1, 2, 3, 4, 5, 7, 10]
nbr_days = [1, 5, 10]

def cVaR_data(prices, historical_depth, nbr_days):
    '''
        Input: 
        - prices: prices file

        Output:
        - cVaR_df: conditional var for a given historical depth (i) and given returns on j days - provided that we have daily data
    '''
    cVaR_df = pd.DataFrame()
    cVaR_df.index = prices.columns

    for i in historical_depth:
        for j in nbr_days:
            cVaR_df['95th percentile'+str(i)+'years'+str(j)+'days'] = [-cVaR(prices.iloc[(-252*i)].pct_change(j)[column].dropna(),5) for column in prices.columns]
            cVaR_df['99th percentile'+str(i)+'years'+str(j)+'days'] = [-cVaR(prices.iloc[(-252*i)].pct_change(j)[column].dropna(),1) for column in prices.columns]
            cVaR_df['98.5th percentile'+str(i)+'years'+str(j)+'days'] = [-cVaR(prices.iloc[(-252*i)].pct_change(j)[column].dropna(),1.5) for column in prices.columns]
            cVaR_df['99.5th percentile'+str(i)+'years'+str(j)+'days'] = [-cVaR(prices.iloc[(-252*i)].pct_change(j)[column].dropna(),0.5) for column in prices.columns]
            cVaR_df['99.9th percentile'+str(i)+'years'+str(j)+'days'] = [-cVaR(prices.iloc[(-252*i)].pct_change(j)[column].dropna(),0.1) for column in prices.columns]

    return -cVaR_df        



    


