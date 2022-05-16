##
## File: assignment04-solutions.py (STAT 3250)
## Topic: Assignment 4 Solutions
##

##  This assignment requires the data file 'airline_tweets.csv'.  This file
##  contains records of over 14000 tweets and associated information related
##  to a number of airlines.  You should be able to read this file in using
##  the usual pandas methods.

import pandas as pd # load pandas as pd
import numpy as np  # load numpy as np

air = pd.read_csv('airline_tweets.csv')  # Read in the data set

## Questions 1-8: These questions should be done without the use of loops.

## 1.  Determine the number of tweets for each airline, indicated by the
##      name in the 'airline' column of the data set.  Give the airline 
##      name and corresponding number of tweets as a Series with airline
##      name as the index, sorted by tweet count from most to least.

group1 = air['airline'].groupby(air['airline']) # group on airline for counts
counts1 = group1.count().sort_values(ascending=False) # number of tweets for each airline
counts1 # the Series of airlines/counts

q1 = counts1
"""
## 1.

airline
American          2759  # Count of tweets by airline
JetBlue           2222
Southwest         2420
US Airways        2913
United            3822
Virgin America     504

visible (0 pts): check type
hidden (2 pts): check for match
"""


## 2.  For each airline's tweets, determine the percentage that are positive,
##      based on the classification in 'airline_sentiment'.  Give the airline 
##      name and corresponding percentage as a Series with airline
##      name as the index, sorted by percentage from largest to smallest

# start by extracting the positive tweets
subframe2 = air[air['airline_sentiment'] == 'positive'] 
# group on airline name; we're counting so column doesn't really matter
group2 = subframe2['airline_sentiment'].groupby(subframe2['airline'])
counts2 = group2.count()  # count of airlines in subframe
# Compute the percentage for each airline, sort by percentage
percents = (100*counts2/counts1).sort_values(ascending=False)

q2 = percents

"""
## 2.

airline
Virgin America    30.158730  # Percentage of negative tweets by airline
JetBlue           24.482448
Southwest         23.553719
United            12.872841
American          12.178325
US Airways         9.234466

visible (1 pts): check type
hidden (2 pts): check for match
"""


## 3.  Find all user names (in the 'name' column) with at least 25 tweets
##      along with the number of tweets for each.  Give the user names and
##      corresponding counts as a Series with user name as index, sorted
##      by count from largest to smallest

group3 = air['name'].groupby(air['name']) # group by user name
# Count for each user, extract those with at least 25 tweets, then sort
group3.count()[group3.count() >= 25].sort_values(ascending=False)

q3 = group3.count()[group3.count() >= 25].sort_values(ascending=False)

"""
## 3.

name
JetBlueNews    63 # Table of tweet counts for users with >= 25 tweets
kbosspotter    32
_mhertz        29
otisday        28
throthra       27

visible (0 pts): check type
hidden (2 pts): check for match
"""


## 4.  Determine the percentage of tweets from users who have more than five
##      tweets in this data set. (Note that this is not the same as the
##      percentage of users with more than five tweets.)

group4 = air['name'].groupby(air['name']) # group by user name
# Counts for each user, then extract those who have more than five tweets
morethan5 = group4.count()[group4.count() > 5] 
100*np.sum(morethan5)/len(air) # compute percentage of tweets from users with
                               # more than five tweets
                               
q4 = 100*np.sum(morethan5)/len(air)                              
                               
"""
## 4.

17.78688524590164  # percentage of tweets from users with more than five tweets

hidden (3 pts): check for match
"""                            


## 5.  Among the negative tweets, determine the four reasons are the most common.
##      Give the percentage among all negative tweets for each as a Series 
##      with reason as index, sorted by percentage from most to least

# start by grouping by reason for negative tweet
group5 = air['negativereason'].groupby(air['negativereason'])
group5cts = group5.count()  # Compute counts of negative reasons
# Compute percentages for each reason, then sort.
table05 = (100*group5cts.sort_values(ascending=False)/np.sum(group5cts))
# Find 4th most common reason, then extract all values >= to that percentage
table05 = table05[table05 >= table05.iloc[3]]

q5 = table05

"""
## 5.

negativereason
Customer Service Issue    31.706254  # percentages of negative reasons,
Late Flight               18.141207  # top-4 sorted in order
Can't Tell                12.965788
Cancelled Flight           9.228590

visible (0 pts): check type
hidden (3 pts): check for match
"""


