import speech_recognition as sr
import threading
from flask import Flask, render_template
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
command=''
index=0
r = sr.Recognizer()
sr.Microphone.list_microphone_names()
r.energy_threshold = 400
r.dynamic_energy_threshold = 1
r.dynamic_energy_ratio = 2
motor_key_words=['turn left', 'turn right', 'forward','backward','stop', 'start']
camera_key_words=['can you see', 'picture','video']

def listen():
    global command
    global index
    while not 'exit' in command:
         with sr.Microphone() as source:
                try:
                    audio = r.listen(source, timeout=10, phrase_time_limit=4)
                    text = r.recognize_google(audio)
                    [command, index]= stadardize_command(text, index)
                    print(command)
                except:
                    pass

def stadardize_command(text, index):
    for item in motor_key_words:
        if item in text:
            return ['motor '+item, index+1]
    for item in camera_key_words:
        if item in text:
            return ['camera '+ text,index+1]
    if 'exit' in text:
        return ['exit', index+1]
    return ['missed that', index]

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
