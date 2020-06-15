# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 15:39:48 2020

@author: Gabriel
"""
# Importando bibliotecas necessarias
import pygame
from classes import *
from assets import *

# Funcao que define o main do jogo com a variavel do tamanho do bloco inserida
def main(tamanho_bloco):
    global PAUSE
    # Início pygame
    pygame.init()

    #Início música
    pygame.mixer.init()

    #Roda aúdio de introdução
    assets['intro'].play()

    #Rodando musica de fundo
    pygame.mixer.music.play(loops=-1)


    # Definindo tamanho da tela
    size = (tamanho_bloco * (WIDTH + 9), tamanho_bloco * (HEIGHT + 2))
    screen = pygame.display.set_mode(size)
    #Nome do jogo
    pygame.display.set_caption("Tetris no Pygame")
    #Variavale para loop principal
    done = False
    #Objetos da classes Figura e Campo
    campo = Campo(WIDTH, HEIGHT, tamanho_bloco, tamanho_bloco)
    figura = Figura(WIDTH // 2 - 1, 0, random.choice([O, L, J, T, I, Z, S]), False, tamanho_bloco, tamanho_bloco)
    #Variavel de velocidade do game
    clock = pygame.time.Clock()
    #Setar o autocair das figuras
    pygame.time.set_timer(AUTOCAIR, figura.vel_auto_baixo)

    # Variavel de limite de linha do menu
    lim_esq_menu = (WIDTH + 3.5) * tamanho_bloco
    
# Loop principal do game
    
    while not done:
        # Define velocidade que a primeira figura cai para baixo e define a pontucao como 0
        vel = 1 + campo.pontuacao // divisor
        figura.vel_auto_baixo = int(0.66 ** vel * 1515)
        pontuacao_print = str((6 - len(str(campo.pontuacao))) * '0' + str(campo.pontuacao))
        pontuacao_sum = pygame.font.SysFont(font, tamanho_bloco, 1).render(pontuacao_print, 1, RED)

        # Desenha info na tela como Prox. Figura, Pontuacao, Linhas etc 
        screen.fill((0, 255, 0))
        for i in range(HEIGHT):
            screen.blit(pygame.font.SysFont(font, int(tamanho_bloco * 0.7), True)
                        .render((str((HEIGHT - i))), 1, (200, 100, 100)), (3, tamanho_bloco * (i + 1)))

        screen.blit(pygame.font.SysFont(font, tamanho_bloco, True)
                    .render("Pontuacao:", 1, RED), (lim_esq_menu, tamanho_bloco))
        screen.blit(pontuacao_sum, (lim_esq_menu, tamanho_bloco * 2.1))
        screen.blit(pygame.font.SysFont(font, tamanho_bloco, True)
                    .render("Fig Nova:", 1, RED), (lim_esq_menu, tamanho_bloco * 3.2))
        screen.blit(pygame.font.SysFont(font, tamanho_bloco, True)
                    .render("Linhas:", 1, RED), (lim_esq_menu, tamanho_bloco * 9))
        screen.blit(pygame.font.SysFont(font, tamanho_bloco, True)
                    .render(str(campo.lines), 1, RED), (lim_esq_menu, tamanho_bloco * 10))
        screen.blit(pygame.font.SysFont(font, tamanho_bloco, True)
                    .render("Level:", 1, RED), (lim_esq_menu, tamanho_bloco * 12))
        screen.blit(pygame.font.SysFont(font, tamanho_bloco, True)
                    .render("=========", 1, RED), (lim_esq_menu, tamanho_bloco * 13))
        screen.blit(pygame.font.SysFont(font, tamanho_bloco, True)
                    .render("[P] = Pause", 1, RED), (lim_esq_menu, tamanho_bloco * 14))
        
        # Quando o campo for inicializado os objetos são chamados desenhando o campo e as figuras
        if campo.game:

            #Música começa a tocar
            mixer.music.set_volume(0.1)
            campo.draw(screen)
            figura.draw(screen)
            campo.fly_points(screen)

            # Loop para realizar desenho da proxima figura a aparecer
            for i in range(len(figura.prox_figura)):
                for j in range(len(figura.prox_figura[i])):
                    if figura.prox_figura[i][j]:
                        pygame.draw.rect(screen, WHITE,
                                         [int(tamanho_bloco * (i + WIDTH + 4.35)), int((j + 4.85) * tamanho_bloco),
                                          int(tamanho_bloco * 0.3), int(tamanho_bloco * 0.3)])
                        pygame.draw.lines(screen, WHITE, 1,
                                          [(tamanho_bloco * (i + WIDTH + 4) + 1, (j + 4.5) * tamanho_bloco + 1),
                                           (tamanho_bloco * (i + WIDTH + 4) + 1, (j + 5.5) * tamanho_bloco - 3),
                                           (tamanho_bloco * (i + WIDTH + 5) - 3, (j + 5.5) * tamanho_bloco - 3),
                                           (tamanho_bloco * (i + WIDTH + 5) - 3, (j + 4.5) * tamanho_bloco + 1)], 4)
    
        # Verifica açao do player, e para cada respectiva acao o jogo realiza algô 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif figura.GAME_OVER:
                    pass
                 # Se tecla P nao estiver apertada Pause nao ocorre
                elif PAUSE and event.type == pygame.KEYDOWN and (
                        event.key == pygame.K_p or event.key == pygame.K_ESCAPE):
                    PAUSE = False
                # Se tecla P estiver apertada Pause ocorre
                elif not PAUSE and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        PAUSE = True
                    # Ao apertar seta para baixo velocidade da figura aumenta
                    elif event.key == pygame.K_DOWN:
                        if figura.vel_auto_baixo > 100:
                            pygame.time.set_timer(AUTOCAIR, 50)
                        figura.move_figura(campo)
                    # Move figura para esquerda , left
                    elif event.key == pygame.K_LEFT and figura.movimentacao(campo, "l"):
                        figura.move_p_esquerda()
                    # Move figura para direite, right
                    elif event.key == pygame.K_RIGHT and figura.movimentacao(campo, "r"):
                        figura.move_p_direita()
                    # Verifica rotacao e rotaciona a fugura com a seta cima apertada
                    elif event.key == pygame.K_UP and figura.verifica_rotacao(campo):
                        figura.rotacao()
                elif PAUSE:
                    pass
                # Verifica acao de tecla apos o pause
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        pygame.time.set_timer(AUTOCAIR, figura.vel_auto_baixo)
                elif event.type == AUTOCAIR:
                    figura.move_figura(campo)
        # Saida do game
        if not campo.game or PAUSE or figura.GAME_OVER:
            pygame.mixer.music.pause()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            # Definindo variáveis de mouse e click para usar caso os botoes de menu forem acionados ao pressionar/clicar na tela          
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            
            # Caso o player pressiona "p" ou barra de espaço desenha na tela quadrados com botões de continuar, reiniciar ou sair do game
            if PAUSE:
                # Pausa a música de fundo
                pygame.mixer.music.pause()

                # Variaveis do bloco
                b0x1 = tamanho_bloco * 3
                b0x2 = tamanho_bloco * (WIDTH - 4)
                b0y1 = tamanho_bloco * 3
                b0y2 = tamanho_bloco * 2

                #Dsenha o bloco
                pygame.draw.rect(screen, (0, 100, 200), (b0x1, b0y1, b0x2, b0y2))
                screen.blit(pygame.font.SysFont(font, tamanho_bloco, True).render("CONTINUE", 1, (0, 0, 100)),
                            (b0x1 + WIDTH / 15 * tamanho_bloco, b0y1 + tamanho_bloco / 2))

            # Variaveis do bloco
            b1x1 = tamanho_bloco * 3
            b1x2 = tamanho_bloco * (WIDTH - 4)
            b1y1 = tamanho_bloco * 6
            b1y2 = tamanho_bloco * 2

            # Desenha o bloco
            pygame.draw.rect(screen, (0, 100, 200), (b1x1, b1y1, b1x2, b1y2))
            screen.blit(pygame.font.SysFont(font, tamanho_bloco, True).render(
                "START" if not PAUSE and not figura.GAME_OVER else "RESTART", 1, (0, 0, 100)),
                (b1x1 + WIDTH / 7.5 * tamanho_bloco, b1y1 + tamanho_bloco / 2))

            # Variaveis do bloco
            b2x1 = tamanho_bloco * 3
            b2x2 = tamanho_bloco * (WIDTH - 4)
            b2y1 = tamanho_bloco * 9
            b2y2 = tamanho_bloco * 2

            # Desenha o bloco
            pygame.draw.rect(screen, (0, 100, 200), (b2x1, b2y1, b2x2, b2y2))
            screen.blit(pygame.font.SysFont(font, tamanho_bloco, True).render("EXIT", 1, (0, 0, 100)),
                        (b2x1 + WIDTH / 5 * tamanho_bloco, b2y1 + tamanho_bloco / 2))

            # Recomeca o game do início, música volta a tocar
            if (b1x1 + b1x2) > mouse[0] > b1x1 and (b1y1 + b1y2) > mouse[1] > b1y1 and click[0] == 1:
                PAUSE = False
                campo.recomecar()
                figura = figura.recomecar()
                pygame.time.set_timer(AUTOCAIR, figura.vel_auto_baixo)
                pygame.mixer.music.play(loops=-1)
             
            # Fecha o game
            elif (b2x1 + b2x2) > mouse[0] > b2x1 and (b2y1 + b2y2) > mouse[1] > b2y1 and click[0] == 1:
                done = True
                
            # Quando PAUSE estiver pausado recomeça de onde o jogo e a música pararam
            elif PAUSE and (b0x1 + b0x2) > mouse[0] > b0x1 and (b0y1 + b0y2) > mouse[1] > b0y1 and click[0] == 1:
                PAUSE = False
                pygame.mixer.music.unpause()


        # Inverte o display
        pygame.display.flip()
        # FPS 
        clock.tick(60)
    # Saida do pygame    
    pygame.quit()

# Gostaria de ressaltar aqui a importância que alguns, tutorias pela internet que serviram de inspiração para a realização deste projeto, 
# entre eles vou citar alguns: freeCodeCamp.org, Tech with Tim, forum do site Pygame. Estes me ajudaram a realizar o código em diversos 
# momentos para entender e aplicar melhor alguns códigos.