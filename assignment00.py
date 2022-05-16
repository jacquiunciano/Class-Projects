list01 = [2,5,4,9,10,-3,5,5,3,-8,0,2,3,8,5,2,-3,8,7]
list02 = [-7,-3,8,-5,-5,2,4,9,10,-7,9,10,2,13,-12,-4,1,3,5]
list03 = [2,-5,6,0,7,-2,-3,5,0,2,8,7,9,2,0,-2,5,5,6]
list04 = [3,5,-10,2,0,4,-5,-7,6,2,3,3,5,12,-5,-9,-7,4]
biglist = list01 + list02 + list03 + list04

index_count = 0
for num in biglist:
    if num != 12:
        index_count += 1
    if num == 12:
        break
q6 = index_count

print(len(biglist))