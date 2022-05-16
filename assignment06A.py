##
## File: assignment06-solutions.py (STAT 3250)
## Topic: Assignment 6 Solutions
##

##  The questions this assignment are based on "timing_log.txt".
##  The file "timing_log.txt" contains a log of all WeBWorK
##  log entries on April 1, 2011  The entries are organized 
##  by line, with each line including the following:
##
##  --the date and time of the entry
##  --a number that is related to the user (but is not unique)
##  --something that appears to be the epoch time stamp
##  --a hyphen
##  --the "WeBWorK element" that was accessed
##  --the "runTime" required to process the problem
##
##  Note: Some or all of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). As usual, scoring 
##  will take this into account.

##  Note: The solutions below we run on the data set 'timing_log_reduced.txt'
##  that was used by the autograder.  Run your file on this data set in order
##  to compare your answers to those below.

import numpy as np # load numpy as np
import pandas as pd # load pandas as pd

# Read in the data from 'timing_log.txt' one line at a time, with each
# line a single string in the Series 'loglines'

loglines = open('timing_log.txt').read().splitlines()
loglines = pd.Series(loglines) # convert list to Series


## 1.  How many log entries were for requests for a PDF version of an
##     assignment?  Those are indicated by "hardcopy" appearing in the 
##     WeBWorK element.

# Use vectorization to examine each line for the word 'hardcopy'
# then count the number of True's.
q1 = loglines.str.contains('hardcopy').sum()

"""
# 1.
40  # Number of log entries that contain 'hardcopy'

""" 


## 2.  What percentage of log entries involved a Spring '12 section of MATH 1320?

# Use vectorization to examine each line for the string 'Spring12-MATH1320',
# count the number of True's, and divide by number of log entries.
ct2 = loglines.str.contains('Spring12-MATH1320').sum()
q2 = 100*ct2/len(loglines)

"""
# 2.
3.2035614525139664  # Percentage of log entries that involve Spring '12 section of MATH 1320

"""


## 3. How many different classes use the system? Treat each different name 
##    as a different class, even if there is more than one section of a course.  

# In several questions that follow it will be useful to have a series
# made up of elements that are lists of the components of the WeBWorK
# element in each line of 'loglines'.  Here we create that series.

# Start by extracting the WeBWorK element
wwels = loglines.str.split().str[8]

# Every WeBWorK element starts with '[/' and ends with ']'.  Remove those:
wwels = wwels.str[2:].str[:-1]

# Some WeBWorK elements have 2nd-to-last character '/' but others do not.
# We test for these and remove them when present
wwels[wwels.str[-1]=='/'] = wwels.str[:-1]

# Finally, create series of lists from WeBWorK elements
wwellists = wwels.str.split('/')  # This is the series of lists

# Starting with 'wwellists' defined above, we extract all lists with
# length greater than 1, extract the second item from each of these lists, 
# remove the duplicates, and count the number remaining.
q3 = len(np.unique(wwellists[wwellists.str.len() > 1].str[1]))  
                        
    
"""
# 3.
32

"""


## 4.  Find the percentage of log entries that came from an initial
##     log in.  For those, the WeBWorK element has the form
##
##          [/webwork2/ClassName] or [/webwork2/ClassName/]
##
##     where "ClassName" is the name of a class.   

# For this question we count the number of lists in 'wwellists'
# defined above that have length equal to 2, divide by the total
# number of log entries, and multiply by 100
q4 = 100*np.sum(wwellists.str.len() == 2)/len(loglines)

"""
# 4.
3.884427374301676  # Percentage of entries for initial log in

"""


## 5.  Determine the percentage of log entries for each section of MATH 1310
##     from Spring 2012, among the total number of log entries for MATH 1320,
##     Spring 2012.  Give the percentages as a Series with class name as
##     index and percentages as values, sorted by percentage largest to smallest.
##     (The class name should be of the form 'Spring12-MATH1310-InstructorName')

# Start by extracting lists with at least two components
temp5 = wwellists[wwellists.str.len()>1]

# Next extract 2nd component when it contains both 'MATH1310' and 'Spring12'
ser5 = temp5[(temp5.str[1].str.contains('MATH1310')) & (temp5.str[1].str.contains('Spring12'))].str[1]

# Count values, divide by the number of entries in 'ser5' and multiply by 100
q5 = 100*ser5.value_counts()/len(ser5)

"""
## 5.

Spring12-MATH1310-Droms       55.825243
Spring12-MATH1310-Schwartz    24.271845
Spring12-MATH1310-Wishne      19.902913

"""


## 6.  How many log entries were from instructors performing administrative
##     tasks?  Those are indicated by "instructor" in the 3rd position of
##     the WeBWorK element.  Give a table of counts for all classes with 
##     such activity, sorted largest to smallest.

# Start by extracting lists with at least three components
temp6 = wwellists[wwellists.str.len()>2]

