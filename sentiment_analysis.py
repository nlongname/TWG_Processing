# loosely adapted from a combination of https://towardsdatascience.com/nlp-part-3-exploratory-data-analysis-of-text-data-1caa8ab3f79d
# and https://towardsdatascience.com/preprocessing-text-data-using-python-576206753c28

import csv
from nicknames import *

name_list = [x.lower() for x in name_list]

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords, wordnet
from nltk import classify
from nltk import NaiveBayesClassifier

import random

import pandas as pd
import numpy as np
import string
import contractions

from functools import reduce

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
            is_wolf[(name_lookup[name_find(row[1].lower()).lower()], row[0])] = row[5]
            is_human[(name_lookup[name_find(row[1].lower()).lower()], row[0])] = row[4]
            
def wolf(name, game): #just for flexibility
    name = str(name)
    game = str(game)
    name = name.lower()
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
        return False #not in the game, or a GM post

def human(name, game): #note that this is not just the opposite of wolf(name, game), because there are 3rd parties and team-switchers who are considered neither
    game = str(game)
    name = str(name)
    name = name.lower()
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

def standardize_name(word):
    if word.lower() in name_list: #don't want to use name_find here, because it will have all kinds of false positives, I'd rather miss some less standard nicknames
        return(names[name_lookup[word.lower()]][0])
    else:
        return word
        

with open('post_archive.csv') as file:
    df = pd.read_csv(file, delimiter=',', quotechar="\'")
file.close()

#columns: ['post_id', 'post_text', 'profile_id', 'game', 'page']
df.drop('page', axis=1, inplace=True)

df['wolf'] = df.apply(lambda row: int(wolf(row['profile_id'], row['game'])), axis=1)
df['human'] = df.apply(lambda row: int(human(row['profile_id'], row['game'])), axis=1)
#df['usable'] = df.apply(lambda row: (int(row['human']) or int(row['wolf'])), axis=1)

df = df[(df['human']==1) | (df['wolf']==1)] #eliminate GM posts, outside players, 3rd parties
df.drop('human', axis=1, inplace=True)

def fix_names(pair):
    name, tag = pair
    if name in name_list:
        tag = 'NNP' #code for a proper noun, in case I ever use these directly
    return((name, tag))

def replace_names(pair):
    name, tag = pair
    if name in name_list:
        name = 'ForumName'
        tag = 'NNP'
    return((name, tag))

def convert_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def token_dicts(tokens_list):
    for tokens in tokens_list:
        yield dict([token, True] for token in tokens)

def process_posts(post_iter): #should work on any iterator, confirmed to work on df columns, lists, filters, and maps
    ws = pd.DataFrame({'post_text':post_iter})
    ws['no_contractions'] = ws['post_text'].apply(lambda x: [contractions.fix(word) for word in str(x).split()])
    ws['new_post'] = [' '.join(map(str, l)) for l in ws['no_contractions']]
    ws['tokenized'] = ws['new_post'].apply(word_tokenize)
    ws['standardized_names'] = ws['tokenized'].apply(lambda x: [standardize_name(word) for word in x])
    ws['lower'] = ws['standardized_names'].apply(lambda x: [word.lower() for word in x])
    ws['no_punctuation'] = ws['lower'].apply(lambda x: [word for word in x if word not in string.punctuation])
    stop_words = set(stopwords.words('english'))
    ws['no_stopwords'] = ws['no_punctuation'].apply(lambda x: [word for word in x if word not in stop_words])
    ws['pos_tags'] = ws['no_stopwords'].apply(nltk.tag.pos_tag) #'pos' stands for 'part of speech'
    # ^this^ wasn't catching proper nouns on forum names, which I can fix
    # this isn't perfect, because the tagger isn't taking into account that these are nouns as it goes through the sentence, but it's the best I can do without rewriting the tagger
    #ws['fixed_names'] = ws['pos_tags'].apply(lambda x: [fix_names(pair) for pair in x])
    ws['fixed_names'] = ws['pos_tags'].apply(lambda x: [replace_names(pair) for pair in x])
    ws['wordnet_pos'] = ws['fixed_names'].apply(lambda x: [(word, convert_pos(pos_tag)) for (word, pos_tag) in x])
    ws['lemmatized'] = ws['wordnet_pos'].apply(lambda x: [WordNetLemmatizer().lemmatize(word, tag) for word, tag in x])
    return ws['lemmatized']

df['lemmatized'] = process_posts(df['post_text'])

wolf_tokens = token_dicts(df[(df['wolf']==1)]['lemmatized'])
human_tokens = token_dicts(df[(df['wolf']==0)]['lemmatized'])

wolf_dataset = [(token_dict, "wolf") for token_dict in wolf_tokens]
human_dataset = [(token_dict, "human") for token_dict in human_tokens]

dataset = wolf_dataset + human_dataset
random.shuffle(dataset)

cutoff = int(len(dataset)*.8)
train_data = dataset[:cutoff]
test_data = dataset[cutoff:]

shortclassifier = NaiveBayesClassifier.train(train_data)

print("Accuracy is:", classify.accuracy(shortclassifier, test_data))
print(shortclassifier.show_most_informative_features(20))

# Notes:
# Accuracy ~64-68% depending on the train/test split
# random guessing according to the probability of wolves gives 61.25% accuracy
# naively guessing all-human gives 75% accuracy

# there are also several oddities cropping up in the top 20 features:
# names, random words that only came up in one game, etc.
# So maybe cleaning up some noise would help

# I suspect some of this is that even wolves have some human-seeming posts
# I want to explore two strategies: what % of a user's posts in a game seem wolfy?


# Compiling all posts into one (by user and game), classifying based on that:
"""
grouped = df.groupby(['profile_id', 'game'])

l = [g[1] for g in grouped]
#combine posts into one per person per game, keep the wolf column, drop everything else
#join would have been more elegant, but it messed up my escape characters

l = [[reduce(lambda x, y: str(x) + '. ' + str(y), x['post_text']), int(x['wolf'].mean())] for x in l]
megaposts = pd.DataFrame(l, columns=['megaposts', 'wolf'])

megaposts['lemmatized'] = process_posts(megaposts['megaposts'])

wolf_mega_tokens = token_dicts(megaposts[(megaposts['wolf']==1)]['lemmatized'])
human_mega_tokens = token_dicts(megaposts[(megaposts['wolf']==0)]['lemmatized'])

wolf_megaset = [(token_dict, "wolf") for token_dict in wolf_mega_tokens]
human_megaset = [(token_dict, "human") for token_dict in human_mega_tokens]

megaset = wolf_megaset + human_megaset
random.shuffle(megaset)

megacutoff = int(len(megaset)*.8)
train_mega = megaset[:megacutoff]
test_mega = megaset[megacutoff:]

megaclassifier = NaiveBayesClassifier.train(train_mega)

print("Accuracy is:", classify.accuracy(megaclassifier, test_mega))
print(megaclassifier.show_most_informative_features(20))
"""
# This is way worse, ~25-35% accurate
# I think the classifier only uses presence rather than frequency
# So the bigger chunks don't work as well because they lose more frequency info
