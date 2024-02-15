import pygame
import sys
import math
import time
# Initialize pygame
pygame.init()

# Constants for screen dimensions and colors
SCREEN_WIDTH = 1270
SCREEN_HEIGHT = 620

BLACK = (0, 0, 0)
RED = (255, 0, 0)

class FaceGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.BACKGROUND_COLOR = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.current_face = self.draw_default_face
        self.subtitle = ''
        self.font = pygame.font.Font('font/THSarabun.ttf', 60)  # Default pygame font, size 36

    def change_face(self, face_function):
        self.current_face = face_function

    def draw_default_face(self):
        # Eyes
        pygame.draw.rect(self.screen, BLACK, (300, 250, 50, 50))
        pygame.draw.line(self.screen, RED, (300, 250), (350, 300), 5)
        pygame.draw.line(self.screen, RED, (300, 300), (350, 250), 5)
        # Right eye
        pygame.draw.rect(self.screen, BLACK, (450, 250, 50, 50))


    def set_subtitle(self, text):
        self.subtitle = text

    def render_subtitle(self,typing_speed):
        # Render the subtitle text at the bottom of the screen
        for i in range(len(self.subtitle) + 1):
            # Clear the screen
            self.screen.fill(self.BACKGROUND_COLOR)

            text_surface = self.font.render(self.subtitle[:i], True, BLACK)
            # Position the text at the bottom center of the screen
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            # Draw the text onto the screen
            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()
            # Wait for a short period to simulate typing
            
            time.sleep(typing_speed)