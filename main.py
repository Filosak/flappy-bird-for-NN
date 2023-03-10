import pygame
import random
from bird import Bird, Walls
pygame.init()
pygame.font.init()

# window
screen = pygame.display.set_mode((700, 1000))
screen.fill((255,255,255))


# variables
run = True
score = 0
font = pygame.font.Font("project/font.TTF", 60)
bg = pygame.image.load("project/hope2.png")
bird_photo = pygame.image.load("project/magor3.png")
bird = Bird()
walls = [Walls(700, 1000), Walls(700, 1000 + 600), Walls(700, 1000 + 1200)]

auto_move = pygame.USEREVENT + 1
pygame.time.set_timer(auto_move, 1000 // 60)



# functions
def draw(bird_pos, new_walls_pos):
    bird_circle = pygame.draw.circle(screen, (0,0,0), bird_pos, 30)

    screen.fill((255,255,255))
    # screen.blit(bg, (0, 0))
    
    rectangles = create_rectangles(new_walls_pos)
    for rect in rectangles:
        pygame.draw.rect(screen, (0,255,0), rect)
    
    screen.blit(font.render(str(score), False, (0, 0, 0)), (350,50))

    rotated_image = pygame.transform.rotate(bird_photo, min(max((bird.velocity * -80), -70), 40))
    screen.blit(rotated_image, bird_circle) 

    return rectangles, bird_circle


def move_objects():
    global score

    for wall in walls:
        flag = wall.move(1000, 700)

        if flag == True:
            score += 1

    bird.new_bird_pos()


def create_rectangles(new_walls_pos):
    rectangles = []

    for pos in new_walls_pos:
        up_rect = pygame.Rect(pos.up_pos[0], pos.up_pos[1], pos.up_pos[2], pos.up_pos[3])
        down_rect = pygame.Rect(pos.down_pos[0], pos.down_pos[1], pos.down_pos[2], pos.down_pos[3])

        rectangles.append(up_rect)
        rectangles.append(down_rect)

    return rectangles



while run:

    for event in pygame.event.get():
        if event.type == auto_move:
            bird.velocity = round(min(1.5, bird.velocity + 0.06), 2)

            move_objects()
            rectangles, bird_circle= draw(bird.possition, walls)

            for rect in rectangles:
                if rect.colliderect(bird_circle):
                    run = False

            if bird.possition[1] > 1030 or bird.possition[1] < 30:
                run = False
                
        

        if event.type == pygame.MOUSEBUTTONDOWN:
            bird.velocity = -1


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        
        pygame.display.update()

pygame.quit()