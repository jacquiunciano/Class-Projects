##
## File: assignment08-solutions.py (STAT 3250)
## Topic: Assignment 8 Solutions
##

##  This assignment requires data from three files: 
##
##      'movies.txt':  A file of nearly 3900 movies
##      'reviewers.txt':  A file of over 6000 reviewers who provided ratings
##      'ratings.txt':  A file of over 1,000,000 movie ratings
##
##  The file 'readme.txt' has more information about these files.
##  You will need to consult the readme.txt file to answer some of the questions.

##  Note: Some or all of the questions on this assignment can be done without the 
##  use of loops, either explicitly or implicitly (apply). As usual, scoring 
##  will take this into account.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the movies.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.

##  Note: The solutions below we run on the data set 'movies-reduced.txt' and
##  'ratings-reduced.txt' that were used by the autograder.  Run your file on 
##  this data set in order to compare your answers to those below.


import pandas as pd # load pandas as pd
import numpy as np # load numpy

# Read in the data sets, starting with "movies.txt"
movietext = pd.Series(open('movies.txt', encoding='utf8').read().splitlines()).str.split("::")
moviedf = pd.DataFrame() # Dataframe for movie data
moviedf['MovieID'] = movietext.str[0] # Add columns for movie ID, title, and year
moviedf['TitlewYear'] = movietext.str[1]
moviedf['Title'] = movietext.str[1].str[:-6]
moviedf['ReleaseYear'] = movietext.str[1].str[-5:-1]
allgenres = np.unique(sum(movietext.str[2].str.split("|"),[])) # identify genres
for genre in allgenres:
    moviedf[genre] = movietext.str[2].str.contains(genre) # new T/F column for each genre
    
# Next read in "reviewers.txt"
reviewertext = pd.Series(open('reviewers.txt', encoding='utf8').read().splitlines()).str.split("::")
reviewerdf = pd.DataFrame() # Dataframe for reviewer data
reviewerdf['ReviewerID'] = reviewertext.str[0]  # Add columns for reviewer ID, gender, age 
reviewerdf['Gender'] = reviewertext.str[1]      # code, occupation code, zip code, state
reviewerdf['AgeCode'] = reviewertext.str[2]
reviewerdf['OccuCode'] = reviewertext.str[3]
reviewerdf['ZipCode'] = reviewertext.str[4]
reviewerdf['State'] = reviewertext.str[5]

# We also need an "Age" for each reviewer.  We define a function to convert,
# then apply to add another column to the reviewer data frame.  Because there
# is no single rule, the values are hard-coded into the function.
def convertages(agecode):
    if agecode == "1":
        return(16)
    elif agecode == "18":
        return(21)
    elif agecode == "25":
        return(29.5)
    elif agecode == "35":
        return(39.5)
    elif agecode == "45":
        return(47)
    elif agecode == "50":
        return(52.5)
    else:
        return(60)

reviewerdf['Age'] = reviewerdf['AgeCode'].apply(convertages).astype(float)

# We will need the occupation titles, so we create a dataframe that will
# be merged with the reviewerdf
occutitles = ["other/not specified","academic/educator","artist","clerical/admin","college/grad student",
	       "customer service","doctor/health care","executive/managerial",
	       "farmer","homemaker","K-12 student","lawyer","programmer","retired",
	       "sales/marketing","scientist","self-employed","technician/engineer",
	       "tradesman/craftsman","unemployed","writer"]
occucodes = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
occudf = pd.DataFrame()
occudf['OccuCode'] = pd.Series(occucodes).astype(str)
occudf['OccuTitle'] = occutitles

reviewerdf = pd.merge(reviewerdf, occudf, on="OccuCode") # merge in occupation titles to reviewerdf

# Next we read in the ratings.txt data
ratingtext = pd.Series(open('ratings.txt', encoding='utf8').read().splitlines()).str.split("::")
ratingdf = pd.DataFrame()
ratingdf['ReviewerID'] = ratingtext.str[0]  # Add columns for ReviewerID, MovieID,
ratingdf['MovieID'] = ratingtext.str[1] # Rating, and Year (all we need)
ratingdf['Rating'] = ratingtext.str[2].astype(int)
ratingdf['RatingYear'] = pd.to_datetime(ratingtext.str[3],unit="s").dt.year   

# Finally we define "df" which is the merged combination of moviedf, reviewerdf
# and ratingdf.  
df = pd.merge(reviewerdf, ratingdf, on="ReviewerID")
df = pd.merge(df, moviedf, on="MovieID")
df.dtypes  # check the data types



## 1.  Based on the data in 'reviewers.txt': Determine the percentage of all 
##     reviewers that are female.  Determine the percentage of all reviewers in
##     the 35-44 age group.  Among the 18-24 age group, find the percentage 
##     of reviewers that are male.

q1a = 100*sum(reviewerdf['Gender']=="F")/len(reviewerdf)  # Percentage of female reviewers
q1b = 100*sum(reviewerdf['AgeCode']=="35")/len(reviewerdf) # Percentage age 35-44
# percentage of males reviewers in 18-24 age group
q1c = 100*sum((reviewerdf['Gender']=="M") & (reviewerdf['AgeCode']=="18"))/sum(reviewerdf['AgeCode']=="18")

"""
## 1.

28.294701986754966  # percentage of female reviewers
19.751655629139073  # percentage of reviewers age 35-44
72.98277425203989   # percentage of male reviewers among 18-24 age group

"""

## 2.  Give a year-by-year Series of counts for the number of ratings, with
##     the rating year as index and the counts as values, sorted by rating
##     year in ascending order.

