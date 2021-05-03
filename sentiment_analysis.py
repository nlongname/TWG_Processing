import csv
from nicknames import *
is_wolf = {} #(game#, profile_id)
is_human = {} #(game#, profile_id)

with open('Players by role and death.csv', newline='') as csvfile:
    inforeader = csv.reader(csvfile, delimiter=',',quotechar="\"")
    for row in inforeader:
        if row[2] != '':
            if name_find(row[1])[-1] == '?':
                print(row[0], row[1])
            is_wolf[(row[0], name_lookup[name_find(row[1])])] = row[5]
            is_human[(row[0], name_lookup[name_find(row[1])])] = row[4]
#with open('post_archive.csv', newline='') as csvfile
            
