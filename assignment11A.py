##
## File: assignment11-solns.py (STAT 3250)
## Topic: Assignment 11 Solutions
##

##  The file Stocks.zip is a zip file containing nearly 100 sets of price 
##  records for various stocks.  A sample of the type of files contained
##  in Stocks.zip is ABT.csv, which we have seen previously and is posted
##  in recent course materials. Each file includes daily data for a specific
##  stock, with stock ticker symbol given in the file name. Each line of
##  a file includes the following:
##
##   Date = date for recorded information
##   Open = opening stock price 
##   High = high stock price 
##   Low = low stock price 
##   Close = closing stock price 
##   Volume = number of shares traded
##   Adj Close = closing price adjusted for stock splits (ignored for this assignment)

##   The time interval covered varies from stock to stock. Within many files
##   there are dates when the market was open but the data is not provided, so
##   those records are missing. Note that some dates are not present because 
##   market is closed on weekends and holidays.  Those are not missing records.  

##  The Gradescope autograder will be evaluating your code on a subset 
##  of the set of files in the folder Stocks.  Your code needs to automatically 
##  handle all assignments to the variables q1, q2, ... to accommodate the 
##  reduced set, so do not copy/paste things from the console window, and
##  take care with hard-coding values. 

##  The autograder will contain a folder Stocks containing the stock data sets.
##  This folder will be in the working directory so your code should be written
##  assuming that is the case.

import numpy as np  # load numnpy
import pandas as pd # load pandas
pd.set_option('display.max_columns', 10) # Display 10 columns in console


# Read in the stock files, using the 'glob' library
# The working directory needs to be set to the directory containing
# the Stocks folder.

import glob # 'glob' searches for files
# '*.csv' selects files ending in '.csv'
filelist = glob.glob('Stocks/*.csv') # Read in stock files

df = pd.DataFrame()  # The dataframe to hold all the stock records
for f in filelist:
    newdf = pd.read_csv(f)  # Read in a stock file
    newdf['Stock'] = f.split('.')[0][7:]  # Add name of stock to records
    df = pd.concat([df,newdf])  # Concatenate the stock file to the dataframe

## 1.  Find the mean for the Open, High, Low, and Close entries for all 
##     records for all stocks.  Give your results as a Series with index
##     Open, High, Low, Close (in that order) and the corresponding means
##     as values.

# We select the columns for Open, High, Low, and Close, then use '.mean()'
# which will return the mean for each of the columns at the same time.

q1 = df[['Open','High','Low','Close']].mean() # Series of means of Open, High, Low, and Close

"""
## 1.

Open     51.120641   # The means for Open, High, Low, and Close
High     51.697694
Low      50.525999
Close    51.131146

"""


## 2.  Find all stocks with an average Close price less than 30.  Give your
##     results as a Series with ticker symbol as index and average Close price. 
##     price as value.  Sort the Series from lowest to highest average Close
##     price.  (Note: 'MSFT' is the ticker symbol for Microsoft.  'MSFT.csv',
##     'Stocks/MSFT.csv' and 'MSFT ' are not ticker symbols.)

# Group the 'Close' prices based on the 'Stock' ticker symbol 
group2 = df['Close'].groupby(df['Stock']) 
group2means = group2.mean()  # Find the mean Close for each stock
q2 = group2means[group2means<30].sort_values()  # The bottom-5 mean Close

"""
## 2.

Stock
NI      21.006456  
CAG     25.557409
FITB    26.414602

"""


## 3.  Find the top-10 stocks in terms of the day-to-day volatility of the
##     price, which we define to be the mean of the daily differences 
##     High - Low for each stock. Give your results as a Series with the
##     ticker symbol as index and average day-to-day volatility as value. 
##     Sort the Series from highest to lowest average volatility.

# Start by adding a new column 'Vol' to the dataframe to hold the
# daily volatility.
df['Vol'] = df['High'] - df['Low']

# Group the 'Vol' values based on the 'Stock' ticker symbol 
group3 = df['Vol'].groupby(df['Stock']) 
group3means = group3.mean()  # Find the mean Vol for each stock
q3 = group3means.sort_values(ascending=False)[0:10]  # Series of top-10 mean volatility

"""
## 3.

Stock
CMI     2.231340
SLB     1.983233
VNO     1.879858
PPG     1.716947
OXY     1.649788
CVX     1.618029
TSCO    1.579966
MMM     1.423166
ESV     1.387686
INTU    1.180895

"""


## 4.  Repeat the previous problem, this time using the relative volatility, 
##     which we define to be the mean of
## 
##                       (High − Low)/(0.5(Open + Close))
##
##     for each day. Provide your results as a Series with the same specifications
##     as in the previous problem.

