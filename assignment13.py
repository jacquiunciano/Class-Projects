# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 15:35:17 2022

@author: jacqu
"""

##
## File: assignment13.py (STAT 3250)
## Topic: Assignment 13 
##


##  These questions are similar to reviewed lecture material, but 
##  provide some experience with Dask.

import dask.dataframe as dd #import libraries
import numpy as np
# import pandas as pd

dtypes = {
 'Date First Observed': str, 'Days Parking In Effect    ': str,
 'Double Parking Violation': str, 'Feet From Curb': np.float32,
 'From Hours In Effect': str, 'House Number': str,
 'Hydrant Violation': str, 'Intersecting Street': str,
 'Issue Date': str, 'Issuer Code': np.float32,
 'Issuer Command': str, 'Issuer Precinct': np.float32,
 'Issuer Squad': str, 'Issuing Agency': str,
 'Law Section': np.float32, 'Meter Number': str,
 'No Standing or Stopping Violation': str,
 'Plate ID': str, 'Plate Type': str,
 'Registration State': str, 'Street Code1': np.uint32,
 'Street Code2': np.uint32, 'Street Code3': np.uint32,
 'Street Name': str, 'Sub Division': str,
 'Summons Number': np.uint32, 'Time First Observed': str,
 'To Hours In Effect': str, 'Unregistered Vehicle?': str,
 'Vehicle Body Type': str, 'Vehicle Color': str,
 'Vehicle Expiration Date': str, 'Vehicle Make': str,
 'Vehicle Year': np.float32, 'Violation Code': np.uint16,
 'Violation County': str, 'Violation Description': str,
 'Violation In Front Of Or Opposite': str, 'Violation Legal Code': str,
 'Violation Location': str, 'Violation Post Code': str,
 'Violation Precinct': np.float32, 'Violation Time': str
}

nyc = dd.read_csv('nyc-parking-tickets2015.csv', dtype=dtypes, usecols=dtypes.keys())
# nyc1 = pd.read_csv("nyc-parking-tickets2015-SMALLTEST.csv")

## 1.  There are several missing values in the 'Vehicle Body Type' column. Impute 
##     missing values of 'Vehicle Body Type' with the mode. What is the mode?

q1 = (nyc["Vehicle Body Type"].value_counts().compute()).sort_values(ascending=False).index[0]
# Report the mode, the most common Vehicle Body Type.

# vbtm = nyc1["Vehicle Body Type"].value_counts().sort_values(ascending=False).index[0]
# =============================================================================
# # 'SUBN'
# =============================================================================

## 2.  How many missing data points are there in the 'Intersecting Street' column?

q2 = nyc["Intersecting Street"].isnull().sum().compute()
# Number of missing data points

# mdpts = nyc1["Intersecting Street"].isnull().sum()
# =============================================================================
# # 8565689
# =============================================================================

## 3.  What percentage of vehicle makes are Jeeps during the months of March - 
##     September (inclusive) of 2015?

## add new col with proper dt format
fmat = "%m/%d/%Y"
nyc["IssueDate"] = dd.to_datetime(nyc["Issue Date"], format=fmat)
## get just 2015 for issue date
j2015 = nyc[nyc["IssueDate"].dt.year==2015]
## get proper date range
jdates = j2015[(j2015["IssueDate"].dt.month>=3)&(j2015["IssueDate"].dt.month<=9)]
## get jeeps
j2 = jdates[jdates["Vehicle Make"]=="JEEP"]
q3 = 100*len(j2)/len(jdates)
# Percentage of Jeeps

# fmat = "%m/%d/%Y"
# nyc1["IssueDate"] = pd.to_datetime(nyc1["Issue Date"], format=fmat)
# j15 = nyc1[nyc1["IssueDate"].dt.year==2015]
# jdate = j15[(j15["IssueDate"].dt.month>=3)&(j15["IssueDate"].dt.month<=9)]
# j22 = jdate[jdate["Vehicle Make"]=="JEEP"]
# jper = 100*len(j22)/len(jdate)
# =============================================================================
# # 2.630800727640212
# =============================================================================

## 4.  What's the most common color of a car in 2015? Maintain the color in all caps.

q4 = (j2015["Vehicle Color"].value_counts().compute()).sort_values(ascending=False).index[0]
# Most common car color

# c2 = j15["Vehicle Color"].value_counts().sort_values(ascending=False).index[0]
# =============================================================================
# # 'GY'
# =============================================================================

## 5.  Find all the cars in any year that are the same color as q4. What percentage of 
##     those care are sedans?

## find all records with proper color
jc = nyc[nyc["Vehicle Color"]==q4]
## then find sedans
js = jc[jc["Vehicle Body Type"]=="SDN"]
q5 = 100*len(js)/len(jc)
# Percentage of sedans

# jc2 = nyc1[nyc1["Vehicle Color"]==c2]
# js22 = jc2[jc2["Vehicle Body Type"]=="SDN"]
# js2 = 100*len(js22)/len(jc2)
# =============================================================================
# # 2.5290764021183736
# =============================================================================

## 6.  Make a table of the top 5 registration states, sorted greatest to least.

rs = (nyc["Registration State"].value_counts().compute()).sort_values(ascending=False)
q6 = rs.nlargest(5)
# Series of top 5 registration states

# rst = nyc1["Registration State"].value_counts().sort_values(ascending=False).nlargest(5)
# =============================================================================
# # NY    9193289
# # NJ    1080414
# # PA     298877
# # CT     160361
# # FL     148868
# =============================================================================

## 7.  Perhaps someone bought a new vehicle and kept the same license plate. How many license 
##     plates have more than one 'Vehicle Make' associated with the respective plate?

## make new df with just the vm and pid
ndf = nyc[["Vehicle Make","Plate ID"]]
## get rid of dups
ndf2 = ndf.drop_duplicates()
## count how many times plate id shows up
pc = (ndf2["Plate ID"].value_counts().compute()).sort_index(ascending=False)
q7 = len(pc[pc>1])
# Number of license plates

# newdf = nyc1[["Vehicle Make","Plate ID"]]
# ndf = newdf.drop_duplicates()
# pc1 = ndf["Plate ID"].value_counts().sort_index(ascending=False)
# pc2 = len(pc1[pc1>1])
# =============================================================================
# # 166001
# =============================================================================

## 8.  Determine the top three hours that result in the most parking violations. 
##     "0011A" would be 12:11 AM and "0318P" would be 3:18 PM. Report the solution 
##     with the index in the format of "01A" and the count.

## make new col with proper format
nyc["Violation Times"] = nyc["Violation Time"].str[0:2]+nyc["Violation Time"].str[4]
vtimes = (nyc["Violation Times"].value_counts().compute()).sort_values(ascending=False)
q8 = vtimes.nlargest(3)
# Series with top three hours

# nyc1["Violation Times"] = nyc1["Violation Time"].str[0:2]+nyc1["Violation Time"].str[4]
# vtime = nyc1["Violation Times"].value_counts().sort_values(ascending=False)
# place_3 = vtime.iloc[2]
# vt22 = vtime[vtime>=place_3]
# t3 = vtime.nlargest(3)
# =============================================================================
# # 09A    1236856
# # 11A    1228632
# # 01P    1144072
# =============================================================================


## 9.  Among the tickets issued by Precinct 99, what is the average distance from the
##     curb in feet?

## get just p99
jp99 = nyc[nyc["Issuer Precinct"]==99]
q9 = jp99["Feet From Curb"].mean().compute()
# Average distance from the curb

# jp = nyc1[nyc1["Issuer Precinct"]==94]
# jpft = jp["Feet From Curb"].mean()
# =============================================================================
# # 0.3670886075949367
# =============================================================================
