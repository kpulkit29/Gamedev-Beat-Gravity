import pygame as pg
import random
from window import *
from sprites import *
class Game:
        def __init__(self):
        # initialize game window, etc
            pg.init()
            pg.mixer.init()
            self.screen = pg.display.set_mode((WIDTH, HEIGHT))
            self.backgrd=pg.image.load("skyjump.png").convert()
            #self.backgrd_rect=pg.transform.scale(self.backgrd,(800,600))
            self.backimg=self.backgrd.get_rect()
            pg.display.set_caption(TITLE)
            self.clock = pg.time.Clock()
            self.running = True
            self.load()
        def load(self):
            with open("score.txt","r") as file:
                try:
                    self.highscore=int(file.read())
                except:
                    self.highscore=0
            self.spritesheet=Spritesheet("walk2.png")
            self.spritesheet2=Spritesheet2("snail.png")
            self.jumpsound=pg.mixer.Sound("marioj.wav")
            self.jet_sound=pg.mixer.Sound("jet.wav")
            self.jumpsound.set_volume(300)
            
        def new(self):
        # start a new game
            self.score = 0
            self.all_sprites = pg.sprite.Group()
            self.platforms = pg.sprite.Group()
            self.powe = pg.sprite.Group()
            self.mobs=pg.sprite.Group()
            self.mob_time=0
            self.player = Player(self)
            self.all_sprites.add(self.player)
            for plat in PLATFORM_LIST:
                 p=Platform(self,*plat)
                 self.all_sprites.add(p)
            
               
            self.run()
        def run(self):
        # Game Loop
            self.playing = True
            while self.playing:
                self.clock.tick(FPS)
                self.events()
                self.update()
                self.draw()
        def update(self):
        # Game Loop - Update
            self.all_sprites.update()
            # check if player hits a platform - only if falling
            if self.player.vel.y > 0:
                        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
                        if hits:
                                      for hit in hits:
                                              lowest=hit
                                              if hit.rect.bottom>lowest.rect.bottom:
                                                      lowest=hit.rect.bottom
                                      
                                      if self.player.pos.x<lowest.rect.right and self.player.pos.x>lowest.rect.left:
                                               self.player.pos.y = lowest.rect.top
                                               self.player.vel.y = 0
                                               self.player.jumping=False
            #spawing mobs
            now=pg.time.get_ticks()
            if now-self.mob_time>3000:
                    mob=Mob(self)
                    self.mob_time=now
            # if player reaches top 1/4 of screen
            if self.player.rect.top <= HEIGHT / 4:
              self.player.pos.y += max(abs(self.player.vel.y),2)
              for m in self.mobs:
                      m.rect.y+=max(abs(self.player.vel.y),2)
        
              for plat in self.platforms:
                   plat.rect.y +=  max(abs(self.player.vel.y),2)
                   if plat.rect.top >= HEIGHT:
                                  plat.kill()
                                  self.score += 10
            #hit the mob
            mob_hit=pg.sprite.spritecollide(self.player,self.mobs,False,pg.sprite.collide_circle)
            if mob_hit:
                    pg.time.wait(2000)
                    self.playing=False
                    
        
            # Die!
            if self.player.rect.bottom > HEIGHT:
                    for sprite in self.all_sprites:
                       sprite.rect.y -= max(self.player.vel.y, 10)
                       if sprite.rect.bottom < 0:
                            sprite.kill()
            #power_ups
            pow_hit=pg.sprite.spritecollide(self.player,self.powe,True)
            if pow_hit:
                    self.jet_sound.play()
                    self.player.vel.y=-JET_SPEED
                    self.jumping=False
            if len(self.platforms) == 0:
                self.playing = False
            # spawn new platforms to keep same average number
            while len(self.platforms) < 6:
                    width = random.randrange(50, 100)
                    p=Platform(self,random.randrange(0, WIDTH - width),
                    random.randrange(-75, -30),
                    width, 20)
                   
                    #self.platforms.add(p)
                    self.all_sprites.add(p)
        def events(self):
        # Game Loop - events
            for event in pg.event.get():
            # check for closing window
                if event.type == pg.QUIT:
                      if self.playing:
                           self.playing = False
                      self.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                            self.jumpsound.play()
                            self.player.jump()
                if event.type==pg.KEYUP:
                        self.player.jump_cut()

                        
        def draw(self):
        # Game Loop - draw
            self.screen.blit(self.backgrd,self.backimg)
            self.all_sprites.draw(self.screen)
            self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
        # *after* drawing everything, flip the display
            pg.display.flip()
        def show_start_screen(self):
        # game splash/start screen
            self.screen.fill(BGCOLOR)
            self.draw_text(TITLE, 60, WHITE, WIDTH / 2, HEIGHT / 4)
            self.draw_text("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
            self.draw_text("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
            self.draw_text("Best Score is:"+str(self.highscore),22,RED,WIDTH/2,HEIGHT/2+100)
            pg.display.flip()
            self.wait_for_key()
        def show_go_screen(self):
            # game over/continue
            if not self.running:
              return
            self.screen.fill(BGCOLOR)
           
            if self.highscore<self.score:
                self.highscore=self.score
                with open("score.txt","w") as f:
                    f.write(str(self.score))
            
               
            self.draw_text("You Lose...", 48, WHITE, WIDTH / 2, HEIGHT / 4)
            self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
            self.draw_text("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
            pg.display.flip()
            self.wait_for_key()
        def wait_for_key(self):
            waiting = True
            while waiting:
                self.clock.tick(FPS)
                for event in pg.event.get():
                   if event.type == pg.QUIT:
                         waiting = False
                         self.running = False
                   if event.type == pg.KEYUP:
                        waiting = False
        def draw_text(self, text, size, color, x, y):
                font = pg.font.SysFont("calibri", size)
                text_surface = font.render(text, True, color)
                text_rect = text_surface.get_rect()
                text_rect.midtop = (x, y)
                self.screen.blit(text_surface, text_rect)
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()
pg.quit()
