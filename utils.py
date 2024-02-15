import json
import pygame
import time

def speaker(filepath):
    pygame.mixer.init()
    pygame.mixer.music.load(filepath)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

        
def load_json_file(file_path):
    with open(file_path) as json_file:
        data = json.load(json_file)
    return data

