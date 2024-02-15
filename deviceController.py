from yeelight import *
from ppadb.client import Client as AdbClient
import speech_recognition as sr

import pandas as pd
import time
from utils import load_json_file
import threading
import json

recognizer = sr.Recognizer()
controllerJson = load_json_file("config/adbConfig.json")

class control:
    def __init__(self):
        self.command_bulbdevices = discover_bulbs()
        self.devices=  pd.DataFrame(self.command_bulbdevices)
        self.client = AdbClient(host=controllerJson["host"], port=controllerJson["port"])
        self.text = ""


    def mic(self):
        with sr.Microphone() as source:
            print("Say something in Thai:")
            audio = recognizer.listen(source,phrase_time_limit=5)
        try:
            self.text = recognizer.recognize_google(audio, language="th-TH")
            return True
        except:
            return False


    def command_bulb(self,bulb, control):
        bulb.turn_on()
        if "set_brightness" in control:
            if control["set_brightness"] <1:
                bulb.turn_off()
            else:
                bulb.turn_on()

        if "set_rgb" in control:
            if "r" in control["set_rgb"]:
                bulb.set_rgb(control["set_rgb"]["r"], control["set_rgb"]["g"], control["set_rgb"]["b"])
            else:
                bulb.turn_off()

    def iot(self,json_obj):
        threads = []
        if json_obj[0] == "{":
            json_obj = json.loads(json_obj)
            
            if "tv" in json_obj:
                if "query" in json_obj["tv"]:

                    control = json_obj["tv"]
                    print("TV Controling: "+ str(control))

                    thread = threading.Thread(target=self.play_youtube_video_on_chromecast, args=(control["query"],control["mode"]))
                    threads.append(thread)
                    thread.start()

            if "light" in json_obj:
                control = json_obj["light"]
                if control != {}:
                    print("IoT Controling: "+ str(control))
                    for i in self.devices["ip"]:
                        bulb = Bulb(i)
                        thread = threading.Thread(target=self.command_bulb, args=(bulb,control))
                        threads.append(thread)
                        thread.start()
        
            for thread in threads:
                thread.join()


    def play_youtube_video_on_chromecast(self,query, mode):
        query = query.replace(" ","_")
        
        # Connect to your Mi Box
        device = self.client.device(controllerJson["mibox_ip"])
        device.shell("input keyevent HOME")

        if query == "HOME" or mode == "HOME":
            return 

        if device is not None:

            if mode == "youtube":
                if query == "":
                    device.shell("am start -a android.intent.action.VIEW -d https://www.youtube.com/")
                    return
                
                device.shell("am start -a android.intent.action.VIEW -d  https://www.youtube.com/results?search_query="+query)
                time.sleep(0.2)
                device.shell("input keyevent KEYCODE_DPAD_RIGHT")
                time.sleep(0.2)
                device.shell("input keyevent KEYCODE_ENTER")

            if mode == "netflix":
                device.shell("am start -a android.intent.action.VIEW -d  https://www.netflix.com/")#search?q="+query)
                time.sleep(0.2)
                device.shell("input keyevent KEYCODE_DPAD_RIGHT")
                time.sleep(0.2)
                device.shell("input keyevent KEYCODE_ENTER")
            
            if mode == "spotify":
                if query == "MYPLAYLIST" or query == "":
                    device.shell("am start -a android.intent.action.VIEW -d https://open.spotify.com/collection/tracks")
                    time.sleep(0.2)
                    device.shell("input keyevent KEYCODE_DPAD_RIGHT")
                    time.sleep(0.2)
                    device.shell("input keyevent KEYCODE_DPAD_RIGHT")
                    time.sleep(0.2)
                    device.shell("input keyevent KEYCODE_ENTER")
                    time.sleep(0.2)
                    device.shell("input keyevent KEYCODE_DPAD_DOWN")
                    time.sleep(0.2)
                    device.shell("input keyevent KEYCODE_DOWN")
                    time.sleep(0.2)
                    device.shell("input keyevent KEYCODE_ENTER")
                    return
                
                device.shell("am start -a android.intent.action.VIEW -d  https://open.spotify.com/search/"+query)
                time.sleep(0.2)
                device.shell("input keyevent KEYCODE_DPAD_RIGHT")
                time.sleep(0.2)
                device.shell("input keyevent KEYCODE_ENTER")

        else:
            print("Couldn't connect to the Mi Box. Make sure the IP is correct and ADB over network is enabled.")
