##
## File: assignment07-solns.py (STAT 3250)
## Topic: Assignment 7 Solutions
##

##  This assignment requires the data file 'movies.txt'.  This file
##  contains records for nearly 3900 movies, including a movie ID number, 
##  the title (with year of release, which is not part of the title), and a 
##  list of movie genre classifications (such as Romance, Comedy, etc).  Note
##  that a given movie can be classified into more than one genre -- for
##  instance Toy Story is classified as "Animation", "Children's", and 
##  "Comedy". 

##  Note: The solutions below we run on the data set 'movies-reduced.txt'
##  that was used by the autograder.  Run your file on this data set in order
##  to compare your answers to those below.


import numpy as np # load numpy as np
import pandas as pd # load pandas as pd

# Read in the movie data as text
movielines = pd.Series(open('movies.txt', encoding = 'utf8').read().splitlines())

# Below we harvest the information into a number of pandas Series for later
# use.  This could all be loaded into a dataframe, but that wasn't necessary
# to answer the questions in this assignment, so did not do that.

# The exact movie titles with the included years
titleswithyears = movielines.str.split("::").str[1] # extract titles w/ years

# The release years are extracted and put into their own Series, then
# converted to type 'float' so that we can do math (averaging, etc) on them.
years = titleswithyears.str[-5:-1].astype(int) # years always in same place 

# Here we extract the titles without the years.
titles = titleswithyears.str[:-7] # the titles all end at the same place

# It turns out having the genres in two forms is handy later on.  One form
# is as the original string with genres separated by '|' and the other is 
# as a list of genres.
genrestrings = movielines.str.split("::").str[2] # genres for each movie, as string
genrelists = genrestrings.str.split('|') # list of genres for each movie


## 1.  Determine the number of movies included in genre "Animation", the number
##     in genre "Horror", and the number in both "Comedy" and "Crime".

q1a = np.sum(genrestrings.str.contains('Animation'))  # Genre includes Animation
q1b = np.sum(genrestrings.str.contains('Horror')) # Genre includes Horror

# Genre includes both Comedy and Crime
q1c = np.sum(genrestrings.str.contains("Comedy") & genrestrings.str.contains('Crime'))

"""
## 1.

73  # 'Animation'
240  # 'Horror'
30   # "Comedy" and "Crime"

"""

## 2.  Among the movies in the genre "Horror", what percentage have the word
##     "massacre" in the title?  What percentage have 'Texas'? (Upper or lower
##     cases are allowed here.) 

horrortitles = titles[genrestrings.str.contains('Horror')] # extract Horror titles

# the percentage that includes the string 'massacre'
q2a = 100*np.sum(horrortitles.str.lower().str.contains('massacre'))/len(horrortitles)

# the percentage that includes the string 'texas'
q2b = 100*np.sum(horrortitles.str.lower().str.contains('texas'))/len(horrortitles)

"""
## 2.
1.25  # percentage Horror that includes 'massacre'
0.8333333333333334 # percentage Horror that includes 'texas'

"""

## 3.  Among the movies with exactly one genre, determine the genres that
##     have at least 50 movies classified with that genre.  Give a Series 
##     with genre as index and counts as values, sorted largest to smallest 
##     by count.

# extract genre lists of length 1, extract the genre, apply volue_counts,
# the display the top-5.
s3 = genrelists[genrelists.str.len() == 1].str[0].value_counts()
q3 = s3[s3>=50] # extract genres with counts >= 50

"""
## 3.

Drama          602
Comedy         372
Horror         123
Documentary     82
Thriller        75

"""

## 4.  Determine the number of movies that have 1 genre, 2 genres, 3 genres, 
##     and so on.  Give your results in a Series, with the number of genres
##     as the index and the counts as values, sorted by index values from
##     smallest to largest. 

# Find the length of each genre list, then use value_counts to summarize
q4 = genrelists.str.len().value_counts()  # Series of number of genres and counts

"""
## 4.

1    1436
2     934
3     293
4      70
5       8

"""

## 5.  How many remakes are in the data? We say a movie is a remake if the title is
##     exactly the same as the title of an older movie. For instance, if 'Hamlet'  
##     is in the data set 4 times, then 3 of those should be counted as remakes.
##     (Note that a sequel is not the same as a remake -- "Jaws 2" is completely
##     different from "Jaws".)

# Apply np.unique to the set of titles. The total number of titles minus
# the total number of unique titles is the number of remakes.
q5 = len(titles) - len(np.unique(titles))

