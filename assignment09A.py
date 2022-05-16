##
## File: assignment09-solutions.py (STAT 3250)
## Topic: Assignment 9 Solutions
##

##  This assignment requires the data file 'airline-stats.txt'.  This file 
##  contains thousands of records of aggregated flight information, organized 
##  by airline, airport, and month.  The first record is shown below. 

##  Note: The solutions below run on the data set 'airlines-stats-reduced.txt' 
##  that were used by the autograder.  Run your file on this data set in 
##  order to compare your answers to those below.
 
##
##  The file is quite large (1.8M lines, 31MB) so may be difficult to open in
##  Spyder.  An abbreviated version 'airline-stats-brief.txt' is also 
##  provided that has the same structure as the original data set.

# =============================================================================
# airport
#     code: ATL 
#     name: Atlanta GA: Hartsfield-Jackson Atlanta International
# flights 
#     cancelled: 5 
#     on time: 561 
#     total: 752 
#     delayed: 186 
#     diverted: 0
# number of delays 
#     late aircraft: 18 
#     weather: 28 
#     security: 2
#     national aviation system: 105 
#     carrier: 34
# minutes delayed 
#     late aircraft: 1269 
#     weather: 1722 
#     carrier: 1367 
#     security: 139 
#     total: 8314 
#     national aviation system: 3817
# dates
#     label: 2003/6 
#     year: 2003 
#     month: 6
# carrier
#     code: AA 
#     name: American Airlines Inc.
# =============================================================================

import numpy as np # load numpy as np
import pandas as pd # load pandas as pd

# Read in the test data as text one line at a time
airlines = pd.Series(open('airline-stats.txt').read().splitlines())

airdf = pd.DataFrame() # Initialize empty data frame

## Populate the columns one at a time.  
airdf['airport.code'] = airlines[1::33].str.split().str[1].tolist()
airdf['airport.city'] = airlines[2::33].str.split(": ").str[1].tolist()
airdf['airport.name'] = airlines[2::33].str.split(": ").str[2].tolist()
airdf['flights.cancelled'] = airlines[4::33].str.split(": ").str[1].astype(int).tolist()
airdf['flights.on_time'] = airlines[5::33].str.split(": ").str[1].astype(int).tolist()
airdf['flights.total'] = airlines[6::33].str.split(": ").str[1].astype(int).tolist()
airdf['flights.delayed'] = airlines[7::33].str.split(": ").str[1].astype(int).tolist()
airdf['flights.diverted'] = airlines[8::33].str.split(": ").str[1].astype(int).tolist()
airdf['num_delays.late_air'] = airlines[10::33].str.split(": ").str[1].astype(int).tolist()
airdf['num_delays.weather'] = airlines[11::33].str.split(": ").str[1].astype(int).tolist()
airdf['num_delays.security'] = airlines[12::33].str.split(": ").str[1].astype(int).tolist()
airdf['num_delays.nat_avia_sys'] = airlines[13::33].str.split(": ").str[1].astype(int).tolist()
airdf['num_delays.carrier'] = airlines[14::33].str.split(": ").str[1].astype(int).tolist()
airdf['min_delayed.late_air'] = airlines[16::33].str.split(": ").str[1].astype(int).tolist()
airdf['min_delayed.weather'] = airlines[17::33].str.split(": ").str[1].astype(int).tolist()
airdf['min_delayed.carrier'] = airlines[18::33].str.split(": ").str[1].astype(int).tolist()
airdf['min_delayed.security'] = airlines[19::33].str.split(": ").str[1].astype(int).tolist()
airdf['min_delayed.total'] = airlines[20::33].str.split(": ").str[1].astype(int).tolist()
airdf['min_delayed.nat_avia_sys'] = airlines[21::33].str.split(": ").str[1].astype(int).tolist()
airdf['dates.label'] = airlines[23::33].str.split(": ").str[1].tolist()
airdf['dates.year'] = airlines[24::33].str.split(": ").str[1].tolist()
airdf['dates.month'] = airlines[25::33].str.split(": ").str[1].astype(int).tolist()
airdf['carrier.code'] = airlines[27::33].str.split(": ").str[1].tolist()
airdf['carrier.name'] = airlines[28::33].str.split(": ").str[1].tolist()


