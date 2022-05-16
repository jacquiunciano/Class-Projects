##
## File: assignment12-solutions.py (STAT 3250)
## Topic: Assignment 12 Solutions
##

##  This year's NCAA basketball tournaments were cancelled. As a small 
##  consolation for this assignment we revisit past men's tournaments 
##  (including the glorious 2019 edition) using data from the file 
##
##      'ncaa.csv':  NCAA Men's Tournament Scores, 1985-2019
##
##  The organization of the file is fairly clear.  Each record has information
##  about one game, including the year, the teams, the final score, and each 
##  team's tournament seed.  

##  Two important points:
##    1) Each team is assigned a "seed" at the start of the tournament.  The
##       teams thought to be better are assigned smaller number seeds.  (So 
##       the best teams are assigned 1 and the worst assigned 16.)  In this 
##       assignment a "lower seed" refers to a worse team and hence larger 
##       seed number, with the opposite meaning for "higher seed". 
##    2) All questions refer only to the data in this in 'ncaa.csv' so you
##       don't need to worry about tournaments prior to 1985.

##  Note: The data set is from Data.World, with the addition of the 2019
##  tournament provided by your dedicated instructor. (There was no 2020
##  tournament and the 2021 tournament didn't turn out to your instructor's
##  liking so that data is omitted.)

##  Submission Instructions: Submit your code in Gradescope under 
##  'Assignment 12 Code'.  The autograder will evaluate your answers to
##  Questions 1-8.  You will also generate a separate PDF for the graphs
##  in Questions 9-11, to be submitted in Gradescope under 'Assignment 12 Graphs'.

import pandas as pd
import numpy as np

ncaa = pd.read_csv("ncaa.csv")

## 1.  Find all schools that have won the championship. Report your results in
##     a Series that has the schools as index and number of championships for
##     values, sorted alphabetically by school.

finals = ncaa.loc[ncaa['Region Name'] == 'Championship',:] # extract records with championship game
# Next extract the champion from each record in 'finals'
champseries = pd.concat([finals.loc[finals['Score'] > finals['Score.1'],'Team'], finals.loc[finals['Score'] < finals['Score.1'],'Team.1']])
q1 = champseries.value_counts().sort_index()  # Series of champions and counts

"""
## 1.

Arizona           1
Arkansas          1
Connecticut       4
Duke              5
Florida           2
Indiana           1
Kansas            2
Kentucky          3
Louisville        2
Maryland          1
Michigan          1
Michigan St       1
North Carolina    4
Syracuse          1
UCLA              1
UNLV              1
Villanova         3
Virginia          1
"""


## 2.  Determine all schools that have been in the tournament at least 25 times.
##     Report your results as a Series with schools as index and number of times
##     in the tournament as values, sorted alphabetically by school.

teams = ncaa.loc[ncaa['Round'] == 1,['Team','Team.1']] # All teams for each year
teams = pd.concat([teams['Team'],teams['Team.1']]) # Combine into a single column
q2 = teams.value_counts()[teams.value_counts()>=25].sort_index() #count values, extract >= 25, then sort

"""
## 2.

Arizona           32
Duke              34
Indiana           25
Kansas            34
Kentucky          30
Louisville        26
Michigan St       29
North Carolina    32
Oklahoma          26
Purdue            26
Syracuse          28
Texas             26
UCLA              25
Xavier            25
"""


## 3.  Find all years when the school that won the tournament was seeded 
##     3 or lower. (Remember that "lower" seed means a bigger number!) Give  
##     a DataFrame with years as index and corresponding school and seed
##     as columns (from left to right).  Sort by year from least to most recent.

finals = ncaa.loc[ncaa['Region Name'] == 'Championship',:] # extract championship games
champs1 = finals.loc[finals['Score'] > finals['Score.1'],['Year','Team','Seed']] # extract some of the champs; the rest on next line of code
champs2 = finals.loc[finals['Score'] < finals['Score.1'],['Year','Team.1','Seed.1']].rename(columns={"Team.1": "Team", "Seed.1": "Seed"})
champs = pd.concat([champs1,champs2]) # combine year, school, and seed into a single DataFrame
champs3 = champs[champs['Seed'] >= 3].sort_values(by='Year')   # extract seeds <= 3; sort on year
champs3.index = champs3['Year']  # change index to 'Year'
q3 = champs3[['Team','Seed']]  # extract final DataFrame columns