# We proceed similar to #3, starting with a new column 'RelVol'.
df['RelVol'] = (df['High'] - df['Low'])/(0.5*(df['Open'] + df['Close']))

# Group the 'RelVol' values based on the 'Stock' ticker symbol 
group4 = df['RelVol'].groupby(df['Stock']) 
group4means = group4.mean()  # Find the mean RelVol for each stock
q4 = group4means.sort_values(ascending=False)[0:10]  # Series of top-10 mean relative volatility

"""
## 4.

Stock
AKAM    0.038354
KMX     0.035649
ESV     0.035586
RHT     0.034125
FITB    0.032628
CMI     0.032048
M       0.031604
TSCO    0.031209
SLB     0.029079
BAC     0.028496

"""


## 5.  For each day the market was open in October 2008, find the average 
##     daily Open, High, Low, Close, and Volume for all stocks that have
##     records for October 2008.  (Note: The market is open on a given
##     date if there is a record for that date in any of the files.)
##     Give your results as a DataFrame with dates as index and columns of
##     means Open, High, Low, Close, Volume (in that order).  The dates should 
##     be sorted from oldest to most recent, with dates formatted (for example)
##     2008-10-01, the same form as in the files.   

# This is the first place we use the Date column.  We start by setting the
# data type so that the values are recognized as dates.
df['Date'] = pd.to_datetime(df['Date'])

# Next we define a new dataframe that includes only the records from Oct '08
df5 = df[(df['Date'].dt.year == 2008) & (df['Date'].dt.month == 10)]

# Then we group the values 'Open','High','Low','Close','Volume' by 'Date'
group5 = df5[['Open','High','Low','Close','Volume']].groupby(df5['Date'])
q5 = group5.mean()  # DataFrame of means for each open day of Oct '08.

"""
## 5.
                 Open       High        Low      Close        Volume
Date                                                                
2008-10-01  42.722271  43.759998  41.646816  42.932725  1.092378e+07
2008-10-02  43.858331  44.244997  42.014581  42.454581  1.059698e+07
2008-10-03  42.927498  44.145831  41.425415  41.727498  1.144612e+07
2008-10-06  40.574165  41.556248  37.999998  40.487915  1.437481e+07
2008-10-07  41.960474  42.664760  38.876188  39.125236  1.699004e+07
2008-10-08  37.079998  40.019581  36.116248  38.055831  2.588118e+07
2008-10-09  38.487498  39.146665  34.466664  34.713748  1.917295e+07
2008-10-10  33.181249  36.464581  31.252915  34.571665  2.536705e+07
2008-10-13  36.314998  38.378749  34.722915  37.873332  1.730743e+07
2008-10-14  39.224284  40.088093  36.114283  37.462854  2.225504e+07
2008-10-15  36.603748  37.032081  33.085832  33.522498  1.513322e+07
2008-10-16  33.856665  35.846247  31.860832  35.285831  1.867913e+07
2008-10-17  33.306520  35.340868  32.191302  33.705216  1.498197e+07
2008-10-20  35.142172  36.545649  34.313042  36.309128  1.136855e+07
2008-10-21  36.230415  37.256665  35.198748  35.750414  1.019015e+07
2008-10-22  34.800831  35.392082  32.801248  33.742082  1.304482e+07
2008-10-23  35.139563  36.508693  33.264346  35.532172  1.470610e+07
2008-10-24  31.923748  34.247915  31.436664  32.935831  1.333542e+07
2008-10-27  32.417915  34.094997  31.571665  32.058332  1.066473e+07
2008-10-28  32.781737  35.460868  31.256955  35.294781  1.512451e+07
2008-10-29  35.624998  37.071665  34.379998  35.382915  1.390545e+07
2008-10-30  35.550000  36.233478  34.208695  35.474348  1.032877e+07
2008-10-31  35.972082  37.656248  35.236665  36.857498  1.445258e+07

"""


## 6. For 2011, find the date with the maximum average relative volatility 
##    for all stocks and the date with the minimum average relative 
##    volatility for all stocks. Give your results as a Series with 
##    the dates as index and corresponding average relative volatility
##    as values, with the maximum first and the minimum second.

# Start by extracting the records for 2011.
df6 = df[df['Date'].dt.year == 2011]

# Next we group 'RelVol' on 'Date'
group6 = df6['RelVol'].groupby(df6['Date'])

# Last step: Compute the means for each date, sort by means, and extract
# the first (minimum) and last (maximum) values with dates.
q6 = group6.mean().sort_values()[[-1,0]] # Series of average relative volatilities

"""
## 6.

Date
2011-08-08    0.076450
2011-12-30    0.013126

"""


