import speech
import time
import sound
import threading
from flask import Flask, render_template
import logging
import console
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
console.set_idle_timer_disabled(1)
app = Flask(__name__)
command=''
index=0
motor_key_words=['Turn left', 'Turn right', 'forward','backward','Stop', 'Start']
camera_key_words=['Can you see', 'picture','video']

def listen():
    global command
    global index
    recorder = sound.Recorder('speech.m4a')
    while 'exit' not in command:
      speech.say('listening')
      print('listening')
      recorder.record()
      time.sleep(3)
      recorder.stop()
      try:
          text = speech.recognize('speech.m4a')
          [command, index]= stadardize_command(text[0][0], index)
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
    if 'Exit' in text:
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
    #listen()
