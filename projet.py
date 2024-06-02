##
## EPITECH PROJECT, 2024
## Jam-Epitech
## File description:
## projet.py
##

import pygame
import sys 

#initialisation de pygame
pygame.init()

#créer une fenêtre
screen_witdh = 900
screen_height = 950
screen = pygame.display.set_mode((screen_witdh, screen_height))
timer = pygame.time.Clock()
fps = 60
pygame.display.set_caption("ROMANIA4EVER")

#initialiser les couleurs
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

pygame. display. set_mode((0, 0), pygame. FULLSCREEN)
pygame.display.flip()

#boucle principal

running = True
while running:
    
    timer.ticks(fps)
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    
#quitter pygame
pygame.quit()
sys.exit()