## 7. For 2010-2012, find the average relative volatility for all stocks on
##    Monday, Tuesday, ..., Friday.  Give your results as a Series with index
##    'Mon','Tue','Wed','Thu','Fri' (in that order) and corresponding
##    average relative volatility as values. 

# Start by extracting the records for 2010-2012.
df7 = df[(df['Date'].dt.year >= 2010) & (df['Date'].dt.year <= 2012)]

# Next we group 'RelVol' on the day of the week (formatted).  Note that we
# do not have to create a new column for 'df' when doing this.
group7 = df7['RelVol'].groupby(df7['Date'].dt.strftime("%a"))
q7 = group7.mean()[['Mon','Tue','Wed','Thu','Fri']] # Series of average relative volatility by day of week

"""
## 7.

Date
Mon    0.020995
Tue    0.022709
Wed    0.022353
Thu    0.023769
Fri    0.021745

"""


## 8.  For each month of 2009, determine which stock had the maximum average 
##     relative volatility. Give your results as a Series with MultiIndex
##     that includes the month (month number is fine) and corresponding stock 
##     ticker symbol (in that order), and the average relative volatility
##     as values.  Sort the Series by month number 1, 2, ..., 12.

# Start by extracting the records for 2009.
df8 = df[(df['Date'].dt.year == 2009)]

# Next we group 'RelVol' on the stock and the month.  
group8 = df8['RelVol'].groupby([df8['Date'].dt.month,df8['Stock']])
# Then we compute group mean, and extract the maximum for each month.
q8 = group8.mean().groupby(level=0, group_keys=False).nlargest(1) # Series of maximum relative volatilities by month

"""
## 8.

Date  Stock
1     FITB     0.145080
2     FITB     0.262208
3     FITB     0.170874
4     FITB     0.160335
5     FITB     0.115028
6     FITB     0.063216
7     FITB     0.055839
8     FITB     0.052509
9     FITB     0.042233
10    FITB     0.049102
11    M        0.043446
12    M        0.034192

"""

## 9.  The “Python Index” is designed to capture the collective movement of 
##     all of our stocks. For each date, this is defined as the average price 
##     for all stocks for which we have data on that day, weighted by the 
##     volume of shares traded for each stock.  That is, for stock values 
##     S_1, S_2, ... with corresponding volumes V_1, V_2, ..., the average
##     weighted volume is
##
##           (S_1*V_1 + S_2*V_2 + ...)/(V_1 + V_2 + ...)
##
##     Find the Open, High, Low, and Close for the Python Index for each date
##     the market was open in January 2013. 
##     Give your results as a DataFrame with dates as index and columns of
##     means Open, High, Low, Close (in that order).  The dates should 
##     be sorted from oldest to most recent, with dates formatted (for example)
##     2013-01-31, the same form as in the files.   


# We start by adding 4 new columns to 'df', named 'OpenVolume', 'HighVolume',
# 'LowVolume', and 'CloseVolume'.  These will be the row-by-row products of
# 'Open', 'High', 'Low', and 'Close', respectively, when multiplied by
# 'Volume'.  Sums of values from these columns will be used for the numerator
# of the Python Index formula.

df['OpenVolume'] = df['Open']*df['Volume']
df['HighVolume'] = df['High']*df['Volume']
df['LowVolume'] = df['Low']*df['Volume']
df['CloseVolume'] = df['Close']*df['Volume']

# We only need the records for January 2013, so we extract those.
df9 = df[(df['Date'].dt.year == 2013) & (df['Date'].dt.month == 1)]

# We want the Python Index for each date, so we group the columns of
# 'df9' by the column 'Date'.
group9 = df9.groupby(df9['Date'])

# Next we create a new dataframe 'pyind9' to hold the Python Index
# records.
pyind9 = pd.DataFrame()  # The new (empty) dataframe 

# The columns for the new dataframe.  
pyind9['Open'] = group9['OpenVolume'].sum()/group9['Volume'].sum()
pyind9['High'] = group9['HighVolume'].sum()/group9['Volume'].sum()
pyind9['Low'] = group9['LowVolume'].sum()/group9['Volume'].sum()
pyind9['Close'] = group9['CloseVolume'].sum()/group9['Volume'].sum()

q9 = pyind9  # DataFrame of Python Index values for each open day of Jan 2013. 