"""
## 3.

              Team  Seed
Year                   
1985    Villanova     8
1988       Kansas     6
1989     Michigan     3
1997      Arizona     4
2003     Syracuse     3
2006      Florida     3
2011  Connecticut     3
2014  Connecticut     7
"""



## 4.  Determine the average tournament seed for each school.  Make a Series
##     of all schools that have an average seed of 5.0 or higher (that is,
##     the average seed number is <= 5.0).  The Series should have schools
##     as index and average seeds as values, sorted alphabetically by
##     school

seedsteamsA = ncaa.loc[ncaa['Round'] == 1,['Team','Seed']]
seedsteamsB = ncaa.loc[ncaa['Round'] == 1,['Team.1','Seed.1']]
seedsteamsB.columns = ['Team','Seed']
seedsteams = pd.concat([seedsteamsA,seedsteamsB])
group4 = seedsteams['Seed'].groupby(seedsteams['Team'])
group4 = group4.mean()
q4 = group4[group4 <= 5]


"""
## 4.

Team
Arizona            4.437500
Connecticut        3.950000
Drake              5.000000
Duke               2.176471
Florida            4.954545
Georgetown         4.666667
Kansas             2.500000
Kentucky           3.566667
Louisville         5.000000
Loyola Illinois    4.000000
Maryland           4.952381
Massachusetts      4.375000
Michigan           4.809524
Michigan St        4.827586
Miss. St           5.000000
North Carolina     2.718750
Ohio St            4.450000
Syracuse           4.428571
TCU                5.000000
Virginia           4.722222
Wake Forest        4.642857
Washington St      5.000000
"""


## 5.  For each tournament round, determine the percentage of wins by the
##     higher seeded team. (Ignore games of teams with the same seed.)
##     Give a Series with round number as index and percentage of wins
##     by higher seed as values sorted by round in order 1, 2, ..., 6. 
##     (Remember, a higher seed means a lower seed number.)

# Extract games between different seeds
ncaa5 = ncaa[ncaa['Seed'] != ncaa['Seed.1']].copy()
# Add a column 'HSW' to indicate if the higher seed won; used in other questions
ncaa5['HSW'] = 0  # "Higher Seed Won"
ncaa5.loc[((ncaa5['Seed']<ncaa5['Seed.1']) & (ncaa5['Score']>ncaa5['Score.1'])) | ((ncaa5['Seed']>ncaa5['Seed.1']) & (ncaa5['Score']<ncaa5['Score.1'])),'HSW'] = 1
group05 = ncaa5['HSW'].groupby(ncaa5['Round'])
q5 = 100*group05.mean()  # Series of round number and percentage higher seed wins

"""
## 5.

Round
1    74.285714 # percentage of wins by team seeded higher (lower seed number)
2    71.250000 # in the tournament, by round.
3    71.428571
4    55.000000
5    65.384615
6    74.074074
"""


## 6.  For each seed 1, 2, 3, ..., 16, determine the average number of games
##     won per tournament by a team with that seed.  Give a Series with seed 
##     number as index and average number of wins as values, sorted by seed 
##     number 1, 2, 3, ..., 16. (Hint: There are 35 tournaments in the data set
##     and each tournamentstarts with 4 teams of each seed.  We are not 
##     including "play-in" games which are not part of the data set.)

seedwon1 = ncaa.loc[ncaa['Score']>ncaa['Score.1'],'Seed']
seedwon2 = ncaa.loc[ncaa['Score']<ncaa['Score.1'],'Seed.1']
seedwon = pd.concat([seedwon1, seedwon2])
q6 = seedwon.value_counts().sort_index()/(35*4) # Series of seed and average number of wins

"""
## 6.

1     3.350000  # Average number of wins by seed
2     2.371429
3     1.864286
4     1.535714
5     1.114286
6     1.071429
7     0.907143
8     0.700000
9     0.600000
10    0.621429
11    0.614286
12    0.514286
13    0.250000
14    0.164286
15    0.064286
16    0.007143
"""


## 7.  For each year's champion, determine their average margin of victory 
##     across all of their games in that year's tournament. Find the champions
##     that have an average margin of victory of at least 15. Give a DataFrame 
##     with year as index and champion and average margin of victory as columns
##     (from left to right), sorted by from highest to lowest average victory 
##     margin.