## 1.  Give the total number of hours delayed for all flights in all records,
##     based on the entries in (minutes delayed)/total

# Add column minutes delayed/total, then divide by 60 to get hours.
q1 = airdf['min_delayed.total'].sum()/60

"""
## 1.

4115972.466666667  # total hours delayed

hidden (3 pts): check value
"""


## 2.  Which airlines appear in at least 500 records?  Give a Series with airline
##     names as index and record counts for values, in order of record count 
##     from largest to smallest.

# count carrier names, then extract those >= 500
q2 = airdf['carrier.name'].value_counts()[airdf['carrier.name'].value_counts() >= 500]
   
"""
## 2.

Delta Air Lines Inc.            1715  # The airline names and number of 
American Airlines Inc.          1680  # appearances in the data set
US Airways Inc.                 1671
United Air Lines Inc.           1630
Continental Air Lines Inc.      1605
AirTran Airways Corporation     1370
Frontier Airlines Inc.          1270
ExpressJet Airlines Inc.        1263
JetBlue Airways                 1150
Southwest Airlines Co.          1117
Mesa Airlines Inc.              1110
SkyWest Airlines Inc.           1045
Northwest Airlines Inc.         1041
American Eagle Airlines Inc.    1029
Alaska Airlines Inc.             994
Comair Inc.                      921
Atlantic Southeast Airlines      796
Pinnacle Airlines Inc.           681

visible (1 pt): check type = Series
hidden (2 pts): check Series
"""


## 3.  The entry under 'flights/delayed' is not always the same as the total
##     of the entries under 'number of delays'.  (The reason for this is not
##     clear.)  Determine the percentage of records for which these two
##     values are different.

# Compare flights/delayed to sum of entries under number of delays
q3 = 100*np.sum(airdf['flights.delayed'] != (airdf['num_delays.late_air'] + airdf['num_delays.weather'] + airdf['num_delays.security'] + airdf['num_delays.nat_avia_sys'] + airdf['num_delays.carrier']))/len(airdf) 

"""
## 3.

29.06904508342208  # percentage of different records

hidden (3 pts): check value 
"""


## 4.  Determine the percentage of records for which the number of delays due to
##     'late aircraft' exceeds the number of delays due to 'carrier'.

# compare the two entries, then sum the Trues
q4 = 100*np.sum(airdf['num_delays.late_air'] > airdf['num_delays.carrier'])/len(airdf)

"""
## 4.

41.62229321973731  # percent records with late aircraft exceeding carrier delays

hidden (3 pts): check value 
"""


## 5.  Find the top-8 airports in terms of the total number of minutes delayed.
##     Give a Series with the airport names (not codes) as index and the total 
##     minutes delayed as values, sorted order from largest to smallest total.
##     (Include any ties for 8th position as usual)

# Group the total minutes delayed by airport, compute each sum, then sort
# and print out top-8.
group05 = airdf['min_delayed.total'].groupby(airdf['airport.name'])
q5 = group05.sum().sort_values(ascending=False)[0:8]

"""
## 5.

airport.name
Hartsfield-Jackson Atlanta International    26453257
Chicago O'Hare International                26434222
Dallas/Fort Worth International             15242537
Newark Liberty International                14329010
San Francisco International                 11685127
Denver International                        11445521
Los Angeles International                   10199051
John F. Kennedy International                9550710

visible (1 pt): check type = Series
hidden (2 pts): check Series
"""


## 6.  Find the top-12 airports in terms of percentage of on-time flights.
##     Give a Series of the airport names (not codes) as index and percentages
##     as values, sorted from largest to smallest percentage. (Include any
##     ties for 12th position as usual)

# Group the total and on time flights by airport, compute each sum, divide,
# then sort and print out top-12.
group6 = airdf[['flights.on_time','flights.total']].groupby(airdf['airport.name'])
q6 = (100*group6.sum()['flights.on_time']/group6.sum()['flights.total']).sort_values(ascending=False)[0:12]

