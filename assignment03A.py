##
## File: assignment03-solns.py (STAT 3250)
## Topic: Assignment 3 Solutions
##

##  The questions in this assignment refer to the data in the
##  file 'absent.csv'.  The data contains 740 records from an
##  employer, with 21 columns of data for each record.  (There
##  are a few missing values indicated by zeros where zeros 
##  are clearly not appropriate.)  The file 'absent.pdf' has
##  a summary of the meanings for the variables.
##
##  All of these questions can be completed without loops.  You 
##  should try to do them this way, "code efficiency" will take 
##  this into account.

import numpy as np  # load numpy as np
import pandas as pd # load pandas as pd

absent = pd.read_csv('absent.csv')  # import the data set as a pandas dataframe

## 1.  Find the mean absent time among all records.

# Extract absenteeism column, compute mean
q1 = np.mean(absent['Absenteeism time in hours']) # mean of "Absenteeism" hours

"""
## 1.

6.924324324324324  # mean of "Absenteeism" hours
"""

## 2.  Determine the number of records corresponding to
##      being absent on a Thursday.

# test day of week == Thursday, count true
q2 = np.sum(absent['Day of the week'] == 5)

"""
## 2.

125  # Number of records for a Thursday
"""

## 3.  Find the number of unique employees IDs represented in 
##      this data.  

# remove duplicates from ID column, find length
q3 = len(np.unique(absent['ID'])) # find unique IDs, then return length of array

"""
## 3.

36  # Number of unique employee IDs
"""

## 4.  Find the average transportation expense for the employee with
##      ID = 34.

# extract trans expense for ID == 34, compute mean
q4 = np.mean(absent.loc[absent['ID']==34, 'Transportation expense'])

"""
## 4.

118
"""

## 5.  Find the total number of hours absent for the records
##      for employee ID = 11.

# extract times absent for ID == 11, compute sum
q5 = np.sum(absent.loc[absent['ID']==11, 'Absenteeism time in hours'])

"""
## 5.

450
"""

## 6.  Find (a) the mean number of hours absent for the records of those who 
##     have no pets, then (b) do the same for those who have more than one pet.

# extract time absent for no pets, compute mean; repeat for more than one pet
q6a = np.mean(absent.loc[absent['Pet']==0, 'Absenteeism time in hours']) # mean hours absent, no pet
q6b = np.mean(absent.loc[absent['Pet']>1, 'Absenteeism time in hours']) # mean hours absent, more than one pet

"""
## 6.

6.828260869565217  # mean absenteeism for those with 0 pets
5.21830985915493   # mean absenteeism for those with > 1 pets
"""

## 7.  Among the records for absences that exceeded 8 hours, find (a) the 
##      proportion that involved smokers.  Then (b) do the same for absences 
##      of no more then 4 hours.

over8ct = np.sum(absent['Absenteeism time in hours'] > 8) # number of records > 8 hours absent
# number of records > 8 hours absent and social smoker
smokover8ct = np.sum((absent['Absenteeism time in hours'] > 8) & (absent['Social smoker']==1))
print(smokover8ct/over8ct) 

under4ct = np.sum(absent['Absenteeism time in hours'] <= 4) # number of records <= 4 hours absent
# number of records <= 4 hours absent and social smoker
smokunder4ct = np.sum((absent['Absenteeism time in hours'] <=4) & (absent['Social smoker']==1))
print(smokunder4ct/under4ct)

q7a = smokover8ct/over8ct # proportion of smokers, absence greater than 8 hours
q7b = smokunder4ct/under4ct # proportion of smokers, absence no more than 4 hours

"""
## 7.

0.06349206349206349  # proportion of smokers among the records for absences > 8
0.06290672451193059  # proportion of smokers among the records for absences <= 4
"""

## 8.  Repeat Question 7, this time for social drinkers in place of smokers.

over8ct = np.sum(absent['Absenteeism time in hours'] > 8) # number of records > 8 hours absent
# number of records > 8 hours absent and social drinker
drinkover8ct = np.sum((absent['Absenteeism time in hours'] > 8) & (absent['Social drinker']==1))
print(drinkover8ct/over8ct)

under4ct = np.sum(absent['Absenteeism time in hours'] <= 4) # number of records <= 4 hours absent
# number of records <= 4 hours absent and social drinker
drinkunder4ct = np.sum((absent['Absenteeism time in hours'] <=4) & (absent['Social drinker']==1))
print(drinkunder4ct/under4ct)

