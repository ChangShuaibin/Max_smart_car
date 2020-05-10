#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr
from Object_detection import Object_detect
import threading
class Max():
    def __init__(self):
        super().__init__()
        # obtain audio from the microphone
        self.r = sr.Recognizer()
        sr.Microphone.list_microphone_names()
        self.r.energy_threshold = 400
        self.r.dynamic_energy_threshold = 1
        self.r.dynamic_energy_ratio = 1.8
        self.command=''

    def listen(self):
        with sr.Microphone() as source:
            print('Max is listening')
            try:
                audio1 = self.r.listen(source, timeout=5)
                try:
                    key_word1 = self.r.recognize_google(audio1)
                    if 'Max' in key_word1 :
                        print('Yes sir')
                        self.Give_command()
                except:
                    pass
            except sr.WaitTimeoutError:
                pass
        return(self.command)

    def Give_command(self):
        with sr.Microphone() as source:
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                    audio = self.r.listen(source)
                    self.command = self.r.recognize_google(audio)
                    if 'turn left' in self.command:
                        print('Roger that, Max is turing left')
                    elif 'turn right' in self.command:
                        print('Roger that, Max is turning right')
                    elif 'can you see' in self.command:
                        print('processing image...')
                        app=Object_detect()
                        app.obj_detect('fruit.jpg')
                        print('success ')
                    elif 'exit' in self.command:
                        print('Good bye!')
                    else:
                        print(self.command)

            except sr.UnknownValueError:
                pass
                # print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                #print("Could not request results from Google Speech Recognition service; {0}".format(e))
                pass



if __name__=="__main__":
    command = ''
    app=Max()
    while not 'exit' in command:
        command=app.listen()