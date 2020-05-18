import requests
import time
import logging
import pyttsx3
engine = pyttsx3.init() # object creation

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
#print (rate)                        #printing current voice rate
engine.setProperty('rate', 200)     # setting up new voice rate


"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
#print (volume)                          #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
#engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female

#for key in logging.Logger.manager.loggerDict:
#    logging.getLogger(key).setLevel(logging.CRITICAL)
logging.getLogger().setLevel(logging.DEBUG)

def retrive_command():
    text=''
    old_index=''
    while 'exit' not in text:
        r = requests.get('http://0.0.0.0:81')
        text = r.text.split('<h1>')
        text = text[1]
        text = text.split('</h1>')
        index=text[1]
        text = text[0]
        index=index.split('<h2>')
        index=index[1]
        index=index.split('</h2>')
        index=index[0]
        if old_index!=index:
            engine.say(index, text)
            old_index=index
        time.sleep(2)

if __name__=="__main__":
    retrive_command()