"""
## 5.

20

"""

## 6.  Determine for each genre the percentage of movies in the data set that
##     are classified as that genre.  Give a Series of all with 8% or more,
##     with genre as index and percentage as values, sorted from highest to 
##     lowest percentage. (Include ties for 5th as usual)

# Combine the genre lists into one big list, convert to Series, apply 
# value_counts, then divide by len(titles) & mutiply by 100 to get percentage
#
# instead of sum(genrelists,[]) you could also try genrelists.sum() or genrelists.explode() 
s6 = 100*pd.Series(sum(genrelists,[])).value_counts()/len(titles)
q6 = s6[s6 >= 8]  # Extract the genres >= 8%


"""
## 6.

Drama       41.955491
Comedy      31.120029
Thriller    12.623130
Romance     12.550164
Action      12.367749
Horror       8.755928

"""


## 7.  It is thought that musicals have become less popular over time.  We 
##     judge that assertion here as follows: Compute the median release year 
##     for all movies that have genre "Musical", and then do the same for all
##     other movies.  

# extract the release years for 'Musical' genre and compute median
q7a = years[genrestrings.str.contains('Musical')].median()
q7b = years[~genrestrings.str.contains('Musical')].median() #the same, non-Musical

"""
## 7.

1968.0 # median, musicals
1994.0 # median, all others

"""

##  8. Determine how many movies came from each decade in the data set.
##     An example of a decade: The years 1980-1989, which we would label as
##     1980.  (Use this convention for all decades in the data set.) 
##     Give your answer as a Series with decade as index and counts as values,
##     sorted by decade 2000, 1990, 1980, ....

# years % 10 gives the remainder of the year when divided by 10, so
# years - years % 10 gives the decade
decades = (years - years % 10) # this contains the decade for each movie
q8 = decades.value_counts().sort_index(ascending=False) # counts of decades, sorted by decade

"""
## 8.

2000     119
1990    1645
1980     417
1970     161
1960     129
1950     108
1940      84
1930      52
1920      24
1910       2

"""

##  9. For each decade in the data set, determine the percentage of titles
##     that have exactly one word.  (Note: "Jaws" is one word, "Jaws 2" is not)
##     Give your answer as a Series with decade as index and percentages as values,
##     sorted by decade 2000, 1990, 1980, ....

# from #8 above
# years % 10 gives the remainder of the year when divided by 10, so
# years - years % 10 gives the decade
decades = (years - years % 10) # this contains the decade for each movie
denom = decades.value_counts().sort_index(ascending=False) # counts of decades, sorted by decade

# identify titles with length greater than 1; extract the corresponding decade;
# count the number of each decade and subtract from denom to get number of
# 1-word titles by decade
numer = denom - decades[titles.str.split().str.len() > 1].value_counts().sort_index(ascending=False)

q9 = 100*numer/denom  # percentage 1-word titles by decade

"""
## 9.

2000    15.966387
1990    18.480243
1980    19.184652
1970    19.254658
1960    12.403101
1950     9.259259
1940    21.428571
1930    17.307692
1920    12.500000
1910     0.000000

"""

## 10. For each genre, determine the percentage of movies classified in
##     that genre also classified in at least one other genre.  Give your 
##     answer as a Series with genre as index and percentages as values, 
##     sorted largest to smallest percentage.

genres = np.unique(np.array(sum(genrelists,[]))) # array of genres
s10 = pd.Series(0.0, index=genres) # initialize Series with index=genres

genrelists = genrestrings.str.split('|') # list of genres for each movie
genrestrings = movielines.str.split("::").str[2] # genres for each movie, as string
genrects = pd.Series(sum(genrelists,[])).value_counts() # counts of genres

for genre in genrects.index:
   genrelocs = genrestrings.str.contains(genre) # find records with genre
   ct = sum(genrelists[genrelocs].str.len() > 1) # count number with > 1 genre
   s10[genre] = 100.0*ct/genrects[genre]  # Compute percentage, put in s10
    
q10 = s10.sort_values(ascending=False) # sort entries in s10 by percentage

   
"""
## 10.

Children's     98.757764
Fantasy        97.727273
Animation      97.260274
Adventure      93.908629
War            93.069307
Romance        92.151163
Mystery        89.610390
Sci-Fi         89.385475
Action         88.200590
Crime          87.012987
Musical        84.415584
Thriller       78.323699
Film-Noir      77.777778
Comedy         56.389215
Western        50.943396
Horror         48.750000
Drama          47.652174
Documentary     6.818182

"""

