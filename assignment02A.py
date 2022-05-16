##
## File: assignment02-solutions.py (STAT 3250)
## Topic: Assignment 2 Solutions
##

## Two *very* important rules that must be followed in order for your 
## assignment to be graded correctly:
##
## a) The file name must be exactly "assignment02.py" (without the quotes)
## b) The variable names followed by "= None" must not be changed and these 
##    names variable names should not be used anywhere else in your file.  Do   
##    not delete these variables, if you don't know how to find a value just  
##    leave it as is. (If a variable is missing the autograder will not grade  
##    any of your assignment.)


## Questions 1-7: For the questions in this part, use the following
##  lists as needed:
    
list01 = [5, -9, -1, 8, 0, -1, -2, -7, -1, 0, -1, 6, 7, -2, -1, -5]
list02 = [-2, -5, -2, 8, 7, -7, -11, 1, -1, 6, 6, -7, -9, 1, 5, -11]
list03 = [9, 0, -8, 3, 2, 9, 3, -4, 5, -9, -7, -3, -11, -6, -5, 1]
list04 = [-4, -6, 8, 8, -5, -5, -11, -3, -1, 7, 0, 2, -5, -2, 0, -5]
list05 = [-11, -3, 8, -9, 2, -8, -7, -12, 7, 3, 2, 0, 6, 4, -11, 6]
biglist = list01 + list02 + list03 + list04 + list05

import numpy as np # load "numpy"

## Questions 1-7: Use for loops to answer each of the following applied to the 
##  lists defined above.
 
## 1.  Add up the squares of the entries of biglist.

s = 0  # Set the sum to 0
for m in biglist:
    s = s + m**2   # add m^2 to the sum
print(s)  # print out the sum of squares

q1 = s

"""
## 1.

2895  # The sum of the squares of entries in biglist
"""


## 2.  Create "newlist01", which has 14 entries, each the sum of the 
##      corresponding entry from list01 added to the corresponding entry
##      from list02.  That is,
##     
##         newlist01[i] = list01[i] + list02[i] 
##
##      for each 0 <= i <= 13.

newlist01 = 14*[0]  # Initialize the list newlist01 to 19 0's
for i in range(14):
    newlist01[i] = list01[i] + list02[i]  # Add terms together
print(newlist01)

q2 = newlist01

"""
## 2.

[3, -14, -3, 16, 7, -8, -13, -6, -2, 6, 5, -1, -2, -1]  #newlist01
"""


## 3.  Determine the number of entries in biglist that are less than 6.

ct = 0  # initialize counter to 0
for m in biglist:
    if m < 6:    # check if list element is less than 6
        ct = ct + 1  # increment the counter
print(ct)  # print count of entries < 6

q3 = ct

"""
## 3.

64  # count of biglist entries that are < 6
"""

## 4.  Create a new list called "newlist02" that contains the elements of
##      biglist that are greater than 5, given in the same order as the
##      elements appear in biglist.

newlist02 = []  # initialize list with no entries
for m in biglist:
    if m > 5:
        newlist02.append(m)  # append entry to end of newlist02
print(newlist02)

q4 = newlist02

""" 
## 4.

[8, 6, 7, 8, 7, 6, 6, 9, 9, 8, 8, 7, 8, 7, 6, 6] 
"""

## 5.  Find the sum of the positive entries of biglist.

s = 0  # initialize counter to 0
for m in biglist:
    if m >0:    # check if list element is positive
        s = s + m  # add to the sum
print(s)  # print sum of positive entries

q5 = s

"""
## 5.

155
"""

##  6. Make a list of the first 19 negative entries of biglist, given in
##      the order that the values appear in biglist.

negvalues = [] # list to contain negative values
valct = 0 # counter for the number of negative values
i = 0 # index for biglist

while valct < 19:   # while loop to aqccumulate negative values
    if biglist[i] < 0:  
        negvalues.append(biglist[i])
        valct = valct + 1
    i = i + 1
