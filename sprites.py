import pygame as pg
from window import *
import random
vec = pg.math.Vector2
class Player(pg.sprite.Sprite):
        def __init__(self, game):
                pg.sprite.Sprite.__init__(self)
                self.game = game
                self.jumping=False
                self.walk=False
                self.frame=0
                self.last_update=0
                self.load_img()
                self.radius=10
                self.image = self.stand_pos[0]
                self.image.set_colorkey(WHITE)
                self.rect = self.image.get_rect()
                self.rect.center = (WIDTH / 2, HEIGHT / 2)
                self.pos = vec(WIDTH / 2, HEIGHT / 2)
                self.vel = vec(0, 0)
                self.acc = vec(0, 0)
        def load_img(self):
                self.stand_pos=[self.game.spritesheet.get_image(0,0,37,50), self.game.spritesheet.get_image(37,0,37,50)]
                self.walk_pos=[ self.game.spritesheet.get_image(37,50,37,50),self.game.spritesheet.get_image(0,100,37,50)]
                self.walk_array=[]
                for frame in self.walk_pos:
                        self.walk_array.append(pg.transform.flip(frame,True,False))
                
        def jump(self):
        # jump only if standing on a platform
                self.rect.x += 2
                hits = pg.sprite.spritecollide(self, self.game.platforms, False)
                self.rect.x -= 2
                if hits and not self.jumping :
                  self.vel.y = -PLAYER_JUMP
                  self.jumping=True
        def jump_cut(self):
                if self.jumping:
                      if self.vel.y<-4:
                              
                              self.vel.y=-4
        def update(self):
                        self.anime()
                        self.acc = vec(0, PLAYER_GRAV)
                        keys = pg.key.get_pressed()
                        if keys[pg.K_LEFT]:
                         self.acc.x = -PLAYER_ACC
                        if keys[pg.K_RIGHT]:
                         self.acc.x = PLAYER_ACC
                        # apply friction
                        self.acc.x += self.vel.x * PLAYER_FRICTION
                        # equations of motion
                        self.vel += self.acc
                        if abs(self.vel.x)<0.05:
                                self.vel.x=0
                        self.pos += self.vel + 0.5 * self.acc

                        if self.pos.x > WIDTH:
                         self.pos.x = 0
                        if self.pos.x < 0:
                         self.pos.x = WIDTH
                        self.rect.midbottom = self.pos
                       
        def anime(self):
                now=pg.time.get_ticks()
                #animation for left/right pos
                if self.vel.x!=0:
                        self.walk=True
                else:
                        self.walk=False
                if self.walk:
                        if now-self.last_update>200:
                                self.last_update=now
                                if self.vel.x<0:
                                        self.image=self.walk_pos[1]
                                if self.vel.x>0:
                                        self.image=self.walk_pos[0]
                                self.image.set_colorkey(WHITE)
                                self.bottom=self.rect.bottom
                                self.rect=self.image.get_rect()
                                self.rect.bottom=self.bottom
                        
                        
                if not self.jumping and not self.walk:
                        if now-self.last_update>200:
                                self.last_update=now
                                self.frame=(self.frame+1)%2
                                self.image=self.stand_pos[self.frame]
                                self.image.set_colorkey(WHITE)
                                self.bottom=self.rect.bottom
                                self.rect=self.image.get_rect()
                                self.rect.bottom=self.bottom
                self.mask=pg.mask.from_surface(self.image)

class Platform(pg.sprite.Sprite):
        def __init__(self,game,x, y, w, h):
                self.groups=game.platforms
                pg.sprite.Sprite.__init__(self,self.groups)
                self.game=game
                self.image1 = pg.image.load("platform.png")
                self.image=pg.transform.scale(self.image1,(w,h))
                self.image.set_colorkey(WHITE)
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                if random.randrange(0,100)<5:
                        Powerup(self.game,self)
                
class Spritesheet:
        def __init__(self,filename):
                self.spriteimage=pg.image.load(filename).convert()
        def get_image(self,x,y,breadth,length):
                image=pg.Surface((breadth,length))
                image.blit(self.spriteimage,(0,0),(x,y,breadth,length))
                #image=pg.transform.scale(image,(breadth//2,length//2))
                return image
class Spritesheet2:
        def __init__(self,filename):
                self.spriteimage=pg.image.load(filename).convert()
        def get_image(self,x,y,breadth,length):
                image=pg.Surface((breadth,length))
                image.blit(self.spriteimage,(0,0),(x,y,breadth,length))
                #image=pg.transform.scale(image,(breadth//2,length//2))
                return image
class Powerup(pg.sprite.Sprite):
        def __init__(self,game,plat):
                self.groups=game.all_sprites,game.powe
                pg.sprite.Sprite.__init__(self,self.groups)
                self.game=game
                self.plat=plat
                self.image1 = pg.image.load("bolt.png")
                self.image=pg.transform.scale(self.image1,(40,40))
                self.rect = self.image.get_rect()
                self.rect.centerx = self.plat.rect.centerx
                self.rect.centery = self.plat.rect.centery-50
        def update(self):
                self.rect.centery=self.plat.rect.centery-50
                if not self.game.platforms.has(self.plat):
                        self.kill()

class Mob(pg.sprite.Sprite):
        def __init__(self,game):
                self.groups=game.all_sprites,game.mobs
                pg.sprite.Sprite.__init__(self,self.groups)
                self.game=game
                self.image_up=self.game.spritesheet2.get_image(0,0,64,50)
                self.image_down=self.game.spritesheet2.get_image(64,0,64,50)
                                                                
                self.image=self.image_up
                self.image.set_colorkey(BLACK)  
                self.rect=self.image.get_rect()
                self.radius=30
                self.rect.centerx=random.randrange(-300,WIDTH)
                self.speedx=3
                if self.rect.centerx>WIDTH:
                        self.speedx*=-3
                self.rect.centery=random.randrange(0,HEIGHT/2)
                self.speedy=0
                self.dy=0.5
                
        def update(self):
                self.rect.centerx+=self.speedx
                self.speedy+=self.dy
               
                self.rect.centery==self.speedy
                self.mask=pg.mask.from_surface(self.image)
                center=self.rect.center
                if self.speedy>0:
                        self.image=self.image_up
                if self.speedy<0:
                        self.image=self.image_down
                self.image.set_colorkey(WHITE)
                self.rect=self.image.get_rect()
                self.rect.center=center
                if self.speedy>3 or self.speedy<-3:
                        self.dy*=-1
                if self.rect.bottom>HEIGHT or self.rect.right<-100:
                        self.kill()



           