q2 = ratingdf['RatingYear'].value_counts() # Series of rating counts by year rated

"""
## 2.

2000    647261  # count of number of ratings by year
2001     48434
2002     17129
2003      2401

"""

## 3.  Determine the average rating from female reviewers and the average  
##     rating from male reviewers.

q3a = df.loc[df['Gender']=="F",'Rating'].mean() # average rating for female reviewers
q3b = df.loc[df['Gender']=="M",'Rating'].mean() # average rating for male reviewers

"""
## 3.

3.620588683333051 # average rating for female reviewers
3.580116063362715 # average rating for male reviewers

"""

## 4.  Determine the number of movies that received an average rating of 
##     less than 1.75.  (Movies and remakes should be considered as
##     different.)

group04 = df['Rating'].groupby(df['TitlewYear']) # group on title, find the mean
q4 = sum(group04.mean() < 1.75)                  # count number with mean < 1.75

"""
## 4.

31  # number of movies with average rating = 1.0

"""

## 5.  Determine the number of movies listed in 'movies.txt' for which there
##     is no rating in 'ratings.txt'.  

allMovieIDs = moviedf['MovieID']  # all the movie IDs
ratedMovieIDs = np.unique(df['MovieID']) # IDs for rated movies
q5 = len(allMovieIDs) - len(ratedMovieIDs) # number of movies that were not rated

"""
## 5.

122 # the number of movies that were not rated

"""

## 6.  Among the ratings from male reviewers, determine the average  
##     rating for each occupation classification (including 'other or not 
##     specified'), and give the results in a Series sorted from highest to 
##     lowest average with the occupation title (not the code) as index.

df06 = df[df['Gender'] == "M"]
group06 = df06['Rating'].groupby(df06['OccuTitle']) # Group by occupation, then
q6 = group06.mean().sort_values(ascending=False)     # find mean of ratings

"""
## 6.

OccuTitle
retired                 3.751277 # average rating by occupation, male reviewers
scientist               3.681300
programmer              3.667748
doctor/health care      3.656280
sales/marketing         3.640465
clerical/admin          3.633731
technician/engineer     3.619117
lawyer                  3.598198
executive/managerial    3.597028
self-employed           3.594219
artist                  3.594209
academic/educator       3.582575
college/grad student    3.548502
K-12 student            3.544530
customer service        3.541003
tradesman/craftsman     3.517945
writer                  3.508070
other/not specified     3.496990
farmer                  3.481837
homemaker               3.466431
unemployed              3.422222

"""

## 7.  Determine the average rating for each genre, and give the results in
##     a Series with genre as index and average rating as values, sorted 
##     alphabetically by genre.

avebygenre = pd.Series(0.0, index = allgenres) # series for genre averages
for genre in allgenres:  # allgenres defined above in the preprocessing
    avebygenre[genre] = sum(df['Rating']*df[genre])/sum(df[genre])
q7 = avebygenre  

"""
## 7.

Action         3.529781  # Average rating by genre
Adventure      3.484924
Animation      3.700646
Children's     3.394881
Comedy         3.525340
Crime          3.729116
Documentary    3.970455
Drama          3.766022
Fantasy        3.341451
Film-Noir      4.108648
Horror         3.233479
Musical        3.683490
Mystery        3.649965
Romance        3.605585
Sci-Fi         3.453675
Thriller       3.577700
War            3.901075
Western        3.596102

"""

## 8.  For the reviewer age category, assume that the reviewer has age at the 
##     midpoint of the given range.  (For instance '35-44' has age (35+44)/2 = 39.5)
##     For 'under 18' assume an age of 16, and for '56+' assume an age of 60.
##     For each possible rating (1-5) determine the average age of the reviewers
##     giving that rating.  Give your answer as a Series with rating as index
##     and average age as values, sorted by rating from 1 to 5.

group08 = df['Age'].groupby(df['Rating']) # group on rating, compute the 
q8 = group08.mean()                       # mean of ages

"""
## 8.

Rating
1    31.755257  # average age for each rating
2    32.802787
3    33.800931
4    34.257081
5    34.348665

"""

## 9.  Find the top-5 states in terms of average rating.  Give as a Series
##     with the state as index and average rating as values, sorted from 
##     highest to lowest average.
##     Note: See the readme.txt file for information on what constitutes a
##     "state" for this assignment.

# Group on each state, then compute the mean for each group.  (Most of the 
# work for this question is done in the data processing at the top.)
group09 = df['Rating'].groupby(df['State'])
q9 = group09.mean().sort_values(ascending=False)[0:5]

"""
## 9.

State           # Highest average ratings by "State"
GU    4.289528  # "GU" is Guam  
MS    4.005025
AK    3.981846
AP    3.924242  # "AP" is a US military base in the Pacific
SC    3.814882

"""

## 10. For each age group, determine the occupation that gave the lowest 
##     average rating.  Give a Series that includes the age group code and 
##     occupation title as a multiindex, and average rating as values.  Sort  
##     the Series by age group code from youngest to oldest. 

# Group by both age and occupation title (occupation code is also fine here),
# compute the group means, then use code borrowed from Exam 2 to extract 
# the smallest value from each group.
group10 = df['Rating'].groupby([df['AgeCode'],df['OccuTitle']])
q10 = group10.mean().groupby(level=0, group_keys=False).nsmallest(1)

"""
## 10.

AgeCode  OccuTitle           
1        lawyer                  3.066667  # Highest occupation average rating
18       doctor/health care      3.235525  # by age category
25       unemployed              3.366426
35       farmer                  2.642045
45       college/grad student    3.280000
50       farmer                  3.437610
56       sales/marketing         3.291755

"""



