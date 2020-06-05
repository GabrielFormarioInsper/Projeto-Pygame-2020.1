# Pygame template - skeleton for a new pygame project
import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (100, 100, 100)
RED = (255, 100, 0)

WIDTH = 10
HEIGHT = 15
tamanho_bloco = 20
AUTOCAIR = pygame.USEREVENT + 1

GAME_OVER = False
PAUSE = False
divisor = 300
font = "Arial"

O = [[1, 1], [1, 1]]
L = [[0, 0, 0], [1, 1, 1], [0, 0, 1]]
J = [[0, 0, 1], [1, 1, 1], [0, 0, 0]]
T = [[0, 1, 0], [0, 1, 1], [0, 1, 0]]
I = [[0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]
Z = [[1, 0], [1, 1], [0, 1]]
S = [[0, 1], [1, 1], [1, 0]]


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

    def add_figura(self, figura):
        for i in range(len(figura.figura)):
            for j in range(len(figura.figura[i])):
                if figura.figura[i][j]:
                    self.campo[j + figura.y][i + figura.x] = 1

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

    def recomecar(self):
        self.game = True
        self.campo = [[1] * 4 + [0] * (self.width - 6) + [1] * 4] * 2 + \
                     [([1] + [0] * self.width + [1]) for i in range(self.height)] + [[1] * (self.width + 2)]
        self.lines = 0
        self.pontuacao = 0


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

    def recomecar(self):
        self.vel_auto_baixo = 1000
        return Figura(WIDTH // 2 - 1, 0, random.choice([O, L, J, T, I, Z, S]), False, tamanho_bloco, tamanho_bloco)


def main(tamanho_bloco):
    global PAUSE
    pygame.init()


    size = (tamanho_bloco * (WIDTH + 9), tamanho_bloco * (HEIGHT + 2))
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Tetris no Pygame")
    done = False
    campo = Campo(WIDTH, HEIGHT, tamanho_bloco, tamanho_bloco)
    figura = Figura(WIDTH // 2 - 1, 0, random.choice([O, L, J, T, I, Z, S]), False, tamanho_bloco, tamanho_bloco)
    clock = pygame.time.Clock()
    pygame.time.set_timer(AUTOCAIR, figura.vel_auto_baixo)


    menu_left_line = (WIDTH + 4) * tamanho_bloco

    while not done:
        vel = 1 + campo.pontuacao // divisor
        figura.vel_auto_baixo = int(0.66 ** vel * 1515)
        pontuacao_print = str((6 - len(str(campo.pontuacao))) * '0' + str(campo.pontuacao))
        pontuacao_sum = pygame.font.SysFont(font, tamanho_bloco, 1).render(pontuacao_print, 1, RED)

        # draw info on the window
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

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

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

            if (b1x1 + b1x2) > mouse[0] > b1x1 and (b1y1 + b1y2) > mouse[1] > b1y1 and click[0] == 1:
                PAUSE = False
                campo.recomecar()
                figura = figura.recomecar()
                pygame.time.set_timer(AUTOCAIR, figura.vel_auto_baixo)
            elif (b2x1 + b2x2) > mouse[0] > b2x1 and (b2y1 + b2y2) > mouse[1] > b2y1 and click[0] == 1:
                done = True
            elif PAUSE and (b0x1 + b0x2) > mouse[0] > b0x1 and (b0y1 + b0y2) > mouse[1] > b0y1 and click[0] == 1:
                PAUSE = False

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


main(tamanho_bloco)



# Para nao esquecer:
    # Partes de codigos foram feitas com base nos exemplos disponiveis pelos professores e tambem pelo site de programcao KidsCanCode 
    # principalmente na parte de powerups e construcao de cenarios para o game.