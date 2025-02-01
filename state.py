import pygame 
from settings import * 
from characters import * 
import random
import opensimplex


class State:
    def __init__(self,game):
        self.game = game
        self.prev_state = None 

    def update(self, dt):
        pass 
    def draw(self, screen):
        pass

    def enter_state(self):
        if len(self.game.states) > 1:
            self.prev_state = self.game.states[-1]
        self.game.states.append(self)
    
    def exit_state(self):
        self.game.states.pop()


class SplashScreen(State):
    def __init__(self, game):
        State.__init__(self,game)
    
    def update(self,dt):
        if INPUTS['space']:
             Scene(self.game).enter_state()
             self.game.reset_inputs()


    def draw(self, screen):
        screen.fill(COLORS['white']) 


class Chunk:
    def __init__(self, x, y, tiles):  # x, y are chunk coordinates
        self.x = x
        self.y = y
        self.tiles = tiles  # 2D array of tile types for this chunk
        self.rect = pygame.Rect(x * CHUNK_SIZE * TILESIZE, y * CHUNK_SIZE * TILESIZE, CHUNK_SIZE * TILESIZE, CHUNK_SIZE * TILESIZE) #Rect for the chunk


class Scene(State):
    def __init__(self, game):
        State.__init__(self, game)

        self.update_sprites = pygame.sprite.Group()
        self.drawn_sprites = pygame.sprite.Group()

        self.player = Player(game, self, [self.update_sprites, self.drawn_sprites], (WIDTH / 2, HEIGHT / 2), 'player')

        self.tile_size = TILESIZE
        self.chunk_size = CHUNK_SIZE
        self.terrain = self.generate_terrain()
        self.chunks = self.generate_chunks()
        print(len(self.chunks.get((0,0)).tiles))

    def generate_terrain(self):
        seed = random.randint(0, 10000)
        noise = opensimplex.OpenSimplex(seed=seed)
        terrain = []
        for y in range(0, HEIGHT // self.tile_size):
            row = []
            for x in range(0, WIDTH // self.tile_size):
                noise_val = noise.noise2(x * 0.05, y * 0.05)
                if noise_val < -0.2:
                    tile_type = 'water'
                elif noise_val < 0.2:
                    tile_type = 'grass'
                elif noise_val < 0.5:
                    tile_type = 'dirt'
                else:
                    tile_type = 'mountain'
                row.append(tile_type)
            terrain.append(row)
        return terrain

    def generate_chunks(self):
        chunks = {}
        num_chunks_x = (WIDTH + self.chunk_size * self.tile_size -1 ) // (self.chunk_size * self.tile_size)  # Corrected calculation
        num_chunks_y = (HEIGHT + self.chunk_size * self.tile_size - 1) // (self.chunk_size * self.tile_size)  # Corrected calculation

        for y_chunk in range(num_chunks_y):
            for x_chunk in range(num_chunks_x):
                tiles = []
                for y_tile in range(y_chunk * self.chunk_size, min((y_chunk + 1) * self.chunk_size, HEIGHT // self.tile_size)): #Corrected range
                    row = []
                    for x_tile in range(x_chunk * self.chunk_size, min((x_chunk + 1) * self.chunk_size, WIDTH // self.tile_size)): #Corrected range
                        if 0 <= y_tile < len(self.terrain) and 0 <= x_tile < len(self.terrain[0]):
                            tile_type = self.terrain[y_tile][x_tile]
                        else:
                            tile_type = 'black'  # Or a default tile type
                        row.append(tile_type)
                    tiles.append(row)
                chunk = Chunk(x_chunk, y_chunk, tiles)
                chunks[(x_chunk, y_chunk)] = chunk
        return chunks

    def draw_terrain(self, screen):
        for chunk in self.chunks.values():
            for y in range(len(chunk.tiles)):  # Iterate through the actual number of rows in the chunk
                for x in range(len(chunk.tiles[0])):  # Iterate through the actual number of columns
                    tile_type = chunk.tiles[y][x]
                    color = self.get_tile_color(tile_type)
                    rect = pygame.Rect(
                        chunk.x * self.chunk_size * self.tile_size + x * self.tile_size,
                        chunk.y * self.chunk_size * self.tile_size + y * self.tile_size,
                        self.tile_size, self.tile_size
                    )
                    pygame.draw.rect(screen, color, rect)

    def get_tile_color(self, tile_type):
        if tile_type == 'water':
            return COLORS['blue']
        elif tile_type == 'grass':
            return COLORS['green']
        elif tile_type == 'dirt':
            return COLORS['brown']
        elif tile_type == 'mountain':
            return COLORS['grey']
        else:
            return COLORS['black']

    def update(self, dt):
        self.update_sprites.update(dt)

    def draw(self, screen):
        self.draw_terrain(screen)
        self.drawn_sprites.draw(screen)