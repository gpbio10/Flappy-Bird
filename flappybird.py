"""
This is a recreation of Flappy Bird using the Pygame module.
To run this game, pygame must be installed along with Python 3.7.X.
Additionally, all images must be downloaded.
"""


import pygame
import math
import random

#Initialize the Pygame module.
pygame.init()
pygame.display.init()
screen_width = 500
screen_height = 600

#Set display size and caption.
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird by GPBIO')

#Render font type.
myFont = pygame.font.SysFont("Times New Roman", 100)
score_font = pygame.font.SysFont("Times New Roman", 40)

#Render images.
bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (55 ,40))
background = pygame.image.load("background copy.png")
floor_img = pygame.image.load("groun.png")
floor_img = pygame.transform.scale(floor_img, (500, 100))
pipe_img = pygame.image.load("pipe.png")
pipe_img_upsidedown = pygame.transform.rotate(pipe_img, 180)
score_board_img = pygame.image.load('scoreboard.png')
score_board_img = pygame.transform.scale(score_board_img, (300, 300))


#Fill screen with background and ground.
def fill_background():
    screen.blit(background, (0, -250))


def fill_floor():
    screen.blit(floor_img, (0, 540))


#Bird class which includes functions for determining position and hitbox positions.
class bird():
    #Set starting position, angle and velocities.
    def __init__(self, position_x=180, position_y=280, dirny=0, angle=0):
        self.position_x = position_x
        self.position_y = position_y
        self.dirny = dirny
        self.angle = 10
        self.jump_time = 0

    #All the dynamics for the bird including gravity and button presses.
    def move(self):
        #Initialize buttons used for closing application.
        global start_game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            #Uses space bar press to change velocity in y direction and also resets angle.
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_SPACE]:
                    self.dirny = - 500
                    self.angle = 10
                    #Resets clock to be used for acceleration calculation and change in angle.
                    self.jump_time = pygame.time.get_ticks()
                    start_game = True

        #Checks clock to determine flight time since last flap.
        self.current_time = pygame.time.get_ticks()
        self.flight_time = (self.current_time - self.jump_time)
        #Max y veloccity and angle.
        max = 750
        if self.dirny <= max:
            self.dirny += (self.flight_time ** 1.8) / 1000
        else:
            self.dirny += 0
        self.position_y += self.dirny * 0.02
        self.angle -= self.dirny / 200

        #Checks collision for the ground and the bird.
        ground = 520
        if self.position_y >= ground:
            self.position_y = ground
            self.angle = -90
            running = False

    #Hitbox coordinates based of bird position.
    def bird_hitbox(self):
        bird_width = 20
        self.hitbox_list = [self.position_x, self.position_y, bird_width, bird_width]

    #Draw function for the bird image based on x and y coordinates.
    def draw(self):
        bird_img_rotated = pygame.transform.rotate(bird_img, self.angle)
        #Line below can be uncommented to draw hitbox behind the bird.
        #pygame.draw.rect(screen, (255, 255, 255), (self.hitbox_list[0] + 5, self.hitbox_list[1] + 5, 30, 30))
        screen.blit(bird_img_rotated, (self.position_x, self.position_y))

#Class for storing and drawing pipes.
class building():
    def __init__(self):
        self.spawn_time = 0
        self.y_height = []
        self.x_height = []
        self.score = -2

    #Spawns a randomly generated set of pipes every 2.5 seconds into an list.
    def spawn_coordinates(self):
        current_time = pygame.time.get_ticks()
        time_since_spawn = (current_time - self.spawn_time) / 1000
        if time_since_spawn >= 2.5:
            self.y_height.append(random.randrange(200, 500))
            self.x_height.append(500)
            #Resets clock after new set of pipes is spawned.
            self.spawn_time = current_time
            self.score += 1

        #The velocity of the pipes moving in the negative x direction in pixels.
        for i in range(len(self.y_height)):
            self.x_height[i] -= 8

    #Determines the hitboxes for the pipes given the position of the pipes.
    def pipe_hitbox(self):
        for i in range(len(self.y_height)):
            self.pipe_hitbox_x = self.x_height[i]
            self.pipe_hitbox_y = self.y_height[i]
            #Pipe hitboxes can be draw if the two following lines are uncommented.
            #pygame.draw.rect(screen, (255, 255, 255), (self.x_height[i] + 175, self.y_height[i], 70, 500))
            #pygame.draw.rect(screen, (255, 255, 255), (self.x_height[i] + 175, self.y_height[i] - 630, 70, 500))

    #Draws the set of pipes
    def draw_building(self):
        for i in range(len(self.y_height)):
            screen.blit(pipe_img, (self.x_height[i], self.y_height[i]))
            screen.blit(pipe_img_upsidedown, (self.x_height[i], self.y_height[i] - 550))

