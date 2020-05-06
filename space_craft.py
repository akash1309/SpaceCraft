import pygame
import random
import time
import os
import neat

pygame.font.init()
WIN_WIDTH = 800
WIN_HEIGHT = 600
STAT_FONT = pygame.font.SysFont("comicsans", 50)
STAT_COLOR = (0,0,255)

WIN = pygame.display.set_mode( (WIN_WIDTH , WIN_HEIGHT)  )


class SpaceCraft :
    movex = 0
    movey = 0
    SpaceCraft_color = (0,0,255)
    radius = 20
    img_size = (83,40)
    img = pygame.image.load("redship4.png")
    img = pygame.transform.scale(img , (50,86)  )
    img = pygame.transform.rotate(img,270)
    bullets = []

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def move(self):
        self.x += self.movex
        self.y += self.movey

    def moveup(self):
        self.movey = - 10

    def move_down(self):
        self.movey = 10

    def stop_up(self):
        self.movey = 0


    def draw(self,win):
        for bullet in self.bullets:
            bullet.draw(win)
        win.blit( self.img, (self.x,self.y) )
        #pygame.draw.circle(win,self.SpaceCraft_color,(self.x,self.y),self.radius)


    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Bullet:
    VEL = 5
    img_size = (25,10)
    img = pygame.image.load("bullet.png")
    img = pygame.transform.scale(img , img_size  )
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def draw(self , win ):
        win.blit( self.img, (self.x,self.y+20) )
        #pygame.draw.rect(win,(0,255,0) , (self.x,self.y+20 , 10,5  ))

    def move(self):
        self.x += self.VEL

    def collide(self, enemy , win):
        if enemy.Visible == True:
            bullet_mask = pygame.mask.from_surface(self.img)
            enemy_mask = enemy.get_mask()
            offset = (self.x - enemy.x, self.y + 20 - round(enemy.y))
            col = enemy_mask.overlap(bullet_mask, offset)
            if col:
                return True
        return False

    def collision_with_pipe(self,pipe):
        upper_pipe = pygame.Rect(  ( pipe.x , 0 , pipe.PIPE_WIDTH, pipe.height  ) )
        lower_pipe = pygame.Rect( ( pipe.x , pipe.height + pipe.GAP , pipe.PIPE_WIDTH,WIN_HEIGHT - pipe.height  ) )
        bullet_rect = self.img.get_rect()
        bullet_rect = pygame.Rect( (self.x , self.y , self.img.get_width(),self.img.get_height()) )


        u_col = bullet_rect.colliderect( upper_pipe )
        l_col = bullet_rect.colliderect( lower_pipe )

        if u_col or l_col :
            return True
        else:
            return False


class Pipe:

    GAP = 200
    VEL = 5
    GAP_START = 100
    GAP_ENDS = 300
    PIPE_COLOR = (0,0,0)
    PIPE_WIDTH = 30



    def __init__(self,x):
        self.x = x
        self.height = round(self.set_random_height() )
        self.passed = False

    def set_random_height(self):
        return random.randrange(self.GAP_START,self.GAP_ENDS)

    def draw(self,win):
        pygame.draw.rect(win, self.PIPE_COLOR , (self.x , 0 , self.PIPE_WIDTH,self.height  ) )
        pygame.draw.rect(win, self.PIPE_COLOR , (self.x , self.height+self.GAP , self.PIPE_WIDTH,WIN_HEIGHT - self.height  ) )

    def move(self):
        self.x -= self.VEL

    def collide(self, spaceCraft, win):
        upper_pipe = pygame.Rect(  ( self.x , 0 , self.PIPE_WIDTH, self.height  ) )
        lower_pipe = pygame.Rect( ( self.x , self.height + self.GAP , self.PIPE_WIDTH,WIN_HEIGHT - self.height  ) )
        spaceCraft_rect = spaceCraft.img.get_rect()
        spaceCraft_rect = pygame.Rect( (spaceCraft.x , spaceCraft.y , spaceCraft.img.get_width(),spaceCraft.img.get_height()) )
        u_col = spaceCraft_rect.colliderect( upper_pipe )
        l_col = spaceCraft_rect.colliderect( lower_pipe )
        if u_col or l_col :
            return True
        else:
            return False



