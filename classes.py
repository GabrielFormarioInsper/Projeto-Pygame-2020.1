# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 15:26:38 2020

@author: Gabriel
"""
import pygame
import random

from assets import *

# Classe que representa o campo de jogar
class Campo:
    def __init__(self, width, height, comeco_x=tamanho_bloco, comeco_y=tamanho_bloco):
        self.width = width
        self.height = height
        self.campo = [[1] * 4 + [0] * (self.width - 6) + [1] * 4] * 2 + \
                     [([1] + [0] * self.width + [1]) for i in range(self.height)] + [[1] * (self.width + 2)]
        self.pontuacao = 0
        self.k = self.lines = 0
        self.pontuacao_plus = self.pontuacao_up = 0
        self.comeco_x, self.comeco_y = comeco_x, comeco_y
        self.frames = 0
        self.game = False
        self.figura_last_x = 0
        self.figura_last_y = 0

# Todas as funçoes que fazem parte da Classe Campo
        
    # Funcao de desenho
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 200, 100), (self.comeco_x, self.comeco_y, WIDTH * tamanho_bloco, HEIGHT * tamanho_bloco))
        for i in range(2, self.height + 2):
            for j in range(1, self.width + 1):
                if self.campo[i][j]:
                    pygame.draw.rect(screen, RED,
                                     [self.comeco_x + int((j - 0.65) * tamanho_bloco),
                                      self.comeco_y + int((i - 1.65) * tamanho_bloco),
                                      tamanho_bloco - int(tamanho_bloco * 0.7), tamanho_bloco - int(tamanho_bloco * 0.7)])
                    pygame.draw.lines(screen, RED, 1,
                                      [(self.comeco_x + (j - 1) * tamanho_bloco + 1, self.comeco_y + (i - 2) * tamanho_bloco + 1),
                                       (self.comeco_x + (j - 1) * tamanho_bloco + 1, self.comeco_y + (i - 1) * tamanho_bloco - 3),
                                       (self.comeco_x + j * tamanho_bloco - 3, self.comeco_y + (i - 1) * tamanho_bloco - 3),
                                       (self.comeco_x + j * tamanho_bloco - 3, self.comeco_y + (i - 2) * tamanho_bloco + 1)], 4)
    #Funcao para adicionar figura
    def add_figura(self, figura):
        for i in range(len(figura.figura)):
            for j in range(len(figura.figura[i])):
                if figura.figura[i][j]:
                    self.campo[j + figura.y][i + figura.x] = 1
                    
    # Funcao para checar a linha que a figura está/parou
    def checa_linha(self):
        self.pontuacao_up = 0
        for i in range(HEIGHT + 2):
            if (0 not in self.campo[i]) and (i != (HEIGHT + 2)):
                self.campo.pop(i)
                self.campo.insert(2, ([1] + [0] * self.width + [1]))
                self.k += 1
                self.lines += 1
                self.figura_last_y = i
                self.pontuacao_plus = 100 * (self.k ** 2 - (self.k - 1) ** 2) + 25 * (self.height - i + 1)
                self.pontuacao_up += self.pontuacao_plus
                self.pontuacao += self.pontuacao_plus

    def fly_points(self, screen):
        if self.k > 0 and self.frames < 80:
            pontuacao_plus = pygame.font.SysFont(font, int(tamanho_bloco + tamanho_bloco / 4 * self.k)) \
                .render(("+" + str(self.pontuacao_up)), 0, (100, 100, 100, 10))
            pontuacao_plus.set_alpha(160 - self.frames * 2)
            screen.blit(pontuacao_plus, ((self.figura_last_x * tamanho_bloco - 10),
                                     (self.figura_last_y * tamanho_bloco - 50 - self.frames / 2)))
            self.frames += 1
        else:
            self.frames = 0
            self.k = 0

    # Funcao para recomecar o game
    def recomecar(self):
        self.game = True
        self.campo = [[1] * 4 + [0] * (self.width - 6) + [1] * 4] * 2 + \
                     [([1] + [0] * self.width + [1]) for i in range(self.height)] + [[1] * (self.width + 2)]
        self.lines = 0
        self.pontuacao = 0
        

# Classe que representa as figuras do Tetris
class Figura:
    def __init__(self, x, y, form, GAME_OVER, comeco_x=tamanho_bloco, comeco_y=tamanho_bloco):
        self.x = x
        self.y = y
        self.press_down = False
        self.GAME_OVER = GAME_OVER
        self.comeco_x, self.comeco_y = comeco_x, comeco_y
        self.figura = form
        self.prox_figura = self.figura_nova()
        self.vel_auto_baixo = 1000
        
        
# Todas as funcoes que fazem parte da classe Figura
    def draw(self, screen):
        for i in range(len(self.figura)):
            for j in range(len(self.figura[i])):
                if self.figura[i][j] and (((self.y + j - 1) * tamanho_bloco) > 0):
                    pygame.draw.rect(screen,
                                     BLACK,
                                     [self.comeco_x + int((self.x + i - 0.65) * tamanho_bloco),
                                      self.comeco_y + int((self.y + j - 1.65) * tamanho_bloco),
                                      tamanho_bloco - int(tamanho_bloco * 0.7),
                                      tamanho_bloco - int(tamanho_bloco * 0.7)])
                    pygame.draw.lines(screen, BLACK, 1, [(self.comeco_x + (self.x + i - 1) * tamanho_bloco + 1,
                                                          self.comeco_y + (self.y + j - 2) * tamanho_bloco + 1),
                                                         (self.comeco_x + (self.x + i - 1) * tamanho_bloco + 1,
                                                          self.comeco_y + (self.y + j - 1) * tamanho_bloco - 3),
                                                         (self.comeco_x + (self.x + i) * tamanho_bloco - 3,
                                                          self.comeco_y + (self.y + j - 1) * tamanho_bloco - 3),
                                                         (self.comeco_x + (self.x + i) * tamanho_bloco - 3,
                                                          self.comeco_y + (self.y + j - 2) * tamanho_bloco + 1)], 4)
  #Funcoes de movimentacao da figura
    def move_p_baixo(self):
        self.y += 1

    def move_p_esquerda(self):
        self.x -= 1

    def move_p_direita(self):
        self.x += 1

    def movimentacao(self, campo, side):
        new_x = self.x
        new_y = self.y
        if side == "d":
            new_y += 1
        elif side == "l":
            new_x -= 1
        elif side == "r":
            new_x += 1

        for i in range(len(self.figura)):
            for j in range(len(self.figura[i])):
                if self.figura[i][j] and campo.campo[new_y + j][new_x + i]:
                    return False
        return True

    def rotacao(self, n=1):
        for i in range(n):
            self.figura = list(zip(*reversed(self.figura)))

    def verifica_rotacao(self, campo):
        forma_nova = list(zip(*reversed(self.figura)))
        for i in range(len(forma_nova)):
            for j in range(len(forma_nova[i])):
                if forma_nova[i][j] and campo.campo[self.y + j][self.x + i]:
                    return False
        return True
    
    #Funcao de fim de jogo
    def game_over(self, campo):
        for i in range(len(self.figura)):
            for j in range(len(self.figura[i])):
                if self.figura[i][j] and campo.campo[self.y + j][self.x + i]:
                    self.GAME_OVER = True

    def figura_nova(self):
        self.prox_figura = random.choice([O, L, J, T, I, Z, S])
        for i in range(random.randint(1, 4)):
            self.prox_figura = list(zip(*reversed(self.prox_figura)))
        return self.prox_figura

    def move_figura(self, campo):
        if self.movimentacao(campo, "d"):
            self.move_p_baixo()
        else:
            campo.figura_last_x = self.x
            campo.add_figura(self)
            campo.checa_linha()
            self.figura = self.prox_figura
            self.x = WIDTH // 2 - 1
            self.y = 0
            self.figura_nova()
            self.game_over(campo)

# Funcao para colocar um figura aleatoria na tela 
    def recomecar(self):
        self.vel_auto_baixo = 1000
        return Figura(WIDTH // 2 - 1, 0, random.choice([O, L, J, T, I, Z, S]), False, tamanho_bloco, tamanho_bloco)