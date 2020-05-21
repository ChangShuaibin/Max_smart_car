import speech_recognition as sr
import threading
from flask import Flask, render_template
import logging

#for key in logging.Logger.manager.loggerDict:
#    logging.getLogger(key).setLevel(logging.CRITICAL)
#logging.getLogger().setLevel(logging.DEBUG)
app = Flask(__name__)
command=''
index=0
r = sr.Recognizer()
sr.Microphone.list_microphone_names()
r.energy_threshold = 400
r.dynamic_energy_threshold = 1
r.dynamic_energy_ratio = 1.8
motor_key_words=['turn left', 'turn right', 'forward','backward','stop']
camera_key_words=['can you see', 'take a picture','take a video']

def listen():
    global command
    global index
    while not 'exit' in command:
        with sr.Microphone(0) as source:
            print("listening period start")
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
                #print('listening period stop')
                try:
                    key_word = r.recognize_google(audio)
                    if 'hey Max' in key_word:
                        print("Yes Sir!")
                        text=Give_command(command)
                        command=stadardize_command(text)
                        index=index+1
                except:
                    print('can not recognize command')
            except sr.WaitTimeoutError:
                print('time out')

def Give_command(command):
        with sr.Microphone() as source:
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
                #print('start processing command')
                command = r.recognize_google(audio)
            except sr.UnknownValueError:
                pass
                # print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return (command)

def stadardize_command(text):
    for item in motor_key_words:
        if item in text:
            return 'motor '+item
    for item in camera_key_words:
        if item in text:
            return 'camera '+ text
    if 'exit' in text:
        return 'exit'
    return ''

@app.route("/")
def hello():
   global command
   global index
   templateData = {
       'index': index,
       'command': command
   }
   return render_template('template.html', **templateData)

if __name__=="__main__":
    thread_listen=threading.Thread(target=listen, name='listen')
    thread_listen.start()
    app.run(debug=True, port=80, host='0.0.0.0', use_reloader=False)
    thread_listen.join()
