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
gen = 0
WIN = pygame.display.set_mode( (WIN_WIDTH , WIN_HEIGHT)  )




""" Spacecraft class representing the spaceship """

class SpaceCraft :
    movex = 0
    movey = 0
    SpaceCraft_color = (0,0,255)
    radius = 20
    img_size = (83,40)

    """ loading and transforming Sprite for SpaceCraft"""

    img = pygame.image.load("redship4.png")
    img = pygame.transform.scale(img , (50,86)  )
    img = pygame.transform.rotate(img,270)

    bullets = []   # bullets array keep bullet objects fired by spaceCraft

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def move(self):
        self.x += self.movex
        #if self.y + self.movey >= 0 and self.y + self.movey < WIN_HEIGHT:
        self.y += self.movey

    """ function to move the ship upward
        return type : None
    """
    def moveup(self):
        if self.y >= 0:
            self.y -= 3
        #self.movey = - 10


    """ function to move the ship Down
        return type : None
     """
    def move_down(self):

        if self.y < WIN_HEIGHT:
            self.y += 3
        #self.movey = 10



    # def stop_up(self):
    #     self.movey = 0


    """ function for drwaing spaceCraft on window
        param  win : pygame surface
        return type : None
    """
    def draw(self,win):
        for bullet in self.bullets:
            bullet.draw(win)
        win.blit( self.img, (self.x,self.y) )
        #pygame.draw.circle(win,self.SpaceCraft_color,(self.x,self.y),self.radius)


    """ To get mask form sprite for collision detection
        return type : pygame.mask.Mask
     """
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

    """ function for drawing bullets
        param win : pygame.Surface/ pygame.window
        return type : None
    """
    def draw(self , win ):
        win.blit( self.img, (self.x,self.y+20) )
        #pygame.draw.rect(win,(0,255,0) , (self.x,self.y+20 , 10,5  ))

    """ function to move the bullets feed_forward
        return type : None
    """
    def move(self):
        self.x += self.VEL

    """ function to detect collision of bullet with
        remove enemy and bullet on collision
        param enemy : an object of enemy class
        param win : pygame.Surface/ pygame.window
        return type : bool , true if collision occcrs.
        """
    def collide(self, enemy , win):
        if enemy.Visible == True:
            bullet_mask = pygame.mask.from_surface(self.img)
            enemy_mask = enemy.get_mask()
            offset = (self.x - enemy.x, self.y + 20 - round(enemy.y))
            col = enemy_mask.overlap(bullet_mask, offset)
            if col:
                return True
        return False


    """ function to detect collision of bullet with obstacle
        remove enemy and bullet on collision
        param obstacle : an object of Obstacle class
        param win : pygame.Surface/ pygame.window
        return type : Bool , retuns true if collision occurs"""

    def collision_with_obstacle(self,obstacle):
        upper_obstacle = pygame.Rect(  ( obstacle.x , 0 , obstacle.PIPE_WIDTH, obstacle.height  ) )
        lower_obstacle = pygame.Rect( ( obstacle.x , obstacle.height + obstacle.GAP , obstacle.PIPE_WIDTH,WIN_HEIGHT - obstacle.height  ) )
        bullet_rect = self.img.get_rect()
        bullet_rect = pygame.Rect( (self.x , self.y , self.img.get_width(),self.img.get_height()) )


        u_col = bullet_rect.colliderect( upper_obstacle )
        l_col = bullet_rect.colliderect( lower_obstacle )

        if u_col or l_col :
            return True
        else:
            return False

''' class for representing a  Obstacle '''
class Obstacle:

    GAP = 200
    VEL = 3
    GAP_START = 100
    GAP_ENDS = 300
    PIPE_COLOR = (0,0,0)
    PIPE_WIDTH = 30



    def __init__(self,x):
        self.x = x
        self.height = round(self.set_random_height() )
        self.passed = False


    """function for selecting the height of obstacle set_y_randomly
        return type: float , a random value between GAP_START and GAP_ENDS
    """
    def set_random_height(self):
        return random.randrange(self.GAP_START,self.GAP_ENDS)

    """ function for drawing obstacles
        param win : pygame.Surface/ pygame.window
        return type : None
    """
    def draw(self,win):
        pygame.draw.rect(win, self.PIPE_COLOR , (self.x , 0 , self.PIPE_WIDTH,self.height  ) )
        pygame.draw.rect(win, self.PIPE_COLOR , (self.x , self.height+self.GAP , self.PIPE_WIDTH,WIN_HEIGHT - self.height  ) )


    ''' function to move the obstacle forward
        return type : None
      '''
    def move(self):
        self.x -= self.VEL


    """ function to detect collision of spaceCraft with obstacle
        end game on collision
        param spaceCraft : an object of spaceCraft class
        param win : pygame.Surface/ pygame.window
        return type : Bool , retuns true if collision occurs """
    def collide(self, spaceCraft, win):
        upper_obstacle = pygame.Rect(  ( self.x , 0 , self.PIPE_WIDTH, self.height  ) )
        lower_obstacle = pygame.Rect( ( self.x , self.height + self.GAP , self.PIPE_WIDTH,WIN_HEIGHT - self.height  ) )
        spaceCraft_rect = spaceCraft.img.get_rect()
        spaceCraft_rect = pygame.Rect( (spaceCraft.x , spaceCraft.y , spaceCraft.img.get_width(),spaceCraft.img.get_height()) )
        u_col = spaceCraft_rect.colliderect( upper_obstacle )
        l_col = spaceCraft_rect.colliderect( lower_obstacle )
        if u_col or l_col :
            return True
        else:
            return False


