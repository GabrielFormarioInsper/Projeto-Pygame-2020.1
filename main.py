# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 15:39:48 2020

@author: Gabriel
"""
import pygame
from classes import *
from assets import *

# Funcao que define o main do jogo com a variavel do tamanho do bloco inserida
def main(tamanho_bloco):
    global PAUSE
    pygame.init()
    pygame.mixer.init()

    #Rodando musica de fundo
    pygame.mixer.music.play(loops=-1)

    size = (tamanho_bloco * (WIDTH + 9), tamanho_bloco * (HEIGHT + 2))
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tetris no Pygame")
    done = False
    campo = Campo(WIDTH, HEIGHT, tamanho_bloco, tamanho_bloco)
    figura = Figura(WIDTH // 2 - 1, 0, random.choice([O, L, J, T, I, Z, S]), False, tamanho_bloco, tamanho_bloco)
    clock = pygame.time.Clock()
    pygame.time.set_timer(AUTOCAIR, figura.vel_auto_baixo)


    menu_left_line = (WIDTH + 4) * tamanho_bloco
    
# Loop principal do game
    
    while not done:
        vel = 1 + campo.pontuacao // divisor
        figura.vel_auto_baixo = int(0.66 ** vel * 1515)
        pontuacao_print = str((6 - len(str(campo.pontuacao))) * '0' + str(campo.pontuacao))
        pontuacao_sum = pygame.font.SysFont(font, tamanho_bloco, 1).render(pontuacao_print, 1, RED)

        # Desenha info na tela como Prox. Figura, Pontuacao, Linhas etc
        screen.fill((0, 255, 0))
        for i in range(HEIGHT):
            screen.blit(pygame.font.SysFont(font, int(tamanho_bloco * 0.7), True)
                        .render((str((HEIGHT - i))), 1, (200, 100, 100)), (3, tamanho_bloco * (i + 1)))
            screen.blit(pygame.font.SysFont(font, int(tamanho_bloco * 0.7), True)
                        .render(("+" + str((HEIGHT - i - 1) * 25)), 1, (200, 100, 100)),
                        ((WIDTH + 1) * tamanho_bloco + 3, tamanho_bloco * (i + 1)))
        screen.blit(pygame.font.SysFont(font, tamanho_bloco, True)
                    .render("Pontuacao:", 1, RED), (menu_left_line, tamanho_bloco))
        screen.blit(pontuacao_sum, (menu_left_line, tamanho_bloco * 2))
        screen.blit(pygame.font.SysFont(font, tamanho_bloco, True)
                    .render("Prox. Figura", 1, RED), (menu_left_line, tamanho_bloco * 3))
        screen.blit(pygame.font.SysFont(font, tamanho_bloco, True)
                    .render("Linhas:", 1, RED), (menu_left_line, tamanho_bloco * 9))
        screen.blit(pygame.font.SysFont(font, tamanho_bloco, True)
                    .render(str(campo.lines), 1, RED), (menu_left_line, tamanho_bloco * 10))
        screen.blit(pygame.font.SysFont(font, tamanho_bloco, True)
                    .render("Level:", 1, RED), (menu_left_line, tamanho_bloco * 11))
        screen.blit(pygame.font.SysFont(font, tamanho_bloco, True)
                    .render(str(vel), 1, RED), (menu_left_line, tamanho_bloco * 12))
        
        # Quando o game estiver on
        if campo.game:
            campo.draw(screen)
            figura.draw(screen)
            campo.fly_points(screen)

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
    
        # Verifica açao do player e realiza açoes 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif figura.GAME_OVER:
                    pass
                elif PAUSE and event.type == pygame.KEYDOWN and (
                        event.key == pygame.K_p or event.key == pygame.K_ESCAPE):
                    PAUSE = False
                elif not PAUSE and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                        PAUSE = True
                    elif event.key == pygame.K_DOWN:
                        if figura.vel_auto_baixo > 100:
                            pygame.time.set_timer(AUTOCAIR, 50)
                        figura.move_figura(campo)
                    elif event.key == pygame.K_LEFT and figura.movimentacao(campo, "l"):
                        figura.move_p_esquerda()
                    elif event.key == pygame.K_RIGHT and figura.movimentacao(campo, "r"):
                        figura.move_p_direita()
                    elif event.key == pygame.K_UP and figura.verifica_rotacao(campo):
                        figura.rotacao()
                elif PAUSE:
                    pass
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        pygame.time.set_timer(AUTOCAIR, figura.vel_auto_baixo)
                elif event.type == AUTOCAIR:
                    figura.move_figura(campo)

        if not campo.game or PAUSE or figura.GAME_OVER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            # Definindo variáveis de mouse e click para usar caso os botoes de menu forem acionados ao pressionar/clicar na tela          
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            
            # Caso o player pressiona "p" ou barra de espaço desenha na tela quadrados com botões de continuar, reiniciar ou sair do game
            if PAUSE:
                b0x1 = tamanho_bloco * 3
                b0x2 = tamanho_bloco * (WIDTH - 4)
                b0y1 = tamanho_bloco * 3
                b0y2 = tamanho_bloco * 2
                pygame.draw.rect(screen, (0, 100, 200), (b0x1, b0y1, b0x2, b0y2))
                screen.blit(pygame.font.SysFont(font, tamanho_bloco, True).render("Continuar", 1, (0, 0, 100)),
                            (b0x1 + WIDTH / 8 * tamanho_bloco, b0y1 + tamanho_bloco / 2))

            b1x1 = tamanho_bloco * 3
            b1x2 = tamanho_bloco * (WIDTH - 4)
            b1y1 = tamanho_bloco * 6
            b1y2 = tamanho_bloco * 2
            pygame.draw.rect(screen, (0, 100, 200), (b1x1, b1y1, b1x2, b1y2))
            screen.blit(pygame.font.SysFont(font, tamanho_bloco, True).render(
                "Start" if not PAUSE and not figura.GAME_OVER else "Restart", 1, (0, 0, 100)),
                (b1x1 + WIDTH / 6 * tamanho_bloco, b1y1 + tamanho_bloco / 2))
            b2x1 = tamanho_bloco * 3
            b2x2 = tamanho_bloco * (WIDTH - 4)
            b2y1 = tamanho_bloco * 9
            b2y2 = tamanho_bloco * 2
            pygame.draw.rect(screen, (0, 100, 200), (b2x1, b2y1, b2x2, b2y2))
            screen.blit(pygame.font.SysFont(font, tamanho_bloco, True).render("EXIT", 1, (0, 0, 100)),
                        (b2x1 + WIDTH / 5 * tamanho_bloco, b2y1 + tamanho_bloco / 2))

            # Recomeca o game da onde ele parou
            if (b1x1 + b1x2) > mouse[0] > b1x1 and (b1y1 + b1y2) > mouse[1] > b1y1 and click[0] == 1:
                PAUSE = False
                campo.recomecar()
                figura = figura.recomecar()
                pygame.time.set_timer(AUTOCAIR, figura.vel_auto_baixo)
             
            # Fecha o game
            elif (b2x1 + b2x2) > mouse[0] > b2x1 and (b2y1 + b2y2) > mouse[1] > b2y1 and click[0] == 1:
                done = True
                
            # Recomeca o game do inicio 
            elif PAUSE and (b0x1 + b0x2) > mouse[0] > b0x1 and (b0y1 + b0y2) > mouse[1] > b0y1 and click[0] == 1:
                PAUSE = False

        pygame.display.flip()
        # FPS 
        clock.tick(60)
    pygame.quit()

# Roda a funcao main
main(tamanho_bloco)