print(negvalues)

q6 = negvalues

"""
## 6.

[-9, -1, -1, -2, -7, -1, -1, -2, -1, -5, -2, -5, -2, -7, -11, -1, -7, -9, -11]
"""
        

##  7. Identify all elements of biglist that have a smaller element that 
##      immediately preceeds it.  Make a list of these elements given in
##      the same order that the elements appear in biglist.

bigvalues = []  # a list to hold the required elements
for i in range(len(biglist)-1):
    if biglist[i] < biglist[i+1]:
        bigvalues.append(biglist[i+1])
print(bigvalues)

q7 = bigvalues

"""
## 7.

[-1, 8, -1, 0, 6, 7, -1, -2, -2, 8, 1, 6, 1, 5, 9, 3, 9, 5, -7, -3, -6, -5, 
 1, 8, -3, -1, 7, 2, -2, 0, -3, 8, 2, -7, 7, 6, 6]
"""


## Questions 8-9: These questions use simulation to estimate probabilities
##  and expected values.  

##  8. Consider the following game: You flip a fair coin.  If it comes up
##      tails, then you win $1.  If it comes up heads, then you get to 
##      simultaneously flip four more fair coins.  In this case you win $1 
##      for each head that appears on all flips, plus you get an extra $7 if 
##      all five flips are heads.
##
##      Use 100,000 simulations to estimate the average amount of money won 
##      when playing this game.

allwinnings = np.zeros(100000)
for i in range(100000):
    flip1 = np.random.choice([1,0], size=1)
    if flip1 == 1:
        flip2 = np.random.choice([1,0], size=4)
        sum = 1 + flip2[0] + flip2[1] + flip2[2] + flip2[3]
    else:
        sum = 1
    if sum == 5:
        sum = 12
    allwinnings[i] = sum
    
q8 = np.mean(allwinnings)  # mean of 100,000 times playing the game

"""
## 8.

Amount varies, acceptable range is [2.19, 2.25]
"""


##  9. Jay is taking a 15 question true/false quiz online.  The
##      quiz is configured to tell him whether he gets a question
##      correct before proceeding to the next question.  The 
##      responses influence Jay's confidence level and hence his 
##      exam performance.  In this problem we will use simulation
##      to estimate Jay's average score based on a simple model.
##      We make the following assumptions:
##    
##      * At the start of the quiz there is a 81% chance that 
##        Jay will answer the first question correctly.
##      * For all questions after the first one, if Jay got 
##        the previous question correct, then there is a
##        90% chance that he will get the next question
##        correct.  (And a 10% chance he gets it wrong.)
##      * For all questions after the first one, if Jay got
##        the previous question wrong, then there is a
##        72% chance that he will get the next question
##        correct.  (And a 28% chance he gets it wrong.)
##      * Each correct answer is worth 5 points, incorrect = 0.
##
##      Use 100,000 simulated quizzes to estimate Jay's average 
##      score.

allscores = np.zeros(100000) # array to hold quiz scores
for i in range(100000):
    scoretotal = 0  # initialize quire score to 0
    q1score = np.random.choice([5,0], size=1, p=[.81,.19]) # random score, Q1
    scoretotal += q1score[0] # add quest 1 to score
    lastscore = q1score # keep track of score on previous problem
    for j in range(14): # the rest of the quiz; 1 loop per question
        if lastscore > 0: # check last result; generate next result
            nextscore = np.random.choice([5,0], size=1, p=[.90,.10])
        else:
            nextscore = np.random.choice([5,0], size=1, p=[.72,.28])
        scoretotal += nextscore[0] # add question score to scoretotal
        lastscore = nextscore # shift question score to last question
    allscores[i] = scoretotal # save the score total

q9 = np.mean(allscores)  # mean of 100,000 simulated quizzes

"""
## 9.

Amount varies, acceptable range is [65.36, 65.52]
"""


