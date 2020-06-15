# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 15:22:14 2020

@author: Gabriel
"""
#Importando bibliotecas necessárias
import pygame
from os import path
from pygame import mixer


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

# Iniciar assets:
assets = {}

# Carregando sons do jogo: 
mixer.music.load(path.join(som_dir, "TetrisFundo.wav"))
# Música começa zerada para rodar aúdio de introdução
mixer.music.set_volume(0)
assets['acerto'] = mixer.Sound(path.join(som_dir, "jogada1.wav"))
mixer.Sound.set_volume(assets['acerto'] ,0.5)
assets['intro'] = mixer.Sound(path.join(som_dir, "intro.wav"))
mixer.Sound.set_volume(assets['intro'] ,0.5)

# Gostaria de ressaltar aqui a importância que alguns, tutorias pela internet que serviram de inspiração para a realização deste projeto, 
# entre eles vou citar alguns: freeCodeCamp.org, Tech with Tim, forum do site Pygame. Estes me ajudaram a realizar o código em diversos 
# momentos para entender e aplicar melhor alguns códigos.