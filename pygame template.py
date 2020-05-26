# Pygame template - skeleton for a new pygame project
import pygame
#import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 800
HEIGHT = 480
FPS = 60
TILE_SIZE = 40 # Tamanho de cada tile (cada tile é um quadrado)

player_img = 'player_img'

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define os tipos de tiles
BLOCK = 0
EMPTY = -1

# Define a aceleração da gravidade
GRAVITY = 5
# Define a velocidade inicial no pulo
JUMP_SIZE = TILE_SIZE
# Define a velocidade em x
SPEED_X = 5

MAP = [
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
    [EMPTY, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, EMPTY, EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
    [EMPTY, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, BLOCK, EMPTY, EMPTY, EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
    [BLOCK, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, BLOCK, EMPTY, EMPTY, EMPTY, BLOCK, BLOCK,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY,EMPTY],
]

# Define estados possíveis do jogador
STILL = 0
JUMPING = 1
FALLING = 2


# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Class que representa os blocos do cenário
class Tile(pygame.sprite.Sprite):

    # Construtor da classe.
    def __init__(self, tile_img, row, column):
        # Construtor da classe pai (Sprite).
        pygame.sprite.Sprite.__init__(self)

        # Aumenta o tamanho do tile.
        tile_img = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))

        # Define a imagem do tile.
        self.image = tile_img
        # Detalhes sobre o posicionamento.
        self.rect = self.image.get_rect()

        # Posiciona o tile
        self.rect.x = TILE_SIZE * column
        self.rect.y = TILE_SIZE * row
        
        
class Player(pygame.sprite.Sprite):
    def __init__(self, player_img, row, column, blocks):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (64, 64))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
    

    def update(self):
        self.vx, self.vy = 0, 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.vy = -5
        if keystate[pygame.K_DOWN]:
            self.vy = 5
        if keystate[pygame.K_LEFT]:
            self.vx = -2
        if keystate[pygame.K_RIGHT]:
            self.vx = 1
        if self.vx != 0 and self.vy != 0:
            self.vx /= 1.414
            self.vy /= 1.414
        self.rect.x += self.vx
        self.rect.y += self.vy
    

#player_img = pygame.image.load(path.join(img_dir, "p1_jump.png")).convert()

# Carrega todos os assets de uma vez.
def load_assets(img_dir):
    assets = {}
    assets[player_img] = pygame.image.load(path.join(img_dir, "p1_jump.png")).convert_alpha()
    assets[BLOCK] = pygame.image.load(path.join(img_dir, 'tile-block.png')).convert()
    return assets



def game_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # Carrega assets
    assets = load_assets(img_dir)

    # Cria um grupo de todos os sprites.
    all_sprites = pygame.sprite.Group()
    # Cria um grupo somente com os sprites de bloco.
    # Sprites de block são aqueles que impedem o movimento do jogador
    blocks = pygame.sprite.Group()

    # Cria Sprite do jogador
    player = Player(assets[player_img], 12, 2, blocks)

    # Cria tiles de acordo com o mapa
    for row in range(len(MAP)):
        for column in range(len(MAP[row])):
            tile_type = MAP[row][column]
            if tile_type == BLOCK:
                tile = Tile(assets[tile_type], row, column)
                all_sprites.add(tile)
                blocks.add(tile)

    all_sprites.add(player)
    
    PLAYING = 0
    DONE = 1

    state = PLAYING
    while state != DONE:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS)

        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():

            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = DONE

        # Depois de processar os eventos.
        # Atualiza a acao de cada sprite. O grupo chama o método update() de cada Sprite dentre dele.
        all_sprites.update()

        # A cada loop, redesenha o fundo e os sprites
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

# Comando para evitar travamentos.
try:
    game_screen(screen)
finally:
    pygame.quit()



# Para nao esquecer:
    # Partes de codigos foram feitas com base nos exemplos disponiveis pelos professores e tambem pelo site de programcao KidsCanCode 
    # principalmente na parte de powerups e construcao de cenarios para o game.