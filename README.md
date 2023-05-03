# Computing Values at Risk

This code helps one compute values at risk (VaRs) through an Excel spreadsheet with prices data on dozens of securities (on a daily basis).
Two methods (May 2023 update) are computed:
- Historical value at risk (hVaR)
- Conditional historical value at risk (c-hVaR)

## What is a Value at Risk?
The Value at Risk is a statistic used in risk management to predict the greatest possible losses over a specific time frame. 
It is determined by 3 variables: 
- Period
- Confidence level
- Size of possible loss

Three methods are used in otder to compute the VaR: the historical method (implemented in May 2023), the variance-covariance method, and the Monte-Carlo simulation. 
