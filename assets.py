# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 15:22:14 2020

@author: Gabriel
"""
import pygame
from os import path
from pygame import mixer
#from classes import *

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (100, 100, 100)
RED = (255, 100, 0)


#Pasta que contêm os arquivos:
som_dir = path.join(path.dirname(__file__), 'sons')

# Variaveis globais
WIDTH = 10
HEIGHT = 15
tamanho_bloco = 20
AUTOCAIR = pygame.USEREVENT + 1

GAME_OVER = False
PAUSE = False
divisor = 300
font = "Arial"

#Som
pygame.mixer.init()

#Clock
clock = pygame.time.Clock()


# Técnica para fazer formato das figuras do tetris 
O = [[1, 1], [1, 1]]
L = [[0, 0, 0], [1, 1, 1], [0, 0, 1]]
J = [[0, 0, 1], [1, 1, 1], [0, 0, 0]]
T = [[0, 1, 0], [0, 1, 1], [0, 1, 0]]
I = [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]
Z = [[1, 0], [1, 1], [0, 1]]
S = [[0, 1], [1, 1], [1, 0]]



# Carregando sons do jogo: 
mixer.music.load(path.join(som_dir, "musica.mp3"))
mixer.music.set_volume(0.3)

