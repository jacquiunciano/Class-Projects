# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 15:18:22 2022

@author: Jacqueline Unciano
"""

##  For each question use the following lists as needed:
list01 = [2,5,4,9,10,-3,5,5,3,-8,0,2,3,8,5,2,-3,8,7]
list02 = [-7,-3,8,-5,-5,2,4,9,10,-7,9,10,2,13,-12,-4,1,3,5]
list03 = [2,-5,6,0,7,-2,-3,5,0,2,8,7,9,2,0,-2,5,5,6]
list04 = [3,5,-10,2,0,4,-5,-7,6,2,3,3,5,12,-5,-9,-7,4]
biglist = list01 + list02 + list03 + list04

## 1.  Find the product of the last five elements of list04.

q1 = list04[-1] * list04[-2] * list04[-3] * list04[-4]

## 2.  Extract the sublist of list01 that goes from
##      the 4th to the 10th elements (inclusive).

q2 = list01[3:10]

## 3.  Concatenate list01 and list04 (in that order), sort
##      the combined list, then extract the sublist that 
##      goes from the 6th to the 17th elements (inclusive).

list0104 = list01 + list04
list0104.sort()
q3 = list0104[5:17]

## 4.  Generate "biglist", then extract the sublist of every 5th 
##      element starting with the 4th list element

q4 = biglist[3::5]

## 5.  Determine the number of times that 3 appears in biglist.

count = 0  ## counting method
for num in biglist: ## for every number in list
    if num == 3:  ## check for 3
        count += 1  ## add to count if the number is 3
q5 = count

## 6.  Determine the index for the first appearance of 12 in biglist.

index_counting = 0  ## counting method
for num in biglist:
    if num != 12:  ## check for 12
        index_counting += 1  ## add to count if the number isn't 12
    if num == 12:
        break
q6 = index_counting