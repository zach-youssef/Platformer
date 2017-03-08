import pygame
import ctypes
import player,background,source

# Resource Directories
img_dir = 'resources/png/'

# Initialize pygame components
pygame.init()

# Obtain Screen Size
user32 = ctypes.windll.user32
resolution = (display_width , display_height) = (user32.GetSystemMetrics(0),user32.GetSystemMetrics(1))
# Create display surface
display = pygame.display.set_mode(resolution,pygame.FULLSCREEN)
# Set window title
pygame.display.set_caption('PyPlatformer')
# Create Clock
clock = pygame.time.Clock()


# Determines whether or not Zach is on a surface.
def on_platform(x,y):
    # TODO
    if y >= display_height:
        return True
    else:
        return False

# Sprite Creation
players = pygame.sprite.Group()
backgrounds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


player = player.Player(source.player('zach_proto.png'), display_height)
background = background.Background(source.background('bgtest.png'), display_height)

players.add(player)
backgrounds.add(background)
all_sprites.add(player,background)

# Game Vars
playerX, playerY = display_width/8, display_height-player.height
position = playerX
dx, dy, bg_x = 0, 0, 0
jumping = False
jump_count = 0
max_jump = 2
jump_speed = -display_height/43.2
fall_acceleration = display_height/1440.0
double_jump_buffer = display_height/216.0
move_speed = display_width/256.0
far_left , far_right = True, False

isRunning = True
fps = 60

# Game loop
while isRunning:

    # Check Events
    for event in pygame.event.get():
        # User closes window
        if event.type == pygame.QUIT:
            isRunning = False
        # Key Press Events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            if event.key == pygame.K_SPACE:
                if jump_count<2:
                    dy, jumping = jump_speed, True
                    jump_count += 1
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                dx = -move_speed
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                dx = move_speed
        if event.type == pygame.KEYUP:
            if ((event.key == pygame.K_RIGHT or event.key == pygame.K_d) and dx == move_speed) or \
                    ((event.key == pygame.K_LEFT or event.key == pygame.K_a) and dx == -move_speed):
                dx = 0

    # Player Y
    if on_platform(playerX,playerY+player.height) and not jumping:
        dy = 0
        jump_count = 0
    else:
        jumping = False
        dy += fall_acceleration

    # Update y position
    playerY += dy
    if playerY > display_height-player.height:
        playerY = display_height-player.height
    if playerY < player.height:
        playerY, dy = player.height, 0

    # Update x position
    if playerX == (display_width-player.width)/2:
        bg_x -= dx
    if not(far_left or far_right):
        playerX = (display_width-player.width)/2
    else:
        playerX += dx

    # Boundary collisions
    if playerX<0:
        playerX = 0
    elif playerX>display_width-player.width:
        playerX = display_width-player.width
    else:
        # Update Absolute Position
        position += dx

    # Update background
    if bg_x >= 0:
        far_left, far_right = True, False
        bg_x = 0
    elif bg_x <= display_width-background.width:
        far_right, far_left = True, False
        bg_x = display_width-background.width
    else:
        far_left = far_right = False

    # Draw and tick
    player.rect.x = playerX
    player.rect.y = playerY

    background.rect.x = bg_x
    background.rect.y = 0

    all_sprites.draw(display)
    all_sprites.update()

    pygame.display.update()
    clock.tick(fps)

pygame.quit()