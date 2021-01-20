import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import pyjokes
from keras.models import load_model
import json
import random
import tensorflow as tf   
import pandas as pd
tf.get_logger().setLevel('ERROR')
from nltk.tag import pos_tag
import convert
import wikipedia
import weather

def fetch_wikipedia(sentence):
    sentence = sentence.title()
    tagged_sent = pos_tag(sentence.split())
    pn = [word for word,pos in tagged_sent if pos == 'NNP']
    final = "".join(pn)
    return wikipedia.summary(final)

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model , words , classes):
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.1
    results = [[i,r] for i,r in enumerate(res) if r>=ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(intent , qtype):
    lisp = []
    if qtype == 'type1':
        data_file = open('database/intents1.json').read()
        lisp = json.loads(data_file)["type1"]
    elif qtype == 'type2':
        data_file = open('database/intents2.json').read()
        lisp = json.loads(data_file)["type2"]
    elif qtype == 'type3':
        data_file = open('database/intents3.json').read()
        lisp = json.loads(data_file)["type3"]
        
    for i in lisp:
        if(i['tag']== intent):
            result = random.choice(i['responses'])
            break
    return result

def call_model(sentence , qtype):
    no = qtype
    model = load_model('models/model' + no + '.h5')
    words = pickle.load(open('type' + no + '/words.pkl','rb'))
    classes = pickle.load(open('type' + no + '/classes.pkl','rb'))
    found_intent = predict_class(sentence , model , words , classes)[0]['intent']
    return found_intent

def main(question):
    model = load_model('models/model.h5')
    words = pickle.load(open('main_model/words.pkl','rb'))
    classes = pickle.load(open('main_model/classes.pkl','rb'))
    qtype = predict_class(question , model , words , classes)[0]['intent']
    if qtype == 'type1':
        it = call_model(question , '1')
    elif qtype == 'type2':
        it = call_model(question , '2')
    elif qtype == 'type3':
        it = call_model(question , '3')
    return (qtype, it)

def get_answer(question):
    if question == "/start":
        return """
Hello! Welcome to **Prometheus**. I'm a query bot and I can help you with your doubts regarding --
– college (IIT Mandi)
– programming

You can talk to me about **weather** (like you would with any fellow human) and ask for suggestions -- songs, movies, books. I also seem to have a decent **sense of humour** (or so what my fellow bots tell me) If you're into programming jokes, we'll get along pretty well ; ) 

I've been in your world for quite a while now; I've observed things and grasped some knowledge. So additionally, you can ask me **general questions** about your world and I hope to answer them correctly! 
__Try -- "tell me about elon musk”__


Please bear with me if I'm unable to answer a few questions or respond with unrelated answers. I'm still learning (and definitely hope to get better!) Have a good day : )
"""
    print(question)
    try:
        a = main(question)
        response = ""
        if a[1] == 'suggest_movie':
            response = 'Response : Here is a movie suggestion ' + str(convert.give_suggestion('movies'))
        elif a[1] == 'suggest_song':
            response = 'Response : Here is a song suggestion ' +  str(convert.give_suggestion('songs'))
        elif a[1] == 'suggest_book':
            response = 'Response : Here is a book suggestion ' + str(convert.give_suggestion('books'))
        elif a[1] == 'tell_joke':
            response = "Response : Here is a joke " + pyjokes.get_joke('en')
        elif a[1] == 'get_info':
            response = "Response : " + fetch_wikipedia(question)
        elif a[1] == 'get_weather':
            response = "Response : " + weather.get_weather(question)
        else:
            typeq = a[0]
            intentq = a[1]
            response = "Response : " + getResponse(intentq , typeq)
        return response
    except:
        return "Sorry. I ran into some error"

    
    