#Function used to compared bird hitboxes with pipe hitboxes to determine if there is a collision.
#Collision is initially set to false.
collision = False
def collision_test(hitbox_list, pipe_hitbox_x, pipe_hitbox_y):
    global collision
    #Sets the coordinates of pipes and birds for all the pipes in the list.
    for i in range(len(pipe_hitbox_x)):
        rect_1_x = hitbox_list[0] + 5
        rect_1_y = hitbox_list[1] + 10
        rect_1_width = 20
        rect_1_height = 20
        rect_2_x = pipe_hitbox_x[i] + 220
        rect_2_y = pipe_hitbox_y[i]
        rect_2_width = 70
        rect_2_height = 500

        #Checks if the there is a collision between the bird and the bottum pipe by checking if the coordinates fall inbetween eachother.
        if rect_1_x < rect_2_x + rect_1_width and rect_1_x + rect_2_width > rect_2_x and rect_1_y < rect_2_y + rect_1_height and rect_1_height + rect_1_y > rect_2_y:
            collision = True

        #Check collsions betwenen pipe and top pipe.
        rect_2_y_upsidedown = pipe_hitbox_y[i] - 550
        if rect_1_x < rect_2_x + rect_1_width and rect_1_x + rect_2_width > rect_2_x and rect_1_y < rect_2_y_upsidedown + 400 + rect_1_height and rect_1_height + rect_1_y > rect_2_y_upsidedown:
            collision = True

#Main function
def main():
    global running
    #Initalizes bird and building classes.
    b = bird()
    o = building()
    #Initialzes clock
    clock = pygame.time.Clock()
    #Initilizes positions list and sets score to zero.
    start_time = []
    time_change = 0
    my_score_txt = []
    #Main while loop that will be terminated when there is a collsion.
    running = True
    while running:
        #Sets framerate to 100.
        clock.tick(100)
        fill_background()
        #Calls bird functions to determine movement and draws bird on canvas.
        b.move()
        b.bird_hitbox()
        b.draw()

        #Prints instruction text on canvas.
        if start_game == False:
            b.position_y = 280
            b.angle = 10
            instruction = "Press SPACE to start!"
            instructions_txt = score_font.render(instruction, 1, (255, 255, 255))
            screen.blit(instructions_txt, (110, 200))

        #Calls pipe functions to determine positions and draws on canvas.
        o.spawn_coordinates()
        o.pipe_hitbox()
        o.draw_building()
        fill_floor()
        collision_test(b.hitbox_list, o.x_height, o.y_height)

        #Runs if collision is set to True.
        if collision:
            fill_background()
            o.draw_building()
            fill_floor()
            #Draws score board and score
            screen.blit(score_board_img, (100, 100))
            my_score_txt.append(o.score)
            score_txt = score_font.render(str(my_score_txt[0]), 1, (235, 175, 85))
            best_score_txt = score_font.render(str(my_score_txt[0]), 1, (235, 175, 85))
            screen.blit(score_txt, (338, 227))
            screen.blit(best_score_txt, (338, 280))
            instructions_txt = score_font.render("Respawning in 3 seconds...", 1, (0,0,0))
            screen.blit(instructions_txt, (75, 400))

            #Records time to wait a 5 second delay.
            start = pygame.time.get_ticks()
            start_time.append(start)
            time_change = current_time - start_time[0]

        #Resets game after 5 seconds.
        current_time = pygame.time.get_ticks()
        if time_change >= 5000:
            running = False

        #Adjust score to counteract initial position.
        if o.score == -1:
            my_score = myFont.render(str(o.score + 1), 1, (255, 255, 255))
        else:
            my_score = myFont.render(str(o.score), 1, (255,255,255))

        if collision is not True:
            screen.blit(my_score, (225, 50))

        #Update display to draw everything.
        pygame.display.update()

#Runs main function and restarts after a collision and 5 second delay.
clock = pygame.time.Clock()
on = True
while on:
    start_game = False
    collision = False
    main()
    if running == False:
        screen.blit(score_board_img, (100, 100))
    pygame.display.update()



