import pygame 
from settings import * 
from pygame.math import Vector2 as vec 

class NPC(pygame.sprite.Sprite):
    def __init__(self,game,scene,group,pos,name):
        super().__init__(group)
        self.game = game 
        self.scene = scene 
        self.name = name 
        self.image = pygame.Surface((16,16*1.5))
        self.rect = self.image.get_rect(topleft = pos)
        self.speed = 60 
        self.force = 250
        self.acc = vec()
        self.vel = vec() 
        self.fric = -15
        self.pos = pos 
    
    def physics(self,dt):
        
        self.acc.x += self.vel.x*self.fric 
        self.vel.x += self.acc.x*dt

        self.acc.y += self.vel.y*self.fric 
        self.vel.y += self.acc.y*dt

        next_x = self.rect.centerx + self.vel.x * dt * 10
        next_y = self.rect.centery + self.vel.y * dt * 10
        next_rect = self.rect.copy()  
        next_rect.center = (next_x, next_y) 

        for y in range(max(0, next_rect.top // self.scene.tile_size), min(len(self.scene.terrain), next_rect.bottom // self.scene.tile_size + 1)): #Iterate through the rows of tiles that the player might collide with.
            for x in range(max(0, next_rect.left // self.scene.tile_size), min(len(self.scene.terrain[0]), next_rect.right // self.scene.tile_size + 1)): #Iterate through the columns of tiles that the player might collide with.
                tile_type = self.scene.terrain[y][x]
                if tile_type == 'water':
                    tile_rect = pygame.Rect(x * self.scene.tile_size, y * self.scene.tile_size, self.scene.tile_size, self.scene.tile_size)

                    if next_rect.colliderect(tile_rect): 
                        
                        dx = next_rect.centerx - tile_rect.centerx
                        dy = next_rect.centery - tile_rect.centery

                        abs_dx = abs(dx)
                        abs_dy = abs(dy)

                        if abs_dx > abs_dy: 
                            if dx > 0:
                                next_x = tile_rect.right + self.rect.width/2  
                            else:
                                next_x = tile_rect.left - self.rect.width/2 
                            self.vel.x = 0 
                        else:  
                            if dy > 0:
                                next_y = tile_rect.bottom + self.rect.height/2  
                            else:
                                next_y = tile_rect.top - self.rect.height/2 
                            self.vel.y = 0 
                        next_rect.center = (next_x,next_y) 
        self.rect.center = (next_x,next_y) 

        if self.vel.magnitude() >= self.speed:
            self.vel = self.vel.normalize() * self.speed
        
class Player(NPC):
    def __init__(self,game,scene,group,pos,name):
        super().__init__(game,scene,group,pos,name)
    
    def movement(self):
        if INPUTS['left']:
            self.acc.x = -self.force
        elif INPUTS['right']:
            self.acc.x = self.force 
        else:
            self.acc.x = 0
        

        if INPUTS['up']:
            self.acc.y = -self.force
        elif INPUTS['down']:
            self.acc.y = self.force 
        else:
            self.acc.y = 0
        
    def update(self,dt):
        self.physics(dt)
        self.movement()