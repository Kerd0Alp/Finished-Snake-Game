import pygame
import sys
import time
import random

# Initial difficulty settings
INITIAL_DIFFICULTY = 25
difficulty = INITIAL_DIFFICULTY

# Window size
frame_size_x = 720
frame_size_y = 480

# Checks for errors encountered
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initializing the game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialized')

# Initialize game window
pygame.display.set_caption('Snake game')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)
purple = pygame.Color(128, 0, 128)
cyan = pygame.Color(0, 255, 255)

# Snake color list
snake_colors = [green, yellow, blue, purple, cyan]
current_snake_color_index = 0

# FPS (frames per second) controller
fps_controller = pygame.time.Clock()

# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

# Food settings
food_size = 20  # Size of the food image
hitbox_size = 30  # Size of the food hitbox
food_limit = 5  # Maximum number of food items allowed on screen
food_positions = []

# Function to add food
def add_food():
    new_food_pos = [random.randrange(1, (frame_size_x // food_size)) * food_size,
                    random.randrange(1, (frame_size_y // food_size)) * food_size]
    if new_food_pos not in food_positions and new_food_pos not in snake_body:
        if len(food_positions) < food_limit:
            food_positions.append(new_food_pos)
        else:
            activate_portal(new_food_pos)

# Function to activate the portal
def activate_portal(portal_pos):
    # Hold snake for 2 seconds
    pygame.time.delay(2000)
    
for _ in range(food_limit):
    add_food()

direction = 'RIGHT'
change_to = direction

score = 0
start_time = pygame.time.get_ticks()  # Store the start time

# Background music
music_files = ["Terraria Music - Day.mp3", "back2.mp3", "back3.mp3", "back4.mp3"]
current_music_index = 0
pygame.mixer.init()

def play_next_music():
    global current_music_index
    pygame.mixer.music.load(music_files[current_music_index])
    pygame.mixer.music.play(-1)  # Play the music in a loop
    current_music_index = (current_music_index + 1) % len(music_files)

play_next_music()
last_music_change_time = pygame.time.get_ticks()  # Store the time when the music was last changed
music_change_interval = 20000  # 20 seconds interval in milliseconds

# Load backgrounds
background1 = pygame.image.load('background.jpg')
background2 = pygame.image.load('background2.png')
background3 = pygame.image.load('Background5.jpg')
background4 = pygame.image.load('Background4.jpg')
background1 = pygame.transform.scale(background1, (frame_size_x, frame_size_y))
background2 = pygame.transform.scale(background2, (frame_size_x, frame_size_y))
background3 = pygame.transform.scale(background3, (frame_size_x, frame_size_y))
background4 = pygame.transform.scale(background4, (frame_size_x, frame_size_y))

# Load food image
food_image = pygame.image.load('food.png')
food_image = pygame.transform.scale(food_image, (food_size, food_size))

# Load banana image
banana_image = pygame.image.load('spiral.png')
banana_image = pygame.transform.scale(banana_image, (food_size, food_size))

# Load portal image
portal_image = pygame.image.load('portal.png')
portal_image = pygame.transform.scale(portal_image, (food_size, food_size))

# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x / 2, frame_size_y / 4)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    show_time(white, 'times', 20, frame_size_y / 1.1)  # Show the time when the game ends
    show_message("Vajuta 'q' et väljuda või 'p' et uuesti proovida", white, 'times', 20, frame_size_y / 1.05)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    restart_game()
                    return
# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rect)

# Show time
def show_time(color, font, size, y_pos):
    current_time = pygame.time.get_ticks() - start_time  # Calculate the elapsed time
    seconds = current_time // 1000
    minutes = seconds // 60
    time_font = pygame.font.SysFont(font, size)
    time_surface = time_font.render('Time : {:02d}:{:02d}'.format(minutes, seconds % 60), True, color)
    time_rect = time_surface.get_rect()
    time_rect.midtop = (frame_size_x / 2, y_pos)
    game_window.blit(time_surface, time_rect)

# Show message
def show_message(message, color, font, size, y_pos):
    message_font = pygame.font.SysFont(font, size)
    message_surface = message_font.render(message, True, color)
    message_rect = message_surface.get_rect()
    message_rect.midtop = (frame_size_x / 2, y_pos)
    game_window.blit(message_surface, message_rect)

# Function to restart the game
def restart_game():
    global snake_pos, snake_body, direction, change_to, score, start_time, food_positions, current_snake_color_index, difficulty
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    change_to = direction
    score = 0
    start_time = pygame.time.get_ticks()
    food_positions = []
    for _ in range(food_limit):
        add_food()
    current_snake_color_index = 0
    difficulty = INITIAL_DIFFICULTY  # Reset the difficulty

# Main logic
background_index = 0
backgrounds = [background1, background2, background3, background4]
background_change_interval = 20000  # 20 seconds interval in milliseconds
last_background_change_time = pygame.time.get_ticks()  # Store the time when the background was last changed

color_change_interval = 10  # 10 seconds interval in milliseconds
last_color_change_time = pygame.time.get_ticks()  # Store the time when the snake color was last changed

# Speed increase settings
speed_increase_interval = 20000  # 30 seconds interval in milliseconds
last_speed_increase_time = pygame.time.get_ticks()  # Store the time when the speed was last increased

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                change_to = 'RIGHT'
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_pos[1] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'RIGHT':
        snake_pos[0] += 10

    snake_body.insert(0, list(snake_pos))
    for food_pos in food_positions:
        # Check for collision with enlarged hitbox
        if (snake_pos[0] in range(food_pos[0] - (hitbox_size - food_size) // 2, food_pos[0] + food_size + (hitbox_size - food_size) // 2) and 
            snake_pos[1] in range(food_pos[1] - (hitbox_size - food_size) // 2, food_pos[1] + food_size + (hitbox_size - food_size) // 2)):
            if food_pos == food_positions[-1]:  # If it's a banana
                score += 2
                add_food()  # Add a new food
            else:
                score += 1
                food_positions.remove(food_pos)
                add_food()  # Add a new food
            break
    else:
        snake_body.pop()

    # Toggle background based on time elapsed
    current_time = pygame.time.get_ticks()
    if current_time - last_background_change_time > background_change_interval:
        background_index = (background_index + 1) % len(backgrounds)
        last_background_change_time = current_time

    # Change snake color based on time elapsed
    if current_time - last_color_change_time > color_change_interval:
        current_snake_color_index = (current_snake_color_index + 1) % len(snake_colors)
        last_color_change_time = current_time

    # Increase speed every 30 seconds
    if current_time - last_speed_increase_time > speed_increase_interval:
        difficulty += 5  # Increase difficulty by reducing the delay
        last_speed_increase_time = current_time
        print("Speed increased!")

    # Check for snake collision with itself
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over()

    # Check for snake collision with walls
    if snake_pos[0] < 0 or snake_pos[0] >= frame_size_x or snake_pos[1] < 0 or snake_pos[1] >= frame_size_y:
        game_over()

    # Music change
    if current_time - last_music_change_time > music_change_interval:
        play_next_music()
        last_music_change_time = current_time

    # GFX
    game_window.blit(backgrounds[background_index], (0, 0))

    for pos in snake_body:
        pygame.draw.rect(game_window, snake_colors[current_snake_color_index], pygame.Rect(pos[0], pos[1], 10, 10))
       
    # Draw food
    for food_pos in food_positions:
        if food_pos == food_positions[-1]:  # If it's a banana
            game_window.blit(banana_image, (food_pos[0], food_pos[1]))
        else:
            game_window.blit(food_image, (food_pos[0], food_pos[1]))

    # Show score and time
    show_score(1, white, 'consolas', 20)
    show_time(white, 'consolas', 20, 15)  # Show the elapsed time

    pygame.display.update()
    fps_controller.tick(difficulty)