"""
## 9.

# The values for the Python Index for January 2013.

                 Open       High        Low      Close
Date                                                  
2013-01-02  26.434119  26.663298  26.126769  26.467802
2013-01-03  27.565817  27.768296  27.297580  27.484102
2013-01-04  28.503559  28.813774  28.371426  28.729682
2013-01-07  24.989248  25.097450  24.752084  24.939711
2013-01-08  29.829415  30.048667  29.524780  29.864948
2013-01-09  21.471674  21.673379  20.980070  21.147272
2013-01-10  27.290640  27.515085  27.057295  27.398614
2013-01-11  27.806769  27.928422  27.484828  27.713908
2013-01-14  31.227286  31.479872  30.981003  31.230612
2013-01-15  28.846573  29.225079  28.726806  29.081978
2013-01-16  28.182061  28.451242  27.952810  28.338129
2013-01-17  22.619809  22.784892  22.162950  22.381414
2013-01-18  31.401574  31.724960  30.987536  31.529284
2013-01-22  33.410253  33.798772  33.208533  33.701697
2013-01-23  39.631141  39.921597  39.372066  39.748044
2013-01-24  37.326160  37.921525  37.192286  37.529979
2013-01-25  76.191693  77.297582  75.423897  76.204306
2013-01-28  40.612180  40.989203  40.178753  40.607533
2013-01-29  36.802919  37.243230  36.661393  37.114814
2013-01-30  36.049126  36.272722  35.735203  35.884687
2013-01-31  39.521791  40.040356  39.227484  39.749839

"""

## 10. For the years 2007-2012 determine the top-8 month-year pairs in terms 
##     of average relative volatility of the Python Index. Give your results
##     as a Series with MultiIndex that includes the month (month number is 
##     fine) and year (in that order), and the average relative volatility
##     as values.  Sort the Series by average relative volatility from
##     largest to smallest.

# We only need the records for 2007-2012, so we extract those.
df10 = df[(df['Date'].dt.year >= 2007) & (df['Date'].dt.year <= 2012)]

# We want the Python Index for each date, so we group the columns of
# 'df10' by the column 'Date'.
group10 = df10.groupby(df10['Date'])

# Next we create a new dataframe 'pyind9' to hold the Python Index
# records.
pyind10 = pd.DataFrame()  # The new (empty) dataframe 

# The columns for the new dataframe.  
pyind10['Open'] = group10['OpenVolume'].sum()
pyind10['High'] = group10['HighVolume'].sum()
pyind10['Low'] = group10['LowVolume'].sum()
pyind10['Close'] = group10['CloseVolume'].sum()

# Next we compute the average relative volatility for each date using
# the Python Index values, and add those to the data frame.
pyind10['RelVol'] = (pyind10['High'] - pyind10['Low'])/(0.5*(pyind10['Open'] + pyind10['Close']))

# Add a column 'Date' to pyind10 to use for grouping
pyind10['Date'] = pyind10.index

# Now we group by month and year, compute the mean for each, and extract
# the top-5.
group10 = pyind10['RelVol'].groupby([pyind10['Date'].dt.month,pyind10['Date'].dt.year])
q10 = group10.mean().nlargest(8) # Series of month-year pairs and average rel. volatilities

"""
## 10.

Date  Date
10    2008    0.090727
2     2009    0.081886
4     2009    0.074761
3     2009    0.073664
11    2008    0.073229
1     2009    0.063496
5     2009    0.061808
9     2008    0.060376

"""


## 11. Each stock in the data set contains records starting at some date and 
##     ending at another date.  In between the start and end dates there may be 
##     dates when the market was open but there is no record -- these are the
##     missing records for the stock.  For each stock, determine the percentage
##     of records that are missing out of the total records that would be
##     present if no records were missing. Give a Series of those stocks
##     with less than 1.3% of records missing, with the stock ticker as index 
##     and the corresponding percentage as values, sorted from lowest to 
##     highest percentage.

allopendates = np.unique(df['Date'])  # Identify dates market is open
allstocks = np.unique(df['Stock'])    # Identify the stocks
ser11 = pd.Series(len(allstocks)*[0.0])  # Series to hold percentages
ser11.index = allstocks  # set Series index to stocks

for stock in allstocks:  # loop through each stock
    stockdates = df.loc[df['Stock']==stock,'Date']  # Dates for stock
    stockmax = stockdates.max()  # latest date
    stockmin = stockdates.min()  # earliest date
    stockopendates = allopendates[(stockmin <= allopendates) & (allopendates <= stockmax)] # dates market open in range of stock dates
    missct = len(np.setdiff1d(stockopendates, stockdates))  # diff between sets = dates missing
    ser11[stock] = (100*(missct/(missct+len(stockdates))))  # compute percent of dates missing 
    
q11 = ser11[ser11<1.3].sort_values()  # Series of stocks and percent missing
    
"""
## 11.

ZTS     0.000000
NI      1.273190
GIS     1.273654
MMM     1.282521
AKAM    1.283462
SYY     1.298701

"""



