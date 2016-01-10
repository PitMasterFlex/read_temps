import pygame
import os
import csv
from time import sleep
import RPi.GPIO as GPIO

data_dir = "/home/pi/projects/read_temps/data/"
data_file = data_dir + "01092016.csv"

#Colours
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)
CYAN  = (  0, 255, 255)
MAGENTA=(255,   0, 255)
YELLOW =(255, 255,   0)

os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
pygame.mouse.set_visible(False)
lcd = pygame.display.set_mode((320, 240))
lcd.fill((0,0,0))
pygame.display.update()

# Fill background
background = pygame.Surface(lcd.get_size())
background = background.convert()
background.fill(WHITE)
box = pygame.draw.rect(background, YELLOW,(40, 0, 40, 240))
box = pygame.draw.rect(background,  CYAN, (80, 0, 40, 240))
box = pygame.draw.rect(background, GREEN, (120, 0, 40, 240))
box = pygame.draw.rect(background,MAGENTA,(160, 0, 40, 240))
box = pygame.draw.rect(background, RED,   (200, 0, 40, 240))
box = pygame.draw.rect(background, BLUE  ,(240, 0, 40, 240))
box = pygame.draw.rect(background, BLACK ,(280, 0, 40, 240))

 
font_big = pygame.font.Font(None, 60)

def get_last_row(csv_filename):
    with open(csv_filename,'rb') as f:
        reader = csv.reader(f)
        lastline = reader.next()
        for line in reader:
            lastline = line
        return lastline

while True:
    temp_c = float(get_last_row(data_file)[1])
    temp = temp_c * 9.0 / 5.0 + 32.0
    lcd.fill((0,0,0))
    text_surface = font_big.render('Temp: ' + str(temp) + "F", True, WHITE)
    rect = text_surface.get_rect(center=(160,120))
    lcd.blit(text_surface, rect)
    pygame.display.update()
    sleep(5)