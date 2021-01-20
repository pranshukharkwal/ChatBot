# %%
import pandas as pd
import json
import random
from nltk.tag import pos_tag
nltk.download('averaged_perceptron_tagger')
import wikipedia
# %%


'''

dictionary -> Arrays -> Data of a book

Types:
'''


def give_suggestion(t1, t2=''):
    '''
    @param
    t1 is from the array of ['songs','movies','books']
    # If t1 not found, it suggests some movie

    t2 is optional, and can only be from the above suggestion_type
    # If t2 is empty or wrong, randomly choses


    @ return: A dictionary with some data and 
    name: The name of the suggestions
    
    movies: [
        'rating',
        'storyline',
        'ratingCount',
        'length',
        'release',
        'thumbnail',
        'name'
    ]

    songs: [
        'artist',
        'year',
        'name'
    ]

    books: [
        'authors',
        'image',
        'download',
        'publisher',
        'year',
        'pages',
        'language',
        'name'
    ]

    '''

    suggestion_type = {
        'books': ['signal_processing',
                  'data_science',
                  'mathematics',
                  'economics',
                  'history',
                  'science',
                  'psychology',
                  'fiction',
                  'computer_science',
                  'nonfiction',
                  'philosophy'],

        'movies': ['Comedy',
                   'Action',
                   'Crime',
                   'Thriller',
                   'Horror',
                   'Mystery',
                   'Drama',
                   'Fantasy',
                   'War',
                   'Children',
                   'Documentary',
                   'Animation',
                   'Romance',
                   'Adventure',
                   'Sci-Fi',
                   'Musical'],

        'songs': ['neo mellow',
                  'hip hop',
                  'pop',
                  'big room',
                  'british soul',
                  'rap',
                  'permanent wave',
                  'boy band',
                  'EDM',
                  'complextro',
                  'australian dance',
                  'contemporary',
                  'latin']
    }

    file = ''
    try:
        file = open('suggestions/' + t1 + '.json').read()
    except FileNotFoundError:
        t1 = 'movies'
        file = open(('suggestions/movies.json')).read()

    dic = json.loads(file)
    keys = list(dic.keys())

    if t2 not in keys:
        # Find a valid t2
        t2 = suggestion_type[t1][0]

    # Now we are ready to find the suggestion
    list_of_songs = dic[t2]
    l = len(list_of_songs)

    r = random.randint(0, l-1)
    song = list_of_songs[r]

    # Now r key is the name
    name = list(song.keys())[0]
    songData = song[name]
    songData['name'] = name

    return songData

def fetch_wikipedia(sentence):
    tagged_sent = pos_tag(sentence.split())
    pn = [word for word,pos in tagged_sent if pos == 'NNP']
    final = " ".join(pn)
    return wikipedia.summary(final)

#%%
# some test cases!!
t1 = 'movies'
t2 = ''

give_suggestion(t1, t2)

#%%

t1 = 'songs'
t2 = 'rap'

give_suggestion(t1, t2)


#%%
t1 = 'books'
t2 = 'kuch bhi'

give_suggestion(t1, t2)