ChampsYears = pd.DataFrame()
ChampsYears['Year'] = pd.Series(range(1985,2020))
finals = ncaa.loc[ncaa['Region Name'] == 'Championship',['Team','Team.1','Score','Score.1']]
ChampsYears['Champion'] = pd.concat([finals.loc[finals['Score'] > finals['Score.1'],'Team'], finals.loc[finals['Score'] < finals['Score.1'],'Team.1']]).sort_index().values

ncaa['Margin'] = np.abs(ncaa['Score'] - ncaa['Score.1'])  # Add margin of victory to df.
ChampsYears['Average Margin'] = 0
for year in ChampsYears['Year']:
    champ = ChampsYears.loc[ChampsYears['Year']==year,'Champion'].values[0]
    margins = ncaa.loc[(ncaa['Year']==year) & ((ncaa['Team']==champ) | (ncaa['Team.1']==champ)),'Margin']
    ChampsYears.loc[ChampsYears['Year']==year,'Average Margin'] = margins.mean()
    
ChampsYears1 = ChampsYears[ChampsYears['Average Margin'] >= 15].sort_values(by='Average Margin', ascending=False)
ChampsYears1.index = ChampsYears1['Year']
q7 = ChampsYears1[['Champion','Average Margin']]

"""
## 7.

            Champion  Average Margin
Year                                
1996        Kentucky       21.500000
2016       Villanova       20.666667
2009  North Carolina       20.166667
1990            UNLV       18.666667
2018       Villanova       17.666667
2001            Duke       16.666667
2013      Louisville       16.166667
2006         Florida       16.000000
1993  North Carolina       15.666667
2015            Duke       15.500000
2000     Michigan St       15.333333
"""
    

## 8.  Determine the 2019 champion.  Use code to extract the correct school,
##     not your knowledge of college backetball history.

q8 = ChampsYears.loc[ChampsYears['Year']==2019,'Champion'].values[0]

"""
## 8.

Virginia
"""


##  Questions 9-11: These require the creation of several graphs. In addition to 
##  the code in your Python file, you will also upload a PDF document (not Word!)
##  containing your graphs (be sure they are labeled clearly).  Include the
##  required code in this file and put your graphs in a PDF document for separate
##  submission.  All graphs should have an appropriate title and labels for
##  the axes.  For these questions the only output required are the graphs.
##  When your PDF is ready submit it under 'Assignment 12 Graphs' in Gradescope.

## 9.  For each year of the tournament, determine the average margin of
##     victory for each round.  Then make a histogram of these averages,
##     using 16 bins and a range of [0,32].

import matplotlib.pyplot as plt

group10 = ncaa['Margin'].groupby([ncaa['Year'],ncaa['Round']])
avemargins = group10.mean()

plt.hist(avemargins, bins=16, range=[0,32], color='red', edgecolor='black')   
plt.title('Average Margin of Victory (by Round and Year)')
plt.ylabel("Counts")
plt.xlabel("Average Margin of Victory (pts)")
plt.show()


## 10. Produce side-by-side box-and-whisker plots, one using the Round 1
##     margin of victory for games where the higher seed wins, and one
##     using the Round 1 margin of victory for games where the lower
##     seed wins.  (Remember that higher seed = lower seed number.)
##     Orient the boxes vertically with the higher seed win data on the 
##     left.

round1 = ncaa[ncaa['Round']==1]
marginhigh = round1.loc[round1['Score']>round1['Score.1'],'Margin']
marginlow = round1.loc[round1['Score']<round1['Score.1'],'Margin']

plt.boxplot([marginhigh,marginlow], notch=None) 
plt.xticks([1, 2], ['Higher Seed', 'Lower Seed']) # Specifies data group
plt.xlabel("Winning Team")
plt.ylabel("Margin of Victory (pts)")
plt.title("Margin of Victory by Relative Seed")
plt.show()


## 11. Produce a bar chart for the number of Round 2 victories by seed.
##     The bars should proceed left to right by seed number 1, 2, 3, ...

ncaa2 = ncaa[ncaa['Round'] == 2]
seedwon1 = ncaa2.loc[ncaa['Score']>ncaa['Score.1'],'Seed']
seedwon2 = ncaa2.loc[ncaa['Score']<ncaa['Score.1'],'Seed.1']
seedwon = pd.concat([seedwon1, seedwon2])
counts = seedwon.value_counts().sort_index()
plt.bar(counts.index, counts, color='green', edgecolor='black')
plt.xlabel("Seed")
plt.ylabel("Number of Victories")
plt.title("Number of Round 2 victories by Seed")
plt.show()




