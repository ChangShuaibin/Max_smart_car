#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import threading
import queue
import time
import numpy as np
from Object_detection import Object_detect
import requests
from picamera import PiCamera
from motor import motor
from US_and_mount import SteppingMount
from Direction_Gen import next_direction

camera = PiCamera()
app1 = Object_detect()
m = motor()
mount=SteppingMount([7,11,13,15])
mount.setup()
motor_queue = queue.Queue()
camera_queue = queue.Queue()
direction=0

def retrive_command():
    global command
    command = ''
    old_index = ''
    while 'exit' not in command:
        r = requests.get('http://192.168.99.164/')
        text = r.text.split('<h1>')
        text = text[1]
        text = text.split('</h1>')
        index = text[1]
        command = text[0]
        index = index.split('<h2>')
        index = index[1]
        index = index.split('</h2>')
        index = index[0]
        if old_index != index:
            parse_command()
            old_index = index
        time.sleep(2)


def parse_command():
    if 'motor' in command:
        motor_queue.put(command)
    elif 'camera' in command:
        camera_queue.put(command)
    elif 'exit' in command:
        #print('Good bye!')
        motor_queue.put('exit')
        camera_queue.put('exit')


def my_motor():
    item = ''
    while 'exit' not in item:
        item = motor_queue.get()
        if 'turn left' in item:
            print('Max is turning left')
            m.angle2speed(90)
            #direction=direction+90
        elif 'turn right' in item:
            print('Max is turning right')
            m.angle2speed(-90)
            #direction=direction-90
        elif 'forward' in item:
            m.forward()
        elif 'backward' in item:
            m.backward()
            #direction=direction+180
        elif 'resume direction' in item:
            m.resume_direction()   #FIXME
        elif 'stop' in item:
            m.stop()
        elif 'exit' in item:
            print('Good bye!')


def my_camera():
    item = ''
    i=0
    while 'exit' not in item:
        item = camera_queue.get()
        if 'can you see' in item:
            i=i+1
            target=item[19:len(item)]
            print('taking pictures and recognizing...')
            figure_name='image'+str(i)+'.jpg'
            camera.capture('/home/pi/Desktop/'+figure_name)
            app1.obj_detect('/home/pi/Desktop/'+figure_name)
        elif 'take a picture' in item:
            i=i+1
            print('taking a picture')
            camera.capture('/home/pi/Desktop/' + figure_name)
        elif 'video' in item:
            k=i
            while i<k+20:
                i=i+1
                figure_name = 'image' + str(i) + '.jpg'
                camera.capture('/home/pi/Desktop/' + figure_name)
                time.sleep(0.5)



def my_radar():
    item = ''
    while 'exit' not in command:
        radar=np.zeros([16,2])
        for i in range(16):
            mount.ClockWiseCycle()
            distance=mount.US.getSonar()
            if distance>0:
                radar[i][1]=distance
            else:
                radar[i][1]=220
            radar[i][0]=i*22.5
        direction=next_direction(direction,radar)
        print('new direction: ',direction)
        m.angle2speed(direction)


if __name__ == "__main__":
    motor_thread = threading.Thread(target=my_motor, name='motor')
    camera_thread = threading.Thread(target=my_camera, name='camera')
    radar_thread = threading.Thread(target=my_radar, name='radar')

    motor_thread.start()
    camera_thread.start()
    radar_thread.start()
    retrive_command()

    motor_thread.join()
    camera_thread.join()