q8a = drinkover8ct/over8ct # proportion of social drinkers, absence greater than 8 hours
q8b = drinkunder4ct/under4ct # proportion of social drinkers, absence no more than 4 hours


"""
## 8.

0.7301587301587301  # proportion of drinkers among the records for absences > 8
0.5336225596529284  # proportion of drinkers among the records for absences <= 4
"""

## 9.  Find the top-5 employee IDs in terms of total hours absent.  Give
##      the IDs and corresponding total hours absent as a Series with ID
##      for the index, sorted by the total hours absent from most to least.

# Group 'Absenteeism time in hours' column on employee 'ID'
IDgroup = absent['Absenteeism time in hours'].groupby(absent['ID']) 
IDsums = IDgroup.sum() # Generate Series of absent hours for each ID

# Sort IDsums on the total hours absent, identify value in 5th place
cutsum = IDsums.sort_values(ascending=False).iloc[4]
# Extract all values (sorted) that are >= cutsum (5th place value)
sortedIDsums = IDsums.sort_values(ascending=False)[IDsums >= cutsum]
print(sortedIDsums)  # print out the top-5

q9 = sortedIDsums  # Series of top-5 employee IDs in terms of total hours absent

"""
## 9.

ID            # Table of top-5 ID's and total hours absent
3     482
14    476
11    450
28    347
34    344
"""

## 10. Find the average hours absent per record for each day of the week.
##      Give the day number and average as a Series with the day number
##      as the index, sorted by day number from smallest to largest.

# Group 'Absenteeism time in hours' column on 'Day of the week'
DoWgroup = absent['Absenteeism time in hours'].groupby(absent['Day of the week']) 
DoWmeans = DoWgroup.mean() # Generate Series of mean absent hours for each day
print(DoWmeans)  # print table of means

q10 = DoWmeans  # Series of average hours absent by day of week.

"""
## 10

Day of the week  # Table of average hours absent by Day of Week
2    9.248447    # 2 = Monday, 3 = Tuesday, ...
3    7.980519
4    7.147436
5    4.424000
6    5.125000
"""

## 11. Repeat Question 10 replacing day of the week with month.

# Group 'Absenteeism time in hours' column on 'Month of absence'
Monthgroup = absent['Absenteeism time in hours'].groupby(absent['Month of absence']) 
Monthmeans = Monthgroup.mean() # Generate Series of mean absent hours for each month
print(Monthmeans.loc[1:12])  # print table of means; leave out Month=0

q11 = Monthmeans.loc[1:12]  # Series of average hours absent by day of week.

"""
## 11.

Month of absence  # Table of average hours absent by Month 
1      4.440000   # Month = 0 is left out; that is not a month, it's
2      4.083333   # an indicator that the value is missing.
3      8.793103
4      9.094340
5      6.250000
6      7.611111
7     10.955224
8      5.333333
9      5.509434
10     4.915493
11     7.507937
12     8.448980
"""

## 12. Find the top 3 most common reasons for absence for the social smokers.
##      Give the reason code and number of occurances as a Series with the 
##      reason code as the index, sorted by number of occurances from
##      largest to smallest.  (If there is a tie for 3rd place,
##      include all that tied for that position.)

smokedf = absent.loc[absent['Social smoker']==1,:] # dataframe of smokers

# Groupby "Reason for absence"; We need counts, so any column will do.
Smokegroup = smokedf['Reason for absence'].groupby(smokedf['Reason for absence'])

# Compile the table of counts, then sort in order of largest to smallest
counttable12a = Smokegroup.count().sort_values(ascending=False)

# Remove the entry with index = 0, which is not a reason for absence
counttable12a = counttable12a[counttable12a.index > 0]

cutval = counttable12a.iloc[2] # Identify value in 3rd place

# Extract table of counts >= the 3rd value
counttable12a = counttable12a[counttable12a>=cutval]

print(counttable12a) # print the table of counts

q12 = counttable12a  # Series of reason codes and counts

"""
## 12
Reason for absence  # Table of "Reason for absence" codes for smokers; 
25    7             # 0 is not included because it is an indication of
19    4             # a missing code.
18    4
28    4
22    4
23    4
"""

