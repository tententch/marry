import speech_recognition as sr
import threading
import time
import json
from ui import FaceGame
import pygame
import time
from utils import load_json_file
from assistances import *
from deviceController import *

recognizer = sr.Recognizer()
media_json = load_json_file("config/mediaPath.json")
assistance = ai()
controller = control()

def speaker(filepath):
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

# Function to continuously listen and process user input
def run():
    game = FaceGame()
    game.screen.fill(game.BACKGROUND_COLOR)
    pygame.display.flip()

    active = False
    answer = False
    following_active = False
    
    for event in pygame.event.get():

        with sr.Microphone() as source:
            print("Say something in Thai:")
            audio = recognizer.listen(source,phrase_time_limit=5)
        try:
            text = recognizer.recognize_google(audio, language="th-TH")
        except:
            text = ""
            following_active = False
            active = False

        if "Ferdinand" in text or "เฟอดินานด์" in text or "เฟอดินาน" in text or "ferdinand" in text or "เฟอร์ดินาน" in text:
            ass_name = "ferdinand"
            active = True
            following_active = False
            assistance.change_ai(ass_name)
            
        if "Mary" in text or "แมรี่" in text or "marry" in text :
            ass_name = "mary"
            active = True
            assistance.change_ai(ass_name)
        
                
        if active:
            print(f"You said: {text}")
            speaker(media_json["signal"])

            if not following_active:
                following_active = True
                pass
            else:
                if ass_name == "mary":
                    game.screen.fill(game.BACKGROUND_COLOR)

                    if 'thread_id' in locals():
                        answer, thread_id = assistance.gpt(text, thread_id)
                    else:
                        answer, thread_id = assistance.gpt(text)
      

                    assistance.answer(answer)

                    threads = []
                    thread = threading.Thread(target=speaker,args=(media_json["answer"],))
                    threads.append(thread)
                    thread.start()

                    game.set_subtitle(answer)
                    game.render_subtitle(0.05)
                    # Update the display
                    pygame.display.flip()
                    # Cap the frame rate at 60 frames per second
                    game.clock.tick(10)
                    for thread in threads:
                        thread.join()

                else:
                    game.screen.fill((0, 0, 0))

                    if 'thread_id' in locals():
                        json_obj, thread_id = assistance.gpt(text, thread_id)
                    else:
                        json_obj, thread_id = assistance.gpt(text)


                    threads = []
                    if json_obj[0] == "{":
                        json_obj = json.loads(json_obj)
                        
                        if "tv" in json_obj:
                            if "query" in json_obj["tv"]:

                                control = json_obj["tv"]
                                print("TV Controling: "+ str(control))

                                thread = threading.Thread(target=controller.play_youtube_video_on_chromecast, args=(control["query"],control["mode"]))
                                threads.append(thread)
                                thread.start()

                        if "light" in json_obj:
                            control = json_obj["light"]
                            if control != {}:
                                print("IoT Controling: "+ str(control))
                                for i in controller.devices["ip"]:
                                    bulb = Bulb(i)
                                    thread = threading.Thread(target=controller.command_bulb, args=(bulb,control))
                                    threads.append(thread)
                                    thread.start()
                    
                    for thread in threads:
                        thread.join()

run()

