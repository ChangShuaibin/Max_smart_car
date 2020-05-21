#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import threading
import queue
import time
from Object_detection import Object_detect
import requests
from picamera import PiCamera
from motor import motor

camera=PiCamera()
m=motor()
motor_queue = queue.Queue()
camera_queue = queue.Queue()
radar_queue = queue.Queue()


def retrive_command():
    global command
    command=''
    old_index=''
    while 'exit' not in command:
        r=requests.get('http://192.168.99.164/')
        text = r.text.split('<h1>')
        text = text[1]
        text = text.split('</h1>')
        index=text[1]
        command = text[0]
        index=index.split('<h2>')
        index=index[1]
        index=index.split('</h2>')
        index=index[0]
        if old_index!=index:
            parse_command()
            old_index=index
        time.sleep(2)


def parse_command():
            if 'turn left' in command:
                queue1.put('turn left')
            elif 'turn right' in command:
                queue2.put('turn right')
            elif 'can you see' in command:
                queue3.put('can you see')
            elif 'exit' in command:
                print('Good bye!')
                queue1.put('exit')
                queue2.put('exit')
                queue3.put('exit')
                queue4.put('exit')
            else:
                queue4.put(command)

def turn_left():
        item=''
        while 'exit' not in item:
            item=queue1.get()
            if item == 'turn left':
                print('Max is turning left')
                m.angle2speed(90)

def turn_right():
        item=''
        while 'exit' not in item:
            item=queue2.get()
            if item == 'turn right':
                print('Max is turning right')
                m.angle2speed(-90)

def can_you_see():
        item=''
        while 'exit' not in item:
            item=queue3.get()
            if item == 'can you see':
                print('taking pictures and recognizing...')
                camera.capture('/home/pi/Desktop/image.jpg')
                app1=Object_detect()
                app1.obj_detect('/home/pi/Desktop/image.jpg')
                
def forward():
    pass


def other():
        item=''
        while 'exit' not in item:
            item=queue4.get()
            if 'exit' not in item:
                print(item)


if __name__=="__main__":
    #retrive_thread=threading.Thread(target=retrive_command, name='retrive')
    left_thread = threading.Thread(target=turn_left,name='turn left')
    right_thread = threading.Thread(target=turn_right, name='turn right')
    see_thread = threading.Thread(target=can_you_see, name='see')
    other_thread = threading.Thread(target=other, name='other')

    left_thread.start()
    right_thread.start()
    see_thread.start()
    other_thread.start()
    retrive_command()
    #retrive_thread.start()
    left_thread.join()
    right_thread.join()
    see_thread.join()
    other_thread.join()
    #retrive_thread.join()

