##
## File: assignment10-solutions.py (STAT 3250)
## Topic: Assignment 10 Solutions
##

##  For this assignment you will be working with Twitter data related
##  to the season opening of Game of Thrones on April 14, 2019.  You will use 
##  a set of over 10,000 tweets for this purpose.  The data is in the file 
##  'GoTtweets.txt'.  

##  Note: On this assignment it makes sense to use loops to extract 
##  information from the tweets. Go wild.

##  The Gradescope autograder will be evaluating your code on a reduced 
##  version of the GoTtweets.txt data that includes only a fraction of the
##  records.  Your code needs to automatically handle all assignments
##  to the variables q1, q2, ... to accommodate the reduced data set,
##  so do not copy/paste things from the console window, and take care
##  with hard-coding values.  

import json
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', 10) # Display 10 columns in console

# Read in the tweets and append them to 'tweetlist'
tweetlist = []
for line in open('GoTtweets.txt', 'r'): # Open the file of tweets
    tweetlist.append(json.loads(line))  # Add to 'tweetlist' after converting

tweetser = pd.Series(tweetlist) # Convert to a series

## 1.  The tweets were downloaded in several groups at about the same time.
##     Are there any that appear in the file more than once?  Give a Series 
##     with the tweet ID for any repeated tweets as the index and the number 
##     of times each ID appears in the file as values.  Sort by the index from
##     smallest to largest.

## Note: For the remaining questions in this assignment, do not worry about 
##       any duplicate tweets.  Just answer the questions based on the 
##       existing data set.
    
tweet_id_ser = pd.Series(len(tweetser)*[0]) # series to hold tweet IDs
for i in range(len(tweetser)):
    tweet_id_ser[i] = tweetser[i]['id']  # put ID in series
tweet_id_cts = tweet_id_ser.value_counts() # counts of the tweet IDs

q1 = tweet_id_cts[tweet_id_cts > 1] # Series of tweet IDs that appear > 1 time

"""
## 1.

1117608741099069440    2 # Repeated tweet ID's and number of times repeated
1117619562588057600    2

"""


## 2.  Determine the number of tweets that include 'Daenerys' (any combination
##     of upper and lower case; part of another work OK) in the text of the 
##     tweet.  Then do the same for 'Snow'.

ct1 = 0  # counter for tweets with text including 'daenerys'
for tweet in tweetser:
    if tweet['text'].lower().count('daenerys') > 0: # check for 'daenerys'
        ct1 += 1
q2a = ct1 # number of tweets including 'daenerys'

ct2 = 0  # counter for tweets with text including 'snow'
for tweet in tweetser:
    if tweet['text'].lower().count('snow') > 0: # check for 'snow'
        ct2 += 1
q2b = ct2 # number of tweets including 'snow'

"""
## 2.

352  # number of tweets with 'Daenerys' (and case variants) in text of tweet
206  # number of tweets with 'Snow' (and case variants) in text of tweet

"""


## 3.  Find the average number of hashtags included in the tweets. (You may get 
##     the wrong answer if you use the text of the tweets instead of the
##     hashtag lists.)

hashtag_count_list = [] # list to hold hashtag counts
for tweet in tweetlist:
    hashtag_list = tweet['entities']['hashtags'] # extract hashtag list
    hashtag_count_list.append(len(hashtag_list)) # add count to list
q3 = np.mean(hashtag_count_list) # average number of hashtags per tweet

"""
## 3.

1.011720930232558  # Mean number of hashtags per tweet

"""
 
## 4.  Determine the tweets that have 0 hashtags, 1 hashtag, 2 hashtags,
##     and so on.  Give your answer as a Series with the number of hashtags
##     as index (sorted smallest to largest) and the corresponding number of
##     tweets as values. Include in your Series index only number of hashtags  
##     that occur for at least one tweet. (Note: See warning in #3)

# This uses 'hashtag_count_list' defined in #3.
q4 = pd.Series(hashtag_count_list).value_counts().sort_index() # Series of number of hashtags and counts

"""
## 4.
  
0      780 # There are 780 tweets with 0 hashtags, 4025 with 1 hashtag, ...
1     4025
2      385
3      136
4       25
5       16
6        5
7        1
8        1
10       1

"""


