
import pygame, sys, random

class ballClass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("ball.png")
        self.rect = self.image.get_rect()
        self.rect.center = [320, 100]
        self.angle = 0
        
    def turn(self, direction): 
        self.angle = self.angle + direction
        if self.angle < -2:  self.angle = -2
        if self.angle >  2:  self.angle =  2 
        center = self.rect.center
        self.image = pygame.image.load("ball.png")
        self.rect = self.image.get_rect()
        self.rect.center = center
        speed = [self.angle, 6 - abs(self.angle) * 2]
        return speed
    
    def move(self, speed):
        # move the skier right and left
        self.rect.centerx = self.rect.centerx + speed[0]
        if self.rect.centerx < 20:  self.rect.centerx = 20
        if self.rect.centerx > 620: self.rect.centerx = 620 
        
class ObstacleClass(pygame.sprite.Sprite):
    def __init__(self, image_file, location, type):
        pygame.sprite.Sprite.__init__(self) 
        self.image_file = image_file        
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.type = type
        self.passed = False
                   
    def update(self):
        global speed
        self.rect.centery -= speed[1]
        if self.rect.centery < -32:
            self.kill()


def create_map():
    global obstacles
    locations=[]
    for i in range(10):            
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        location  = [col * 64 + 32, row * 64 + 32 + 640]
        if not (location in locations):       
            locations.append(location)          
            type = random.choice(["rock", "flag"])
            if type == "rock": 
                img = "rock.png"
            elif type == "flag":
                img = "flag.png"
            obstacle = ObstacleClass(img, location, type)
            obstacles.add(obstacle)

def animate():
    screen.fill([125, 0, 255])
    obstacles.draw(screen)
    screen.blit(ball.image,ball.rect)
    screen.blit(score_text, [10, 10])
    screen.blit(lifes,[10,50])
    pygame.display.flip()    

pygame.init()
screen = pygame.display.set_mode([640,640])
clock = pygame.time.Clock()
speed = [0, 6]
obstacles = pygame.sprite.Group()   
ball = ballClass()
map_position = 0
points = 0
create_map()      
font = pygame.font.Font(None, 50)

life=3
running = True
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if life==0:
            running=False
        if event.type == pygame.KEYDOWN:        
            if event.key == pygame.K_LEFT:        
                speed = ball.turn(-1)
            elif event.key == pygame.K_RIGHT:     
                speed = ball.turn(1)
    ball.move(speed)                         
    map_position += speed[1]                     
    
    if map_position >= 640:
        create_map()
        map_position = 0
    hit =  pygame.sprite.spritecollide(ball, obstacles, False)
    if hit:
        if hit[0].type == "rock" and not hit[0].passed: 
            life=life-1
            ball.image = pygame.image.load("ball.png")  
            pygame.time.delay(100)
            ball.image = pygame.image.load("ball.png") 
            ball.angle = 0
            speed = [0, 6]
            hit[0].passed = True
        elif hit[0].type == "flag" and not hit[0].passed:   
            points += 20
            hit[0].kill()                                 
    
    obstacles.update()
    score_text = font.render("Score: " +str(points), 1, (0, 0, 0))
    lifes = font.render("Life: " +str(life), 1, (0, 0, 0))
    animate()   
pygame.quit()