# We check each list in 'temp6' to determine which has 'instructor'
# in the 3rd position, then count the Trues
q6 = np.sum(temp6.str[2] == 'instructor')

"""
# 6.
92  # The number of entries with 'instructor' as 3rd WeBWorK element

"""


## 7.  Find the number of log entries for each hour of the day. Give the
##     counts for the top-5 (plus ties as usual) as a Series, with hour of day
##     as index and the count as values, sorted by count from largest to 
##     smallest.

# Split each line on spaces, extract the time, split on ':', then extract
# the hour.
hourseries = loglines.str.split().str[3].str.split(":").str[0]

# Count the number of times each hour appears; extract top-5 plus ties
cts7 = hourseries.value_counts() 
q7 = cts7[cts7 >= cts7.iloc[4]]

"""
## 7.

22    1900  #  Top-5 hours in terms of log entries plus counts
21    1874
16    1800
17    1705
23    1678

"""


## 8.  Find the number of log entries for each minute of each hour of the day. 
##     Give the counts for the top-8 (plus ties as usual) as a Series, with 
##     hour:minute pairs as index and the count as values, sorted by count 
##     from largest to smallest.  (An example of a possible index entry
##     is 15:47)

# Split each line on spaces, extract the time, then extract hour:min
hourminseries = loglines.str.split().str[3].str[0:5]

# Count the number of times each hour:min appears
cts8 = hourminseries.value_counts()
q8 = cts8[cts8 >= cts8.iloc[7]]

"""
## 8.

20:35    51 # Top-8 hour:min combinations with counts
16:56    51
17:58    50
22:00    49
18:05    49
16:26    48
21:41    48
21:08    48
22:02    48

"""


## 9. Determine which 5 classes had the largest average "runTime".  Give a 
##    Series of the classes and their average runTime, with class as index
##    and average runTime as value, sorted by value from largest to smallest.

# Extract the runtimes (12th position after split()) then convert to floating
# point for averaging 
runtimes = loglines.str.split().str[11].astype(float)

# Extract the lists with at least two components
temp9 = wwellists[wwellists.str.len()>1]

# Group the runtimes by class, compute the mean for each group, then sort
q9 = runtimes.groupby(temp9.str[1]).mean().sort_values(ascending=False)[0:5]

"""
## 9.

Fall11-APMA2130-Morris       0.690000 # Top 5 by average runtime
APMA2120-Devel               0.450469
apma2130-devel               0.430833
Spring12-APMA2130            0.341939
Spring11-APMA2130-Fulgham    0.280005

"""


## 10. Determine the percentage of log entries that were accessing a problem.  
##     For those, the WeBWorK element has the form
##
##           [/webwork2/ClassName/AssignmentName/Digit]
##     or
##           [/webwork2/ClassName/AssignmentName/Digit/]
##
##     where "ClassName" is the name of the class, "AssignmentName" the
##     name of the assignment, and "Digit" is a positive digit.

# Extract the lists with at exactly four components
temp10 = wwellists[wwellists.str.len() == 4]

# Now determine how many of 'temp10' have a digit for a 4th component
# (not all do), divide by the length of 'loglines' and multiply by 100
q10 = 100*np.sum(temp10.str[3].str.isdigit())/len(loglines)
 
"""
# 10.

78.36504888268156  # Percentage of log entries accessing a problem

""" 


## 11. Find the top-10 (plus tied) WeBWorK problems that had the most log entries,
##     and the number of entries for each (plus ties as usual).  Sort the 
##     table from largest to smallest.
##     (Note: The same problem number from different assignments and/or
##     different classes represent different WeBWorK problems.) 
##     Give your answer as a Series with index entries of the form
##
##          ClassName/AssignmentName/Digit
##
##     and counts for values, sorted by counts from largest to smallest.

# Extract the lists with at least four components
temp11 = wwellists[wwellists.str.len()>3]

# Now extract the subset with 4th component a digit
temp11 = temp11[temp11.str[3].str.isdigit()]

# Form up the combinations 'ClassName/AssignmentName/Digit'
probs = temp11.str[1]+'/'+temp11.str[2]+'/'+temp11.str[3]

# Count the values, print the top 10 plus ties
cts11 = probs.value_counts()
q11 = cts11[cts11 >= cts11.iloc[9]]

"""
## 11.

Spring11-STAT2120/Webwork09/22              366
Spring11-APMA2130-Fulgham/2130_Quiz_09/5    359
Spring11-STAT2120/Webwork09/20              352
Spring11-STAT2120/Webwork09/24              343
Spring11-APMA2130-Fulgham/2130_Quiz_09/7    341
Spring11-STAT2120/Webwork09/25              337
Spring11-STAT2120/Webwork09/18              333
Spring11-STAT2120/Webwork09/23              323
Spring11-STAT2120/Webwork09/19              294
Spring11-STAT2120/Webwork09/1               293

"""

