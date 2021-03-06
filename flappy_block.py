import random
import pygame
pygame.init()

#colors found on w3schools
WHITE = (255,255,255)
BLACK = (238,253,1)
PIPE = (102,255,102)
SKY = (102,31,173)
GROUND = (204,255,255)
DARK_GROUND = (124,115,46)
BIRD = (245,61,153)

size = (800,700)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Flappy Block")

done = False

clock = pygame.time.Clock()

arial18 = pygame.font.SysFont('arial',18, False, False)
arial30 = pygame.font.SysFont('arial',30, False, False)

gameState = 1

pipes = []

score = 0
highScore = 0

class Bird():
    def __init__(self):
        self.x = 250
        self.y = 250
        self.yV = 0
    
    def flap(self):
        self.yV = -10
    
    def update(self):
        self.yV += 0.5
        self.y += self.yV
        if self.y >= 608:
            self.y = 608
            self.yV = 0
        if self.yV > 20:
            self.yV = 20
    
    def draw(self):
        pygame.draw.rect(screen,BIRD,(self.x,self.y,40,40))
    
    def reset(self):
        self.x = 250
        self.y = 250
        self.yV = 0

bird = Bird()

class Pipe():
    def __init__(self):
        self.centerY = random.randrange(130,520)
        self.x = 800
        self.size = 100
    
    def update(self):
        global pipes
        global bird
        global gameState
        global score
        self.x -= 4
        if self.x == 300:
            pipes.append(Pipe())
        if self.x <= -100:
            del pipes[0]
        if self.x >= 170 and self.x <= 290 and bird.y <= (self.centerY - self.size) or self.x >= 170 and self.x <= 290 and (bird.y + 40) >= (self.centerY + self.size):
            gameState = 3
        if self.x == 168 and bird.y > (self.centerY - 100) and bird.y < (self.centerY + 100):
            score += 1
        if bird.y >= 608:
            gameState = 3
    
    def draw(self):
        pygame.draw.rect(screen,PIPE,(self.x,0,80,(self.centerY - self.size)))
        pygame.draw.rect(screen,PIPE,(self.x,(self.centerY + self.size),80,(548 - self.centerY)))

pipes.append(Pipe())

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if gameState == 1:
                    gameState = 2
                elif gameState == 3:
                    bird.reset()
                    pipes = []
                    pipes.append(Pipe())
                    gameState = 2
                    score = 0
                else:
                    bird.flap()
    
    screen.fill(SKY)
    pygame.draw.rect(screen,GROUND,(0,650,800,50))
    pygame.draw.line(screen,DARK_GROUND,(0,650),(800,650),5)
    pygame.draw.line(screen,DARK_GROUND,(0,650),(800,650),5)
    
    if gameState == 1:
        pygame.draw.rect(screen,GROUND,(300,300,200,100))
        pygame.draw.rect(screen,DARK_GROUND,(300,300,200,100),5)
        text = arial18.render("Press space to play",True,DARK_GROUND)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text,((400 - (textX / 2)),(350 - (textY / 2))))
    
    if gameState == 2:
        bird.update()
        bird.draw()
        
        for pipe in pipes:
            pipe.update()
            pipe.draw()
        
        if score > highScore:
            highScore = score
        
        text = arial30.render(str(score),True,WHITE)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text,((400 - (textX / 2)),(50 - (textY / 2))))
    
    if gameState == 3:
        for pipe in pipes:
            pipe.draw()
        bird.draw()
        
        pygame.draw.rect(screen,GROUND,(300,250,200,200))
        pygame.draw.rect(screen,DARK_GROUND,(300,250,200,200),5)
        text = arial18.render(("Score: " + str(score)),True,DARK_GROUND)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text,((400 - (textX / 2)),(300 - (textY / 2))))
        text = arial18.render(("High Score: " + str(highScore)),True,DARK_GROUND)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text,((400 - (textX / 2)),(350 - (textY / 2))))
        text = arial18.render("Press space to play",True,DARK_GROUND)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text,((400 - (textX / 2)),(400 - (textY / 2))))
        text = arial30.render(str(score),True,WHITE)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text,((400 - (textX / 2)),(50 - (textY / 2))))
    
    pygame.display.flip()
    
    clock.tick(60)

pygame.quit()
