import csv
from nicknames import *

import sys
sys.path.append('/home/xazarus/.local/lib/python3.5/site-packages')

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer

from pandas import Dataframe

is_wolf = {} #(profile_id, game#)
is_human = {} #(profile_id, game#)
wolfposts = []
humanposts=[]
otherposts=[]
gms = [0]*50

with open('Players by role and death.csv', newline='') as csvfile:
    inforeader = csv.reader(csvfile, delimiter=',',quotechar="\"")
    for row in inforeader:
        if row[2] != '':
            if name_find(row[1])[-1] == '?':
                print(row[0], row[1])
            is_wolf[(name_lookup[name_find(row[1])], row[0])] = row[5]
            is_human[(name_lookup[name_find(row[1])], row[0])] = row[4]
            
def wolf(name, game): #just for flexibility
    game = str(game)
    if name in names.keys():
        profile = name
    elif name in name_lookup.keys():
        profile = name_lookup[name]
    else:
        profile = name_lookup[name_find(name)]
    try:
        result = bool(int(is_wolf[(profile, game)]))
        return result
    except KeyError:
        if gms[int(game)] == 0: #since the posts are in order, this should be the initial post by the GM
            gms[int(game)] = profile
            return False

def human(name, game): #note that this is not just the opposite of wolf(name, game), because there are 3rd parties and team-switchers who are considered neither
    game = str(game)
    if name in names.keys():
        profile = name
    elif name in name_lookup.keys():
        profile = name_lookup[name]
    else:
        profile = name_lookup[name_find(name)]
    try:
        result = bool(int(is_human[(profile, game)]))
        return result
    except KeyError: #people who aren't in the game aren't wolves or human (might be GM, but that's set by Wolf)
        return False

firstline = True
with open('post_archive.csv', newline='') as csvfile:
    postreader = csv.reader(csvfile, delimiter=',', quotechar="\'")
    for row in postreader:
        if firstline:
            firstline = False
        else:
            if wolf(row[2], row[3]):
                wolfposts.append(row[1])
            elif human(row[2], row[3]):
                humanposts.append(row[1])
            else:
                otherposts.append(row[1])

#switching gears on this part, since the previous lemmatization method couldn't easily deal with contractions
#leaving it in in case I can use some of it later

#wolf_tokens = map(word_tokenize, wolfposts)
#human_tokens = map(word_tokenize, humanposts)
#
#def lemmatize(token_list):
#    lemmatizer = WordNetLemmatizer()
#    lemmatized = []
#    for word, tag in pos_tag(token_list):
#        if tag[:2] == 'NN':
#            pos = 'n' #pos 'part of speech', comes from the NLTK function
#        elif tag[:2] == 'VB':
#            pos = 'v'
#        else:
#            pos = 'a'
#        lemmatized.append(lemmatizer.lemmatize(word, pos))
#    return lemmatized


#wolf_tokens = map(lemmatize, wolf_tokens)
#human_tokens = map(lemmatize, human_tokens)

#wf = Dataframe(wolfposts, columns = ['raw_post'])
#hf = Dataframe(humanposts, columns = ['raw_post'])