## 6.  How many tweets include a link to a web site? (Indicated by the 
##      presence of "http" anywhere in the tweet.)



q6 = np.sum(air['text'].str.contains('http')) # look for 'http' then count

"""
## 6.

1173  # number of tweets with 'http' indicating a web link

hidden (3 pts): check for match
"""


## 7.  How many tweets include the word "air" (upper or lower case,
##      not part of another word)?

# Start by converting tweets to lower case, padding each end with a space,
# and removing any punctuation.
tweets = (" " + air['text'].str.lower() + " ").str.replace(r'[^\w\s]+', ' ', regex=True)
# Now check if each tweet contains the string ' air ' by itself, and then
# apply np.sum to count the number


q7 = np.sum(tweets.str.contains(' air ')) 

"""
## 7.

141  # Number of tweets containing the word 'air' (any case)

hidden (3 pts): check for match
"""


## 8.  How many times total does the word "help" appear in a tweet, either in
##      upper or lower case and not part of another word.

# Start by converting tweets to lower case, padding each end with a space,
# and removing any punctuation.
tweets = (" " + air['text'].str.lower() + " ").str.replace(r'[^\w\s]+', ' ', regex=True)
# Now count the times each tweet contains the string ' help ' by itself, and 
# then apply np.sum to count the total
 

q8 = np.sum(tweets.str.count(' help ')) 

"""
## 8.

872

hidden (3 pts): check for match
"""


## Questions 9-14: Some of these questions can be done without the use of 
##  loops, while others cannot.  It is preferable to minimize the use of
##  loops where possible, so grading will reflect this.
##
##  Some of these questions involve hashtags and @'s.  These are special 
##  Twitter objects subject to special rules.  For these problems we assume
##  that a "legal" hashtag:
##
##  (a) Starts with the "#" (pound) symbol, followed by letter and/or numbers 
##       until either a space or punctuation mark (other than "#") is encountered.
##   
##      Example: "#It'sTheBest" produces the hashtag "#It"
##
##  (b) The "#" symbol can be immediately preceded by punctuation, which is 
##       ignored. If "#" is immediately preceded by a letter or number then
##       it is not a hashtag.
##
##      Examples: "The,#dog,is brown"  produces the hashtag "#dog"
##                "The#dog,is brown" does not produce a hashtag
##                "#dog1,#dog2" produces hashtags "#dog1" and "#dog2"
##                "#dog1#dog2" produces the hashtag "#dog1#dog2"
##
##  (c) Hashtags do not care about case, so "#DOG" is the same as "#dog"
##       which is the same as "#Dog".
##
##  (d) The symbol "#" by itself is not a hashtag
##
##  The same rules apply to Twitter handles (user names) that begin with the
##   "@" symbol.         

## 9.  How many of the tweets have at least two Twitter handles?

# Start by converting tweets to lower case, padding each end with a space,
# and removing any punctuation except "@".
tweets = (" " + air['text'].str.lower() + " ").str.replace(r'[^\w\s@]+', ' ', regex=True)

ct1 = tweets.str.count(' @') # series of counts of ' @' in each tweet
ct2 = tweets.str.count(' @ ') # series of counts of ' @ ' in each tweet
atcts = ct1 - ct2 # series of counts of "legal" handles in each tweet
np.sum(atcts > 1) # count the number of tweets with more than one handle

q9 = np.sum(atcts > 1)

"""
## 9.

1482  # number of tweets with at least two Twitter handles

visible (1 pt): check that count is between 1400 and 1600
hidden (2 pts): check for match
"""


## 10. Suppose that a score of 3 is assigned to each positive tweet, 1 to
##      each neutral tweet, and -2 to each negative tweet.  Determine the
##      mean score for each airline and give the results as a Series with
##      airline name as the index, sorted by mean score from highest to lowest.

air['score'] = 1  # add a column to hold the score; preset to all 1's
# Mask using air['airline_sentiment'] == 'positive', set those scores = 3
air.loc[air['airline_sentiment'] == 'positive','score'] = 3
# Mask using air['airline_sentiment'] == 'negative', set those scores = -2
air.loc[air['airline_sentiment'] == 'negative','score'] = -2

# Below we group by the 'airline' column, keeping the 'score' column
group13 = air['score'].groupby(air['airline'])
group13.mean().sort_values(ascending=False)  # mean for each airline, sorted

