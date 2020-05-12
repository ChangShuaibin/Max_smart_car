#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
import threading
import queue
import time
from Object_detection import Object_detect

queue1 = queue.Queue()
queue2 = queue.Queue()
queue3 = queue.Queue()
queue4 = queue.Queue()
queue0 = queue.Queue()

r = sr.Recognizer()
sr.Microphone.list_microphone_names()
r.energy_threshold = 400
r.dynamic_energy_threshold = 1
r.dynamic_energy_ratio = 1.8
def listen():
        command=''
        while not 'exit' in command:
            with sr.Microphone() as source:
                print('Max is listening')
                try:
                    audio = r.listen(source, timeout=5)
                    try:
                        key_word = r.recognize_google(audio)
                        if 'Max' in key_word :
                            print('Yes sir')
                            command=Give_command(command)
                    except:
                        pass
                except sr.WaitTimeoutError:
                    pass

def Give_command(command):
        with sr.Microphone() as source:
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                audio = r.listen(source)
                command = r.recognize_google(audio)
                queue0.put(command)
            except sr.UnknownValueError:
                pass
                # print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return(command)


def dequeue():
        item=''
        while 'exit' not in item:
            item=queue0.get()
            if 'turn left' in item:
                queue1.put('turn left')
            elif 'turn right' in item:
                queue2.put('turn right')
            elif 'can you see' in item:
                queue3.put('can you see')
            elif 'exit' in item:
                print('Good bye!')
                queue1.put('exit')
                queue2.put('exit')
                queue3.put('exit')
                queue4.put('exit')
            else:
                queue4.put(item)

def turn_left():
        item=''
        while 'exit' not in item:
            item=queue1.get()
            if item == 'turn left':
                print(threading.current_thread(),'Max is turning left')

def turn_right():
        item=''
        while 'exit' not in item:
            item=queue2.get()
            if item == 'turn right':
                print(threading.current_thread(),'Max is turning right')

def can_you_see():
        item=''
        while 'exit' not in item:
            item=queue3.get()
            if item == 'can you see':
                print(threading.current_thread())
                app1=Object_detect()
                app1.obj_detect('fruit.jpg')


def other():
        item=''
        while 'exit' not in item:
            item=queue4.get()
            if 'exit' not in item:
                print(threading.current_thread(),item)


if __name__=="__main__":

    left_thread = threading.Thread(target=turn_left,name='turn left')
    right_thread = threading.Thread(target=turn_right, name='turn right')
    see_thread = threading.Thread(target=can_you_see, name='see')
    other_thread = threading.Thread(target=other, name='other')
    thread_dequeue=threading.Thread(target=dequeue, name='dequeue')
    left_thread.start()
    right_thread.start()
    see_thread.start()
    other_thread.start()
    thread_dequeue.start()
    listen()
    left_thread.join()
    right_thread.join()
    see_thread.join()
    other_thread.join()
    thread_dequeue.join()

