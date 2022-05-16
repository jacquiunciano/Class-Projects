##
## File: assignment05-solutions.py (STAT 3250)
## Topic: Assignment 5 Solutions
##

##  This assignment requires the data file 'diabetic_data.csv'.  This file
##  contains records for over 100,000 hospitalizations for people who have
##  diabetes.  The file 'diabetic_info.csv' contains information on the
##  codes used for a few of the entries.  Missing values are indicated by
##  a '?'.  You should be able to read in this file using the usual 
##  pandas methods.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the diabetic_data.csv data that includes about 35% of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values. 

##  Note: Many of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). Scoring will take
##  this into account.

##  Note: The solutions below we run on the data set 'diabetic_data_reduced.csv'
##  that was used by the autograder.  Run your file on this data set in order
##  to compare your answers to these.


import numpy as np # load numpy as np
import pandas as pd # load pandas as pd

dia = pd.read_csv('diabetic_data_reduced.csv')

## 1.  Determine the average number of procedures ('num_procedures') for 
##     those classified as females and for those classified as males.

# groupby the gender, compute the means, and extract female and male only
numprocs = dia['num_procedures'].groupby(dia['gender']).mean()  

q1f = numprocs['Female']  # female average number of procedures
q1m = numprocs['Male']  # male average number of procedures

"""
## 1.

gender
Female    1.220463  # average number of procedure, by gender classification
Male      1.460613
"""


## 2.  Determine the average length of hospital stay ('time_in_hospital')
##     for each race classification.  (Omit those unknown '?' but include 
##     those classified as 'Other'.)  Give your answer as a Series with
##     race for the index sorted alphabetically.

# groupby race, compute the means, extract all but those with '?'
avelength = dia['time_in_hospital'].groupby(dia['race']).mean()[1:]

q2 = avelength  # Series of average length of stay by race

"""
## 2.

race
AfricanAmerican    4.511514  # table of length of stay by race
Asian              4.009217
Caucasian          4.372311
Hispanic           4.045386
Other              4.312236
"""

## 3.  Determine the percentage of total days spent in the hospital due to
##     stays ("time_in_hospital") of at least 7 days. (Do not include the %
##     symbol in your answer.)

# Identify records for stays >7 days, then sum up stay times
longstaytot = np.sum(dia.loc[dia['time_in_hospital'] >= 7,'time_in_hospital'])
perc3 = 100*longstaytot/np.sum(dia['time_in_hospital']) # percentage of days >= 7

q3 = perc3  # percentage of days from stays of at least 7 days

"""
## 3.

43.431464796550394 # percentage of days due to stays >= 7 days
"""


## 4.  Among the patients in this data set, what percentage had at least
##     three recorded hospital visits?  Each distinct record can be assumed 
##     to be for a separate hospital visit. Do not include the % symbol in
##     your answer.

numpats = len(np.unique(dia['patient_nbr'])) # number of distinct patients
# number of patients that had more than three hospital visits
numpatsatleastthree = np.sum(dia['patient_nbr'].value_counts()>=3)

q4 = 100*numpatsatleastthree/numpats # percentage patients with more than three visits

"""
## 4.

2.7296059933407326  # percentage of patients with at least visits
"""


## 5.  List the top-15 most common diagnoses, based on the codes listed 
##     collectively in the columns 'diag_1', 'diag_2', and 'diag_3'.
##     Give your response as a Series with the diagnosis code as the 
##     index and the number of occurances as the values, sorted by
##     values from largest to smallest.  If more than one value could
##     go in the 15th position, include all that could go in that 
##     position.  (This is the usual "include ties" policy.)

# Convert columns to list, concatenate, then convert to Series
alldiags = pd.Series(list(dia['diag_1']) + list(dia['diag_2']) + list(dia['diag_3']))
cutval = alldiags.value_counts().iloc[14] # find cut-off value
top15 = alldiags.value_counts()[alldiags.value_counts() >= cutval] # top 15 + ties