q10 = group13.mean().sort_values(ascending=False)  

"""
## 10

airline
Virgin America    0.525794  # mean score for each airline
JetBlue           0.200270
Southwest         0.000826
United           -0.809262
American         -0.887640
US Airways       -1.145898

visible (1 pt): check type
hidden (2 pts): check for match
"""


## 11. What is the total number of hashtags in tweets associated with each
##      airline?  Give a Series with the airline name as index and the
##      corresponding totals for each, sorted from most to least.

# Start by converting tweets to lower case, padding each end with a space,
# and removing any punctuation except "#".
tweets = (" " + air['text'].str.lower() + " ").str.replace(r'[^\w\s#]+', ' ', regex=True)

ct1 = tweets.str.count(' #') # series of counts of ' #' in each tweet
ct2 = tweets.str.count(' # ') # series of counts of ' # ' in each tweet
hashtagcts = ct1 - ct2 # series of counts of "legal" hashtags in each tweet
air['hashtag_count'] = hashtagcts # add column of hashtag counts to 'air'

# Below we group by the 'airline' column, keeping the 'hashtag_count' column
group11 = air['hashtag_count'].groupby(air['airline'])
group11.sum().sort_values(ascending=False)  # count for each airline, sorted

q11 = group11.sum().sort_values(ascending=False)

"""
## 11.

airline
United            804    # Total number of hashtags, by airline
Southwest         718
US Airways        651
JetBlue           618
American          492
Virgin America    175

visible (1 pt): check type
hidden (3 pts): check for match
"""


## 12. Among the tweets that "@" a user besides the indicated airline, 
##      find the percentage include an "@" directed at the other airlines 
##      in this file. 

# Start by converting tweets to lower case, padding each end with a space,
# and removing any punctuation except "@".
tweets = (" " + air['text'].str.lower() + " ").str.replace(r'[^\w\s@]+', ' ', regex=True)

ct1 = tweets.str.count(' @') # series of counts of ' @' in each tweet
ct2 = tweets.str.count(' @ ') # series of counts of ' @ ' in each tweet
atcts = ct1 - ct2 # series of counts of "legal" handles in each tweet
multats = np.sum(atcts > 1) # count the number of tweets with more than
                            # one "legal" handle.

airhandles = pd.Series(['@virginamerica','@united','@southwestair','@jetblue', 
                        '@usairways','@americanair']) # list of airline handles
    
cts = np.zeros(len(air))  # Series of counts for each tweet
for airhandle in airhandles:  # Loop through each airline
    # t0 is 0/1 depending on if airhand is in the tweet; 1* converts T/F to 1/0
    t0 = 1*tweets.str.contains(" " + airhandle + " ")
    cts = cts + t0  # Add to each tweet counter (vectorized)
# cts has the number of airline users in each tweet; if > 1 then more than one
# airline is included in the tweet
np.sum(cts > 1)  # This produces 349 tweets with at least two airlines
100*np.sum(cts > 1)/multats  # compute percentage

q12 = 100*np.sum(cts > 1)/multats

"""
## 12.

23.549257759784076  # Percentage of tweets with more than one airline among
                    # those with more than one "@"
                    
hidden (4 pts): check for match                    
"""


## 13. Suppose the same user has two or more tweets in a row, based on how they 
##      appear in the file. For such tweet sequences, determine the percentage
##      for which the most recent tweet (which comes nearest the top of the
##      file) is a positive tweet.

twseqct = 0  # counter for consecutive tweet seqs
posct = 0  # count for positive first tweets in sequence
if air.loc[0,'name'] == air.loc[1,'name']:  # Check the first two entries
    twseqct += 1  # increment counter of tweet sequences
    if air.loc[0,'airline_sentiment'] == 'positive':
        posct += 1  # increment counter of positive tweets

# The loop below check entries indexed by 1, 2, 3, ...
for i in range(1,len(air)-1):
    if (air.loc[i,'name'] == air.loc[i+1,'name']) & (air.loc[i-1,'name'] != air.loc[i,'name']):
        twseqct += 1  # increment counter of tweet sequences
        if air.loc[i,'airline_sentiment'] == 'positive':
            posct += 1  # increment counter of positive tweets
print(100*posct/twseqct)  # print percentage of positive first tweets

q13 = 100*posct/twseqct

"""
## 13.

11.189634864546525  # Percentage positive tweets among consec tweets, same user

hidden (4 pts): check for match   
"""
