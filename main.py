from ui import FaceGame
import pygame
from utils import load_json_file, speaker
from assistances import *
from deviceController import *
import threading


mediaJson = load_json_file("config/mediaPath.json")
assistance = ai()
controller = control()

# Function to continuously listen and process user input
def run():
    game = FaceGame()
    game.screen.fill(game.BACKGROUND_COLOR)
    pygame.display.flip()

    for event in pygame.event.get():
        if not controller.mic():
            assistance.following_active = False
            assistance.active = False

        text = controller.text
        assistance.ai_call(text)


        if assistance.active:
            threads = []

            speaker(mediaJson["signal"])
            if not assistance.following_active:
                assistance.following_active = True
                assistance.new_thread()
                print(assistance.name+": Activated")
                continue
                
            else:
                print("user: "+text)
                game.screen.fill(game.BACKGROUND_COLOR)
                answer = assistance.gpt(text)

                
                if assistance.name == "ferdinand":
                    thread = threading.Thread(target=controller.iot, args=(answer,))
                    thread.start()
                    threads.append(thread)

                    thread = threading.Thread(target=speaker, args=(mediaJson["complete"],))
                    thread.start()    
                    threads.append(thread)
                    answer = "กำลังคุมคอนโด"

                else:
                    assistance.make_file(answer)
                    thread = threading.Thread(target=speaker, args=(mediaJson["answer"],))
                    thread.start()    
                    threads.append(thread)
                
                print("assistant: "+answer)
                game.set_subtitle(answer)
                thread = threading.Thread(target=game.render_subtitle, args=(0.5,))
                thread.start()    
                threads.append(thread)
                pygame.display.flip()
                game.clock.tick(10)
                
                for thread in threads:
                    thread.join()


            speaker(mediaJson["signal"])

if __name__ == "__main__":
    run()