q5 = top15  # top-15 diagnoses plus any ties

"""
## 5.

428    6006  # table of top-15 diagnosis codes (code left, count right)
250    5942
276    4550
414    4195
401    4064
427    3849
599    2267
496    2004
403    1950
486    1857
786    1746
780    1567
491    1509
410    1442
682    1411
"""


## 6.  The 'age' in each record is given as a 10-year range of ages.  Assume
##     that the age for a person is the middle of the range.  (For instance,
##     those with 'age' [40,50) are assumed to be 45.)  Determine the average
##     age for each classification in the column 'acarbose'.  Give your
##     answer as a Series with the classification as index and averages as
##     values, sorted from largest to smallest average.

def midage(agerange):  # function to convert the age ranges into mean age
    y = agerange.split('[')[1].split(')')[0].split('-') # chop up '[ , )'
    return((float(y[1]) + float(y[0]))/2)  # return middle of range
# Note: a function that uses if/elif/elif... to convert the age ranges
# into an age is fine too.
    
dia['C6'] = dia['age'].apply(midage) # apply 'midage' to column 'age' for new col.
group6 = dia['C6'].groupby(dia['acarbose']) # group by 'acarbose'

q6 = group6.mean().sort_values(ascending=False) # mean of 'C6'
    
"""
## 6.

acarbose
Down      85.000000  # Series of mean age for each 'acarbose' classification
Steady    67.989691
No        65.967271
Up        65.000000
"""


## 7.  Determine all medical specialties that have an average hospital stay
##     (based on time_in_hospital) of at least 7 days.  Give a Series with
##     specialty as index and average hospital stay as values, sorted from
##     largest to smallest average stay.

# Group time_in_hospital by medical_specialty
group7 = dia['time_in_hospital'].groupby(dia['medical_specialty'])

# Extract the entries with mean >= 7, then sort on means
q7 = group7.mean()[group7.mean() >= 7].sort_values(ascending=False)

"""
## 7.

medical_specialty
Rheumatology                         9.400000
PhysicalMedicineandRehabilitation    8.804688
Pediatrics-Pulmonology               8.100000
Pathology                            7.750000
"""


##  8. Three medications for type 2 diabetes are 'glipizide', 'glimepiride',
##     and 'glyburide'.  There are columns in the data for each of these.
##     Determine the number of records for which at least two of these
##     are listed as 'Steady'.

# Define a T/F Series for 'Steady' in each medication column; it's more compact
med1 = (dia['glipizide'] == 'Steady')
med2 = (dia['glimepiride'] == 'Steady')
med3 = (dia['glyburide'] == 'Steady')

# Check if any of the pairs are both True; sum to count total
q8 = np.sum((med1 & med2) | (med1 & med3) | (med2 & med3))

# Alternate solution: 1* a T/F Series converts it to 1/0; then we can add
# the new Series, and count number of entries >= 2
medct = 1*med1 + 1*med2 + 1*med3
np.sum(medct >= 2)

"""
## 8.

97  # number of records with at least 2 of 3 listed as 'Steady'
"""


##  9. Find the percentage of "time_in_hospital" accounted for by the top-100 
##     patients in terms of number of times in file.  (Include all patients 
##     that tie the 100th patient.)

# Groupby patient number, then count to find the number of times each patient
# appears in the data.
groupX2 = dia['patient_nbr'].groupby(dia['patient_nbr'])
patientcts = groupX2.count().sort_values(ascending=False)

cutoffct = patientcts.iloc[100] # number of times in data for 100th patient
# The set of patient numbers that appear in data >= cutoffct times
top100pats = patientcts.index[patientcts >= cutoffct]

# Identify stay times for records of the patients in top100pats set
top100pattimes = dia.loc[dia['patient_nbr'].isin(top100pats),'time_in_hospital']

