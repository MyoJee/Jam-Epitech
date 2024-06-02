import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Initialize the mixer for sound
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load('musique.mp3')
pygame.mixer.music.play(-1)  # -1 means the music will loop indefinitely

# Load sound effect for touching an object
touch_sound = pygame.mixer.Sound('touch.mp3')

# Define the dimensions of the game window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Le temps presse pour Beemp")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# Load player sprites
player_images = {
    'default': pygame.transform.scale(pygame.image.load('bmo.png'), (50, 70)),
    'closed_eyes': pygame.transform.scale(pygame.image.load('bmo_closed_eyes.png'), (50, 70)),
    'dollar_eyes': pygame.transform.scale(pygame.image.load('bmo_dollar_eyes.png'), (50, 70))
}
player_image = player_images['default']  # Start with the default image

# Load the item image
item_image = pygame.transform.scale(pygame.image.load('item.png'), (30, 50))
enemy_image = pygame.transform.scale(pygame.image.load('mob.png'), (40, 50))

# Load the background image
background_image = pygame.transform.scale(pygame.image.load('background.jpg'), (width, height))

# Define the clock
clock = pygame.time.Clock()
font = pygame.font.Font(None, 74)

# Game variables
player_pos = [width // 2, height // 2]
player_speed = 5
player_health = 100
time_left = 60  # 60 seconds to finish the level
start_ticks = pygame.time.get_ticks()  # to count elapsed time

# Animation variables
animation_timer = pygame.time.get_ticks()
animation_state = 'default'
dollar_eyes_duration = 1000  # Duration of dollar eyes in milliseconds
dollar_eyes_start = None

# Level variables
current_level = 1
max_level = 3
initial_enemy_count = 15
additional_enemies_per_level = 5

# Create collectible items
num_items = 5
items = []
item_velocities = []
for i in range(num_items):
    items.append(pygame.Rect(random.randint(50, width - 50), random.randint(50, height - 50), 30, 30))
    item_velocities.append([random.choice([-1, 1]), random.choice([-1, 1])])

# Create enemies
def create_enemies(num_enemies):
    enemies = []
    enemy_velocities = []
    for i in range(num_enemies):
        enemies.append(pygame.Rect(random.randint(50, width - 50), random.randint(50, height - 50), 30, 30))
        enemy_velocities.append([random.choice([-1, 1]), random.choice([-1, 1])])
    return enemies, enemy_velocities

num_enemies = initial_enemy_count
enemies, enemy_velocities = create_enemies(num_enemies)

# Define the time machine
time_machine = pygame.Rect(random.randint(50, width - 50), random.randint(50, height - 50), 60, 60)

def change_player_image(new_image_key):
    global player_image
    player_image = player_images[new_image_key]

# Function to reset the level
def reset_level():
    global player_pos, player_health, time_left, start_ticks, items, item_velocities, enemies, enemy_velocities, time_machine
    player_pos = [width // 2, height // 2]
    player_health = 100
    time_left = 60
    start_ticks = pygame.time.get_ticks()

    # Reset items
    items = []
    item_velocities = []
    for i in range(num_items):
        items.append(pygame.Rect(random.randint(50, width - 50), random.randint(50, height - 50), 30, 30))
        item_velocities.append([random.choice([-1, 1]), random.choice([-1, 1])])

    # Reset enemies
    enemies, enemy_velocities = create_enemies(num_enemies)

    # Reset time machine
    time_machine = pygame.Rect(random.randint(50, width - 50), random.randint(50, height - 50), 60, 60)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    # Check screen boundaries for the player
    if player_pos[0] < 0:
        player_pos[0] = width
    if player_pos[0] > width:
        player_pos[0] = 0
    if player_pos[1] < 0:
        player_pos[1] = height
    if player_pos[1] > height:
        player_pos[1] = 0

    # Create the player rectangle
    player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 50)
                        
    # Update item positions
    for i, item in enumerate(items):
        item.x += item_velocities[i][0]
        item.y += item_velocities[i][1]

        # Check screen boundaries for items
        if item.left <= 0 or item.right >= width:
            item_velocities[i][0] = -item_velocities[i][0]
        if item.top <= 0 or item.bottom >= height:
            item_velocities[i][1] = -item_velocities[i][1]

    # Update enemy positions
    for i, enemy in enumerate(enemies):
        enemy.x += enemy_velocities[i][0]
        enemy.y += enemy_velocities[i][1]

        # Check screen boundaries for enemies
        if enemy.left <= 0 or enemy.right >= width:
            enemy_velocities[i][0] = -enemy_velocities[i][0]
        if enemy.top <= 0 or enemy.bottom >= height:
            enemy_velocities[i][1] = -enemy_velocities[i][1]

    # Check collisions with items
    new_items = []
    new_item_velocities = []
    for i, item in enumerate(items):
        if player_rect.colliderect(item):
            player_health = min(player_health + 10, 100)  # Increase player health
            touch_sound.play()  # Play the touch sound effect
            change_player_image('dollar_eyes')  # Change BMO's image when touching a blue square
            dollar_eyes_start = pygame.time.get_ticks()
        else:
            new_items.append(item)
            new_item_velocities.append(item_velocities[i])
    items = new_items
    item_velocities = new_item_velocities

    # Check collisions with enemies
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            player_health -= 25  # Reduce player health
            enemies.remove(enemy)  # Remove the enemy from the list

        # If player health reaches zero or less, display a losing message
        if player_health <= 0:
            print("T'as perdu, retry ?")
            running = False

    # Check if all items are collected and if the player reaches the time machine
    if not items and player_rect.colliderect(time_machine):
        if current_level < max_level:
            current_level += 1
            num_enemies += additional_enemies_per_level
            reset_level()
        else:
            print("Mazel tov, tu as gagné")
            running = False

    # Calculate the remaining time
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    time_left = 60 - int(seconds)

    # End the game if time is up
    if time_left <= 0:
        print("Tu n'as plus de temps! Beemo est mort...")
        running = False

    # Handle BMO animation
    current_time = pygame.time.get_ticks()

    # Return to default state after a collision with a delay
    if dollar_eyes_start and current_time - dollar_eyes_start > dollar_eyes_duration:
        dollar_eyes_start = None  # Reset the delay
        animation_timer = current_time  # Reset the animation timer to continue alternating

    if not dollar_eyes_start:
        if current_time - animation_timer > 1000:  # Change image every second
            animation_timer = current_time
            if animation_state == 'default':
                animation_state = 'closed_eyes'
            else:
                animation_state = 'default'
            change_player_image(animation_state)
    else:
        change_player_image('dollar_eyes')

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw items
    for item in items:
        screen.blit(item_image, item)

    # Draw enemies
    for enemy in enemies:
        screen.blit(enemy_image, enemy)

    # Draw the time machine
    pygame.draw.rect(screen, red, time_machine)

    # Draw the player
    screen.blit(player_image, (player_pos[0], player_pos[1]))

    # Display the remaining time
    timer_text = font.render(str(time_left), True, red)
    screen.blit(timer_text, (10, 10))

    # Display the player's health
    health_text = font.render(str(player_health), True, green)
    screen.blit(health_text, (width - 100, 10))

    # Display the current level
    level_text = font.render("Level " + str(current_level), True, white)
    screen.blit(level_text, (width // 2 - 100, 10))

    # Update the display
    pygame.display.flip()

    # Set the game loop speed
    clock.tick(60)

pygame.quit()
sys.exit()