"""
## 6.

airport.name
Salt Lake City International                            83.418846
Phoenix Sky Harbor International                        82.395810
Chicago Midway International                            81.058578
Portland International                                  80.566124
George Bush Intercontinental/Houston                    80.565183
Baltimore/Washington International Thurgood Marshall    80.306278
McCarran International                                  80.299277
Denver International                                    80.123584
San Diego International                                 79.924097
Tampa International                                     79.536849
Seattle/Tacoma International                            79.472297
Orlando International                                   79.282851

visible (1 pt): check type = Series
hidden (2 pts): check Series
"""


## 7.  Find the top-10 airlines in terms of percentage of on time flights.
##     Give a Series of the airline names (not codes) as index and percentages  
##     as values, sorted from largest to smallest percentage. (Include any
##     ties for 10th position as usual)

# Group the total and on time flights by airline, compute each sum, divide,
# then sort and print out top-10.
group7 = airdf[['flights.on_time','flights.total']].groupby(airdf['carrier.name'])
q7 = (100*group7.sum()['flights.on_time']/group7.sum()['flights.total']).sort_values(ascending=False)[0:10]

"""
## 7.

carrier.name
Aloha Airlines Inc.            86.117647
Alaska Airlines Inc.           82.113187
Southwest Airlines Co.         81.103990
SkyWest Airlines Inc.          79.559121
Frontier Airlines Inc.         79.385138
AirTran Airways Corporation    78.659444
Pinnacle Airlines Inc.         78.246443
Delta Air Lines Inc.           78.184099
US Airways Inc.                78.098198
Mesa Airlines Inc.             77.477003

visible (1 pt): check type = Series
hidden (2 pts): check Series
"""


## 8.  Determine the average length (in minutes) by airline of a delay due
##     to the national aviation system.  Give a Series of airline name (not 
##     code) as index and average delay lengths as values, sorted from largest 
##     to smallest average delay length.

# Group the number of delays and minutes delayed by airline, compute each sum, divide,
# then sort and print.
group8 = airdf[['num_delays.nat_avia_sys','min_delayed.nat_avia_sys']].groupby(airdf['carrier.name'])
q8 = (group8.sum()['min_delayed.nat_avia_sys']/group8.sum()['num_delays.nat_avia_sys']).sort_values(ascending=False)

"""
## 8.

carrier.name
ExpressJet Airlines Inc.        62.525652
SkyWest Airlines Inc.           60.917248
JetBlue Airways                 58.488065
Mesa Airlines Inc.              57.963801
American Eagle Airlines Inc.    53.247578
Continental Air Lines Inc.      50.748317
Atlantic Southeast Airlines     50.661366
Comair Inc.                     50.074634
American Airlines Inc.          48.039576
United Air Lines Inc.           47.713945
AirTran Airways Corporation     47.704901
Southwest Airlines Co.          43.181892
Pinnacle Airlines Inc.          42.760702
Hawaiian Airlines Inc.          42.217391
Delta Air Lines Inc.            42.035775
US Airways Inc.                 40.083044
Frontier Airlines Inc.          38.691088
Northwest Airlines Inc.         36.370548
Alaska Airlines Inc.            35.540944
Aloha Airlines Inc.             26.272727

visible (1 pt): check type = Series
hidden (2 pts): check Series
"""


## 9.  For each month, determine the percentage of flights delayed by weather.
##     Give a Series sorted by month (1, 2, ..., 12) with the corresponding
##     percentages as values.

group09 = airdf[['num_delays.weather','flights.total']].groupby(airdf['dates.month'])
sums09 = group09.sum()
q9 = 100*sums09['num_delays.weather']/sums09['flights.total']

"""
## 9.

dates.month
1     0.795855
2     0.840691
3     0.595756
4     0.513723
5     0.580902
6     0.909091
7     0.835359
8     0.707094
9     0.399734
10    0.391166
11    0.310662
12    0.958975

visible (1 pt): check type = Series
hidden (3 pts): check Series
"""