""" class representing enemies """

class Enemy:
    Visible = True
    VEL = 3
    COLOR = ( 255,0,0 )
    START_Y = 100
    END_Y = 400
    RADIUS = 30
    img_size = (80,80)
    img = pygame.image.load("base3n.png")
    img = pygame.transform.scale(img , img_size  )

    def __init__(self,x):
        self.x = x
        self.y = round(self.set_y_randomly() )


    """ function for selecting the height (y axis value) of enemy set_y_randomly
        return type : float , a randomly between START_Y and END_Y
    """
    def set_y_randomly(self):
        return random.randrange( self.START_Y , self.END_Y )


    """ function for drawing Enemies
        param win : pygame.Surface/ pygame.window
        return type : None
    """
    def draw(self,win):
        if self.Visible == True:
            win.blit( self.img, (self.x,self.y) )
            #pygame.draw.circle(win,self.COLOR,(int(self.x),int(self.y)),int(self.RADIUS)  )

    ''' function to move the enemy forward
        return type : None
      '''
    def move(self):
        self.x -= self.VEL

    """ function to detect collision of spaceCraft with enemy
        end game on collision
        param spaceCraft : an object of spaceCraft class
        param win : pygame.Surface/ pygame.window
        return type : Bool , retuns true if collision occurs """
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


    """ function to get bit mask of enemy Sprite
        return type : pygame.mask.Mask
     """
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


""" function to draw main window in the main game loop
    param win : pygame.Surface on  which all object will be drawn
    param spaceCraft: spaceCraft object
    param obstacles: list of obstacles to be drawn
    param enemies : list of enemies to be drawn
    param score : score to be rendered
    param gen : generation number to be rendered
    param member_no :  Genome number to be rendered
    return type : None
    """
def draw_window(win , spaceCraft,obstacles,enemies,score,gen, member_no):
    win.fill((255,255,255))

    for obstacle in obstacles:
        obstacle.draw(win)
    for enemy in enemies:
        enemy.draw(win)
    spaceCraft.draw(win)

    score_label = STAT_FONT.render("Score: " + str(score),1,STAT_COLOR )
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    score_label = STAT_FONT.render("Gens: " + str(gen-1),1,STAT_COLOR )
    win.blit(score_label, (10, 10))

    score_label = STAT_FONT.render("GENOME NUM: " + str(member_no),1,STAT_COLOR )
    win.blit(score_label, (10, 50))

    pygame.display.update()


