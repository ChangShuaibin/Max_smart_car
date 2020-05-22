#!/usr/bin/env python3
import threading
import queue
import time
import numpy as np
from Object_detection import Object_detect
import requests
from picamera import PiCamera
from motor import motor
from US_and_Mount import SteppingMount
from Direction_Gen import next_direction
from subprocess import call
camera = PiCamera()
app1 = Object_detect()
m = motor()
mount=SteppingMount([7,11,13,15])
mount.setup()
motor_queue = queue.Queue()
camera_queue = queue.Queue()
direction=0
forward=1
start=0
rotation=1
command = ''

def retrive_command():
    global command
    old_index = ''
    while 'exit' not in command:
        r = requests.get('http://192.168.99.177/') #iphone or mac IP address
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
            #print(command)
            old_index = index
        time.sleep(0.5)


def parse_command():
    global command
    if 'motor' in command:
        motor_queue.put(command)
    elif 'camera' in command:
        camera_queue.put(command)
    elif 'exit' in command:
        print('Good bye!')
        motor_queue.put('exit')
        camera_queue.put('exit')
        


def my_motor():
    global forward
    global start
    item = ''
    while 'exit' not in item:
        item = motor_queue.get()
        if 'left' in item:
            print('Max is turning left')
            m.angle2speed(90, forward)
            #direction=direction+90
        elif 'right' in item:
            print('Max is turning right')
            m.angle2speed(-90, forward)
            #direction=direction-90
        elif 'forward' in item:
            print('Max is moving forward')
            m.forward(forward)
        elif 'backward' in item:
            print('Max is moving backward')
            forward=forward*-1
            m.backward(forward)
            #direction=direction+180
        elif 'resume direction' in item:
            m.resume_direction()   #FIXME
        elif 'stop' in item or 'Stop' in item: # capital key word for ios speech recognition
            m.stop()
            start=0
        elif 'start' in item or 'Start' in item:
            start=1
            m.start(forward)
            


def my_camera():
    item = ''
    i=0
    while 'exit' not in item:
        item = camera_queue.get()
        if 'you see' in item:
            i=i+1
            target=item[19:len(item)]
            print('taking pictures and recognizing...')
            figure_name='image'+str(i)+'.jpg'
            camera.capture('/home/pi/Documents/Projects/Max_smart_car-master/photos/'+figure_name)
            app1.obj_detect('/home/pi/Documents/Projects/Max_smart_car-master/photos/'+figure_name)
        elif 'picture' in item:
            i=i+1
            figure_name='image'+str(i)+'.jpg'
            print('taking a picture')
            camera.capture('/home/pi/Documents/Projects/Max_smart_car-master/photos/' + figure_name)
        elif 'video' in item:
            print('taking 20 frames')
            k=i
            while i<k+20:
                i=i+1
                figure_name = 'image' + str(i) + '.jpg'
                camera.capture('/home/pi/Documents/Projects/Max_smart_car-master/photos/' + figure_name)
                #time.sleep(0.5)
            print('finished taking 20 frames')
    camera.close()



def my_radar():
    global command
    global direction
    global start
    global rotation
    global forward
    while 'exit' not in command:
        radar=np.zeros([16,2])
        for i in range(16):
            if rotation==1:
                mount.ClockWiseCycle()
            else:
                mount.CClockWiseCycle()
            distance=mount.US.getSonar()
            
            if distance>0:
                radar[i][1]=distance
                print(i*22.5*rotation, distance)
            else:
                radar[i][1]=220
                print(i*22.5*rotation, 220)
            tmp=i*22.5*rotation
            if tmp<0:
                tmp=tmp+360
            radar[i][0]=tmp
        direction=next_direction(direction,radar)
        print('new direction: ',direction)
        if start==1:
            m.angle2speed(direction, forward)
        rotation=rotation*-1
    print('exit radar')
    #mount.motorStop()


if __name__ == "__main__":
    from urllib.request import urlopen
    loop=1
    call(['espeak "hi hi   wait for wifi connection" 2>/dev/null'],shell=True)
    while loop:
        try:
            urlopen("http://192.168.99.177")
            loop=0
        except:
            time.sleep(1)
    call(['espeak "hi hi   initiating max" 2>/dev/null'],shell=True)
    motor_thread = threading.Thread(target=my_motor, name='motor')
    camera_thread = threading.Thread(target=my_camera, name='camera')
    radar_thread = threading.Thread(target=my_radar, name='radar')

    motor_thread.start()
    camera_thread.start()
    radar_thread.start()
    retrive_command()

    motor_thread.join()
    camera_thread.join()
    call(['espeak "hi hi   shutting down!" 2>/dev/null'],shell=True)
    time.sleep(6)
    m.destroy()
    call(['espeak "hi hi   Good bye!" 2>/dev/null'],shell=True)