## 5.  Determine the number of tweets that include the hashtag '#GoT', then
##     repeat for '#GameofThrones'.  (You may get the wrong answer if you
##     use the text of the tweets instead of the hashtag lists.)
##     Note: Hashtags are not case sensitive, so any of '#GOT', '#got', 'GOt' 
##     etc are all considered matches.

# We dig the hashtag list out of each tweet.
ct5a = 0 # initialize the counter
for tweet in tweetlist:
    hashtag_list = tweet['entities']['hashtags'] # extract hashtag list
    if len(hashtag_list) > 0: # check if any hashtags; if so:
        present = 0 # flag to indicate if 'got' found
        for i in range(len(hashtag_list)):
            if (hashtag_list[i]['text']).lower() == 'got': # check for 'got'
                present = 1
        ct5a += present  # increment counter when 'got' found
q5a = ct5a  # number of tweets with '#GoT' hashtag and upper/lower variants               

# Repeat above for 'gameofthrones'
ct5b = 0 # initialize the counter
for tweet in tweetlist:
    hashtag_list = tweet['entities']['hashtags'] # extract hashtag list
    if len(hashtag_list) > 0: # check if any hashtags; if so:
        present = 0 # flag to indicate if 'gameofthrones' found
        for i in range(len(hashtag_list)):
            if (hashtag_list[i]['text']).lower() == 'gameofthrones': # check for 'gameofthrones'
                present = 1
        ct5b += present  # increment counter when 'gameofthrones' found
q5b = ct5b  # number of '#GoT' hashtags and upper/lower variants             

"""
## 5.

548  # Number of tweets with '#GoT' (and case variants)
4147  # Number of tweets with '#GameofThrones' (and case variants)

"""        


## 6.  Some tweeters like to tweet a lot.  Find the screen name for all 
##     tweeters with at least 3 tweets in this data.  Give a Series with 
##     the screen name (in lower case) as index and the number of tweets as 
##     value, sorting by the index in alphbetical order.  

tweet_screenname_ser = pd.Series(len(tweetser)*[""]) # series for screen names
for i in range(len(tweetser)):
    tweet_screenname_ser[i] = tweetser[i]['user']['screen_name'].lower()
tweeter_cts = tweet_screenname_ser.value_counts() 
q6 = tweeter_cts[tweeter_cts >= 3].sort_index() # Series of screen name and counts

"""
## 6.

adrianaf1700      3 # screen names with 3 or more tweets
caioomartinez     3
chronicwheelz     3
czo18             4
dasia90sss        3
eleo_ellis        3
eliase_21         3
gameofvikings_    3
gamoraavengxr     3
richadafangirl    3
tytydelicate      3
valdoalmeida      3

"""

    
## 7.  Among the screen names with 3 or more tweets, find the average
##     'followers_count' for each and then give a table with the screen  
##     and average number of followers.  (Note that the number of
##     followers might change from tweet to tweet.)  Give a Series with
##     screen name (in lower case) as index and the average number of followers  
##     as value, sorting by the index in alphbetical order.  

screenname_cts = tweet_screenname_ser.value_counts() # count screen names
screennames3 = screenname_cts[screenname_cts >= 3].index # 3 or more tweets
followers = pd.Series(index = screennames3) # series with screen names = index
for screenname in screennames3:
    followers_cts = []  # list to hold follower counts
    for i in range(len(tweetser)): # find tweets with screen name
        if tweetser[i]['user']['screen_name'].lower() == screenname:
            followers_cts.append(tweetser[i]['user']['followers_count'])
    followers[screenname] = np.mean(followers_cts) # mean of follow counts
q7 = followers.sort_index() # Series of screen names and mean follower counts  

"""
## 7.

adrianaf1700       260.0  # screen name and average follower counts
caioomartinez      245.0
chronicwheelz      193.0
czo18             1811.0
dasia90sss         280.0
eleo_ellis        2948.0
eliase_21           15.0
gameofvikings_    1493.0
gamoraavengxr     3842.0
richadafangirl     892.0
tytydelicate       130.0
valdoalmeida      3939.0

"""

                                                                
## 8.  Determine the hashtags that appeared in at least 50 tweets.  Give
##     a Series with the hashtags (lower case) as index and the corresponding 
##     number of tweets as values, sorted alphabetically by hashtag.