"""  Main game loop
param nnet : neural network associated with a genome
param member_no : Genome number
return type : float , fitness of the current genome
"""
def main( nnet , member_no):

    TIC_COUNT = 0
    """ initialize the game clock """
    clock = pygame.time.Clock()

    """ gameon variable to determine wheather we should continue game or not """
    gameOn = True
    spaceCraft = SpaceCraft(300,300)

    ''' Initializing list of obstacle '''
    obstacles = [ Obstacle(WIN_WIDTH) , Obstacle(WIN_WIDTH+int(WIN_WIDTH/2)) ]

    score = 0
    fitness = 0

    ''' Initializing list of enemies '''
    enemies = [ Enemy( WIN_WIDTH - 100 ) , Enemy( round(WIN_WIDTH+WIN_WIDTH/2 - 100) )  ]


    ''' function to remove the first obstacle and adding a new obstacle at the end of screen
        parma obstacles : list of obstacles
        return : None
     '''
    def removeAndAddObstacles(obstacles):
        obstacles.pop(0)
        obstacles.append( Obstacle(WIN_WIDTH) )

    ''' function to remove the first obstacle and adding a new Enemies at the end of screen
        parma enemies : list of Enemies
        return : None
     '''
    def removeAndAddEnemies(enemies):
        enemies.pop(0)
        enemies.append( Enemy(WIN_WIDTH) )



    """ MAIN GAME LOOP """
    while gameOn :

        ''' screen refresh rate (frame rate) '''
        clock.tick(500)

        """ Quit game on close event """
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                gameOn = False
                pygame.quit()
                quit()
                break

        """ for selecting first obstacle and enemy in front of spacecraft """
        obstacle_index = 0
        enemy_index = 0
        if obstacles[0].x + obstacles[0].PIPE_WIDTH < spaceCraft.x:
            obstacle_index = 1
        if enemies[0].Visible == False:
            ememy_index = 1

        """ passing argument to neural network for computing results
            arg 1 : y position of spacecreft
            arg 2 : difference of heights between spaceCraft and lower end of upper obstacle
            arg3 : difference of heights between spacecraft and upper end of lower obstacle
            """
        nnoutput = nnet.activate( ( spaceCraft.y  , abs(spaceCraft.y - obstacles[obstacle_index].height  ) , abs( spaceCraft.y - obstacles[obstacle_index].height - obstacles[0].GAP ) , abs( spaceCraft.y - enemies[enemy_index].y )  )  )

        if nnoutput[0] > 0.5 :
            spaceCraft.moveup()
        if nnoutput[0] < 0.5 :
            spaceCraft.move_down()
        if nnoutput[1] > 0.5 :
            if TIC_COUNT > 10 :
                spaceCraft.bullets.append( Bullet(spaceCraft.x,spaceCraft.y ) )
                TIC_COUNT = 0
            else :
                TIC_COUNT += 1

        spaceCraft.move()
        if spaceCraft.y < 50:
            fitness -= 0.2
        if spaceCraft.y > WIN_HEIGHT - 50 :
            fitness -= 0.2

        ''' increase fitness for every frame spaceship is alive  '''
        fitness += 0.1


        for obstacle in obstacles:
            obstacle.move()
            if obstacle.x < spaceCraft.x and obstacle.passed == False:
                obstacle.passed = True
                score += 1
                fitness += 5  # add fitness if obstacle is passed
            """ on collision of spacecraft with obstacle end the game and return fitness  """
            if obstacle.collide(spaceCraft , WIN ):
                pygame.display.update()
                return fitness


        for enemy in enemies:
            enemy.move()
            """ on collision of spacecraft with enemy end the game and return fitness  """
            if enemy.collide( spaceCraft , WIN  ):
                pygame.display.update()
                return fitness


        for bullet in spaceCraft.bullets:
            bullet.move( )
            if bullet and bullet.x > WIN_WIDTH:
                spaceCraft.bullets.remove(bullet)  #Remove the bullet if it  goes past the screen

        for enemy in enemies:
            for bullet in spaceCraft.bullets :
                if bullet.collide( enemy , WIN  ):
                    enemy.Visible = False
                    score += 1
                    fitness += 3   # add fitness on eliminating a enemy """
                    if spaceCraft.bullets:
                        spaceCraft.bullets.remove(bullet)

        for obstacle in obstacles :
            for bullet in spaceCraft.bullets :
                if bullet.collision_with_obstacle(obstacle):
                    if spaceCraft.bullets:
                        spaceCraft.bullets.remove(bullet)


        """ remove obstacle if it goes past the screen  """
        if obstacles and obstacles[0].x < -30:
            removeAndAddObstacles ( obstacles )

        """ remove enemies if it goes past the screen  """
        if enemies and enemies[0].x < -30 :
            removeAndAddEnemies ( enemies )

        draw_window(WIN,spaceCraft,obstacles,enemies,score,gen, member_no )



""" function to evaluate fitness of genomes and selecting the best form them
param genomes : list of  genomes
param config : configuration file for implementing neat algo
"""
def eval_genomes(genomes , config ):
    global gen
    gen += 1
    i = 0
    best_fit = 0
    for genome_id, genome in genomes:
        i+=1
        genome.fitness = 0  # start with fitness level of 0

        """ get a neural network from current Genome  """
        nnet = neat.nn.FeedForwardNetwork.create(genome, config)

        """ Run  the game and get the fitness of current genome """
        current_fitness = main(nnet,i)
        #print(current_fitness)

        genome.fitness = current_fitness
        if current_fitness > best_fit:
            best_fit = current_fitness
        #print ( genome.fitness )
    print( 'beat fit ' + str(best_fit) )





def run(config_file):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run( eval_genomes , 50)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-file.txt')
    run(config_path)
