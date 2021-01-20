import sys
import io
from nltk.tag import pos_tag
import weather_forecast as wf
import json

def get_narrative(whatWasPrinted):
    
    d = whatWasPrinted.strip()
    d = d.split(',')
    # print(d)
    for i in d:
        if "\'narrative\'" in i:
            i = i.split(":")
            a = i[1].strip()
            if a != "None":
                return a

def get_weather(sentence):
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    sentence = sentence.title()
    tagged_sent = pos_tag(sentence.split())
    pn = [word for word,pos in tagged_sent if pos == 'NNP']
    if "Weather" in pn:
        pn.remove("Weather")
    final = "".join(pn)
    wf.forecast(place = final)
    sys.stdout = old_stdout
    text = buffer.getvalue()
    return get_narrative(text)

# print(get_weather('what is the weather of kasganj'))