# Calculate the percentage of total stay times for top-100 patients out of
# the total of all stay times.
q9 = 100*np.sum(top100pattimes)/np.sum(dia['time_in_hospital'])

"""
## 9.

3.7284991910754295  # Percentage of stay times accounted for by top-100 pats
"""


## 10. What percentage of reasons for admission ('admission_source_id')
##     correspond to some form of transfer from another care source?

transcodes = [4,5,6,10,18,22,25,26] # transfer codes from 'diabetic_info'

# Not all transfer codes appear in the data set, so we take the intersection
# of all transfer codes with the 'admission_source_id' to determine which
# to count.
translist = np.intersect1d(np.unique(dia['admission_source_id']),transcodes)

# count number of each admission code, extract totals for the transfer list
# then sum the to get the total number from transfers
transct = dia['admission_source_id'].value_counts()[translist].sum()

q10 = 100*transct/len(dia) # compute percentage of admission by transfer

"""
## 10.

6.288411864255812  # percentage of reasons corresponding to transfer
"""


## 11. The column 'discharge_disposition_id' gives codes for discharges.
##     Determine the 5 codes that resulted in the greatest rate of
##     readmissions.  Give your answer as a Series with discharge code
##     as index and readmission percentage as value, sorted by percentage
##     from largest to smallest.

dia['C11'] = 1 # New column with all 1's
dia.loc[dia['readmitted']=='NO','C11'] = 0 # set 'C11' to 0 when readmit = NO

# Count of each discharge code
dischargects = dia['C11'].groupby(dia['discharge_disposition_id']).count()

# Using 'sum' on 'C11' effectively counts the number of readmits by adding
# up the 1's that appear in the readmit rows.  Thus groupby gives the
# number of readmits for each discharge code.
readmitcts = dia['C11'].groupby(dia['discharge_disposition_id']).sum()

q11 = (100*readmitcts/dischargects).sort_values(ascending=False).iloc[:5]

"""
## 11.

10   100.000000  # The top-5 discharge codes in terms of percentage of 
27   100.000000  # readmits per code
16    75.000000
28    65.909091
15    63.157895
"""


## 12. The columns from 'metformin' to 'citoglipton' are all medications, 
##     with "Up", "Down", and "Steady" indicating the patient is taking that 
##     medication.  For each of these medications, determine the average
##     number of medications from this group that patients are taking.
##     Give a Series of all medications with an average of at least 1.5,
##     with the medications as index and averages as values, sorted 
##     largest to smallest average.
##     (Hint: df.columns gives the column names of the data frame df.)

# Start by creating a 0/1 dataframe with columns from the specified meds
# converted to 1 if any of 'Up'/'Down'/'Steady' present, 0 otherwise.
meds = dia.loc[:,'metformin':'citoglipton'].copy() # copy of meds columns
medseries = pd.Series(0, index=meds.columns) # series with meds as index
def medconv(s):  # Function to convert strings to 0/1 to indicate med use
    if (s == 'Up') or (s == 'Down') or (s == 'Steady'):
        return(1)
    else:
        return(0)
for med in meds.columns:
    meds[med] = meds[med].apply(medconv) # loop does the converting to 0/1

meds['medct'] = np.sum(meds, axis=1) # Add a column that gives count of meds

for med in medseries.index:   # Loop to access one column at a time
    cts = meds.loc[meds[med] == 1, 'medct']  # Extract 'medct' values for med
    medseries.loc[med] = np.mean(cts)  # Save the mean into Series 'medseries'
    
q12 = medseries[medseries > 1.5].sort_values(ascending=False) # sorted series of meds and means

"""
## 12.

miglitol         2.400000 # Table of medications and mean cts for each
acarbose         2.186275
rosiglitazone    1.787518
nateglinide      1.747706
pioglitazone     1.743917
metformin        1.690259
repaglinide      1.592292
glyburide        1.583520
glimepiride      1.561454
glipizide        1.525635
"""