all_hashtags = [] # initialize the master hashtag list
for tweet in tweetser:
    hashtags = tweet['entities']['hashtags'] # extract hashtag list for tweet
    if len(hashtags) > 0: # check if any hashtags; if so:
        new_hashtags = [] # create list of new hashtags
        for i in range(len(hashtags)):  # loop puts hashtags in list
            new_hashtags.append((hashtags[i]['text']).lower()) # add to list
        all_hashtags = all_hashtags + new_hashtags # add to master list

# Next define a series to hold counts for the number of tweets containing each hashtag.
hashtag_cts = pd.Series(0, index=np.unique(all_hashtags)) # initialize to 0

for tweet in tweetlist:
    hashtags = tweet['entities']['hashtags'] # extract hashtag list
    if len(hashtags) > 0: # check if any hashtags; if so:
        hashtag_list = [] # initialize list to hold hashtags
        for i in range(len(hashtags)):
            hashtag_list.append((hashtags[i]['text']).lower()) # append hashtag to list
        hashtag_cts[np.unique(hashtag_list)] += 1 # increment hashtag counters

# Finally print out the require table of hashtags and counts
q8 = hashtag_cts[hashtag_cts>= 50].sort_index() # Series of hashtags and counts

"""
## 8.

forthethrone             111  # This gives the number of tweets each hashtag
gameofthrones           4147  # appears in.  
gameofthronesseason8      75
got                      548
gots8                     50

"""       
        

##  9.  Some of the tweets include the location of the tweeter.  Give a Series
##      of the names of countries with at least three tweets, with country 
##      name as index and corresponding tweet count as values.  Sort the
##      Series alphabetically by country name.

##      sorted by tweet 
##      count with largest at the top.

country_list = [] # list to hold country names
for tweet in tweetlist:
    if tweet['place'] != None:
        country = tweet['place']['country'] # extract country
        country_list.append(country) # add country to list of countries
        
country_cts = pd.Series(country_list).value_counts() # tally up the country counts
q9 = country_cts[country_cts >= 3].sort_index()   # print those countries with at least three tweets

"""
## 9.

Brasil            16
Colombia           4
India              5
México             4
United Kingdom     3
United States     26

"""


## Questions 10-11: The remaining questions should be done using regular 
##                  expressions as described in the class lectures.

## 10.  Determine the percentage of tweets (if any) with a sequence of 3 or more
##      consecutive digits.  (No spaces between the digits!)  For such tweets,
##      apply 'split()' to create a list of substrings.  Among all the 
##      substrings with a sequence of at least three consecutive digits,
##      determine the percentage where the substring starts with a '@' at the 
##      beginning of the substring.

ct = 0  # counter for tweets with a sequence of three digits
substring_list = []
for tweet in tweetlist:
    # create a True/False vector indicating three digits for each tweet
    tfvec = list(pd.Series(tweet['text'].split()).str.contains("\d\d\d",regex = True))
    if np.sum(tfvec) > 0:  # check if at least one substring has three digits
        # add all substrings with three digits to master list
        substring_list = substring_list + list(pd.Series(tweet['text'].split())[tfvec])
        ct += 1  # increment tweet counter
q10a = 100*ct/len(tweetser)  # percentage of tweets with three consecutive digits

# Count the number of substrings starting with '@' then compute percentage
q10b = 100*np.sum(pd.Series(substring_list).str.startswith('@'))/len(substring_list)

"""
## 10.

5.786046511627907   # percentage of tweets with three consecutive digits
55.214723926380366  # percentage of substrings starting with '@'

"""


## 11.  Determine if there are any cases of a tweet with a 'hashtag' that is
##      actually not a hashtag because there is a character (letter or digit)
##      immediately before the "#".  An example would be 'nota#hashtag'.
##      Count the number of tweets with such an incorrect 'hashtag'.

import re # import regular expression library

ct11 = 0  # counter for tweets with bad hashtag
for tweet in tweetser:
    if re.search("[a-z0-9]#[a-z0-9]", tweet['text'].lower()): # look for # between characters 
        ct11 += 1  # increment counter
q11 = ct11 # print count of tweets with bad hashtag

"""
## 11.

0  # number of tweets with a bad hashtag

## The one tweet with bad hashtag below:
Arya and Jon’s reunion is the best 😭🖤❄️🐺 #winterishere#gameofthrones
"""