## 10. Find all airports where the average length (in minutes) of 
##     security-related flight delays exceeds 35 minutes.  Give a Series with  
##     airport names (not codes) as index and average delay times as values, 
##     sorted from largest to smallest average delay.

group10 = airdf[['num_delays.security','min_delayed.security']].groupby(airdf['airport.name'])
sums10 = group10.sum()
avedel10 = (sums10['min_delayed.security']/sums10['num_delays.security']).sort_values(ascending=False)
q10 = avedel10[avedel10 > 35]

"""
## 10.

airport.name
Logan International                         47.075000
Hartsfield-Jackson Atlanta International    46.988701
Chicago O'Hare International                44.878866
Miami International                         44.241176
LaGuardia                                   42.568182
San Francisco International                 40.572289
John F. Kennedy International               39.861905
Ronald Reagan Washington National           38.383117
Newark Liberty International                37.993711
Dallas/Fort Worth International             37.987382
Charlotte Douglas International             37.232258
Fort Lauderdale-Hollywood International     37.113861
San Diego International                     36.315126
Orlando International                       35.487179
Denver International                        35.251534
McCarran International                      35.115789

visible (1 pt): check type = Series
hidden (3 pts): check Series
"""


## 11. For each year, determine the airport that had the highest percentage
##     of delays.  Give a Series with the years (least recent at top) and 
##     airport names (not code) as MultiIndex and the percentages as values.

group11 = airdf[['flights.delayed','flights.total']].groupby([airdf['dates.year'],airdf['airport.name']])
sums11 = group11.sum()
perc11 = (100*sums11['flights.delayed']/sums11['flights.total'])
q11 = perc11.groupby(level=0, group_keys=False).nlargest(1)

"""
## 11.

dates.year  airport.name                
2007        Newark Liberty International    36.198461
2008        Newark Liberty International    33.961774
2009        Newark Liberty International    31.307501
2010        San Francisco International     26.344055
2011        Newark Liberty International    28.799771

visible (0.5 pt): check type = Series
visible (0.5 pt): check index type = MultiIndex
hidden (3 pts): check Series
"""


## 12. For each airline, determine the airport where that airline had its 
##     greatest percentage of delayed flights.  Give a Series with airline
##     names (not code) and airport names (not code) as MultiIndex and the
##     percentage of delayed flights as values, sorted from smallest to
##     largest percentage.

group12 = airdf[['flights.delayed','flights.total']].groupby([airdf['carrier.name'],airdf['airport.name']])
sums12 = group12.sum()
perc12 = (100*sums12['flights.delayed']/sums12['flights.total'])
q12 = perc12.groupby(level=0, group_keys=False).nlargest(1).sort_values()

"""
## 12.

Aloha Airlines Inc.           San Diego International                    14.065934
Alaska Airlines Inc.          San Francisco International                25.608819
Delta Air Lines Inc.          Newark Liberty International               30.238796
American Airlines Inc.        Newark Liberty International               31.755309
Southwest Airlines Co.        LaGuardia                                  31.910427
Hawaiian Airlines Inc.        San Francisco International                32.054795
Continental Air Lines Inc.    John F. Kennedy International              32.818352
United Air Lines Inc.         Fort Lauderdale-Hollywood International    33.462282
US Airways Inc.               Newark Liberty International               33.904404
American Eagle Airlines Inc.  Newark Liberty International               34.420821
Mesa Airlines Inc.            John F. Kennedy International              35.571429
AirTran Airways Corporation   Newark Liberty International               36.344417
JetBlue Airways               Newark Liberty International               36.389224
Frontier Airlines Inc.        LaGuardia                                  38.845144
Comair Inc.                   Newark Liberty International               41.536214
Northwest Airlines Inc.       Newark Liberty International               42.883951
ExpressJet Airlines Inc.      John F. Kennedy International              46.308725
Pinnacle Airlines Inc.        Orlando International                      57.692308
SkyWest Airlines Inc.         Logan International                        71.428571
Atlantic Southeast Airlines   Portland International                     86.666667

visible (0.5 pt): check type = Series
visible (0.5 pt): check index type = MultiIndex
hidden (3 pts): check Series
"""