class Enemy:
    Visible = True
    VEL = 5
    COLOR = ( 255,0,0 )
    START_Y = 100
    END_Y = 400
    RADIUS = 30
    img_size = (80,80)
    img = pygame.image.load("base3n.png")
    img = pygame.transform.scale(img , img_size  )
    current_offset = 0
    change_offest = 2

    def __init__(self,x):
        self.x = x
        self.y = round(self.set_y_randomly() )

    def set_y_randomly(self):
        return random.randrange( self.START_Y , self.END_Y )

    def draw(self,win):
        if self.Visible == True:
            win.blit( self.img, (self.x,self.y+self.current_offset) )
            self.current_offset += self.change_offest
            if self.current_offset > 50:
                self.change_offest = -2
            elif self.current_offset < -50:
                self.change_offest = 2

            #pygame.draw.circle(win,self.COLOR,(int(self.x),int(self.y)),int(self.RADIUS)  )

    def move(self):
        self.x -= self.VEL


    def collide(self, spaceCraft, win):
        if self.Visible == True:
            spaceCraft_mask = spaceCraft.get_mask()
            enemy_mask = pygame.mask.from_surface(self.img)

            offset = (self.x - spaceCraft.x, self.y - round(spaceCraft.y))
            col = spaceCraft_mask.overlap(enemy_mask,offset)
            if col:
                return True
            return False
        return False

    def get_mask(self):
        return pygame.mask.from_surface(self.img)



def draw_window(win , spaceCraft,pipes,enemies,score):
    win.fill((255,255,255))

    for pipe in pipes:
        pipe.draw(win)
    for enemy in enemies:
        enemy.draw(win)
    spaceCraft.draw(win)
    score_label = STAT_FONT.render("Score: " + str(score),1,STAT_COLOR )
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))
    pygame.display.update()

def main( ):

    clock = pygame.time.Clock()
    gameOn = True
    spaceCraft = SpaceCraft(300,300)
    pipes = []
    pipes.append( Pipe(WIN_WIDTH))
    pipes.append( Pipe(WIN_WIDTH+WIN_WIDTH/2) )
    enemies = []
    score = 0

    # to do change to relate to win_width
    enemies.append( Enemy( WIN_WIDTH - 100 ) )
    enemies.append( Enemy( round(WIN_WIDTH+WIN_WIDTH/2 - 100) ) )



    def removeAndAddPipes(pipes):
        pipes.pop(0)
        pipes.append( Pipe(WIN_WIDTH) )

    def removeAndAddEnemies(enemies):
        enemies.pop(0)
        enemies.append( Enemy(WIN_WIDTH) )

    while gameOn :
        clock.tick(30)

        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                gameOn = False
                pygame.quit()
                quit()
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    spaceCraft.moveup()
                elif event.key == pygame.K_DOWN:
                    spaceCraft.move_down()
                elif event.key == pygame.K_SPACE:
                    spaceCraft.bullets.append( Bullet(spaceCraft.x,spaceCraft.y ) )

            elif event.type == pygame.KEYUP :
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    spaceCraft.stop_up()

        spaceCraft.move()
        for pipe in pipes:
            pipe.move()
            if pipe.x < spaceCraft.x and pipe.passed == False:
                pipe.passed = True
                score += 1


            if pipe.collide(spaceCraft , WIN ):
                time.sleep(5)
                gameOn = False
                pygame.display.update()


        for enemy in enemies:
            enemy.move()
            if enemy.collide( spaceCraft , WIN  ):
                time.sleep(5)
                gameOn = False
                pygame.display.update()


        for bullet in spaceCraft.bullets:
            bullet.move( )
            if bullet and bullet.x > WIN_WIDTH:
                spaceCraft.bullets.remove(bullet)

        for enemy in enemies:
            for bullet in spaceCraft.bullets :
                if bullet.collide( enemy , WIN  ):
                    enemy.Visible = False
                    score += 1
                    if spaceCraft.bullets:
                        spaceCraft.bullets.remove(bullet)

        for pipe in pipes :
            for bullet in spaceCraft.bullets :
                if bullet.collision_with_pipe(pipe):
                    if spaceCraft.bullets:
                        spaceCraft.bullets.remove(bullet)


        if pipes and pipes[0].x < -30:
            removeAndAddPipes ( pipes )

        if enemies and enemies[0].x < -30 :
            removeAndAddEnemies ( enemies )

        draw_window(WIN,spaceCraft,pipes,enemies,score)

main()
