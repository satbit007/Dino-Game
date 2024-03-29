import pygame
import os
import random

pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load assets
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]
SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]
BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]
CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))
SUN = pygame.image.load(os.path.join("Assets/Other", "Sun.jpeg"))

# Initial game state variables
game_speed = 20
x_pos_bg = 0
y_pos_bg = 380
points = 0
high_score = 0
obstacles = []
is_paused = False
level = 1

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1

def draw_pause_button():
    font = pygame.font.Font('freesansbold.ttf', 20)
    pause_btn_color = (0, 0, 0)
    pause_btn_rect = pygame.Rect(10, 10, 100, 50)
    pygame.draw.rect(SCREEN, pause_btn_color, pause_btn_rect)
    pause_text_color = (255, 255, 255)
    pause_text = font.render('Pause' if not is_paused else 'Play', True, pause_text_color)
    pause_text_rect = pause_text.get_rect(center=pause_btn_rect.center)
    SCREEN.blit(pause_text, pause_text_rect)
    return pause_btn_rect

def update_level():
    global level, points, game_speed
    if points > 250 * level and level < 5:  # Example condition for leveling up
        level += 1
        game_speed += 5

def add_obstacle():
    if level == 1:
        obstacles.append(SmallCactus(SMALL_CACTUS))
    elif level == 2:
        if random.randint(0, 1):
            obstacles.append(SmallCactus(SMALL_CACTUS))
        else:
            obstacles.append(LargeCactus(LARGE_CACTUS))
    elif level >= 3:
        obstacle_choice = random.choice([SmallCactus(SMALL_CACTUS), LargeCactus(LARGE_CACTUS), Bird(BIRD)])
        obstacles.append(obstacle_choice)

def main(death_count):
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, is_paused, high_score, level
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    font = pygame.font.Font('freesansbold.ttf', 20)

    while run:
        update_level()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                pause_btn_rect = draw_pause_button()
                if pause_btn_rect.collidepoint(mouse_pos):
                    is_paused = not is_paused

        SCREEN.fill((255, 255, 255))

        # Draw the background
        background = BG
        SCREEN.blit(background, (x_pos_bg, y_pos_bg))

        if not is_paused:
            userInput = pygame.key.get_pressed()
            player.update(userInput)
            cloud.update()

            if len(obstacles) == 0 or random.randint(0, 250 // level) == 0:
                add_obstacle()

            for obstacle in obstacles:
                obstacle.update()
                if player.dino_rect.colliderect(obstacle.rect):
                    run = False
                    break

            points += 1

        player.draw(SCREEN)
        cloud.draw(SCREEN)
        for obstacle in obstacles:
            obstacle.draw(SCREEN)

        # Draw the score on the screen outside of the pause condition
        score_text = font.render(f"Score: {points}", True, (0, 0, 0))
        SCREEN.blit(score_text, (70, 70))

        draw_pause_button()
        pygame.display.update()
        clock.tick(30)

    if not run:
        menu(death_count + 1)

def menu(death_count):
    global points, game_speed, obstacles, is_paused, high_score, level
    font = pygame.font.Font('freesansbold.ttf', 30)
    run = True

    while run:
        SCREEN.fill((255, 255, 255))

        if points > high_score:
            high_score = points

        text = font.render("Press any Key to Restart", True, (0, 0, 0))
        score_text = font.render("Your Score: " + str(points), True, (0, 0, 0))
        high_score_text = font.render("High Score: " + str(high_score), True, (0, 0, 0))
        scoreRect = score_text.get_rect()
        highScoreRect = high_score_text.get_rect()
        textRect = text.get_rect()
        scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
        highScoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(score_text, scoreRect)
        SCREEN.blit(high_score_text, highScoreRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                points = 0
                game_speed = 20
                level = 1
                obstacles = []
                is_paused = False
                run = False

    main(death_count)

menu(death_count=0)
