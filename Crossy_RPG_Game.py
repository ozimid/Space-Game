# Pygame development
# Start the basic game set up. Set up the Display
# Set up th game loop to render graphics
# Draw objects to the Display. Loud images into objects
# Focus on making code object oriented. Introduce classes and objects into our code
# Implement game classes. Implement generic game object class
# Implement player character class and movement
# Implement enemy character class and bounds checking
# Implement collision detection. Detect collision with treasure and enemies
# Add true end game condition. Implement specific win and lose condition
# Add more enemies and make them move faster

import pygame # Gain access to the pygame library

SCREEN_TITLE = "Crossy RPG"
SCREEN_WIDTH = 1100 # Size of screen
SCREEN_HEIGHT = 800
PURPLE_COLOR = (120,0,128) # Collors according to RGB codes
GREEN_COLOR = (0,128,0)
BLUE_COLOR = (0,191,255)
WHITE_COLOR = (255,255,255)
RED_COLOR = (255,0,0)
GRAY_COLOR = (128,128,128)
BLACK_COLOR = (0,0,0)
clock = pygame.time.Clock() # Clock used to update game event and frames
pygame.font.init() # Initialaze Font from pygame library
font = pygame.font.SysFont('comicsans', 65)

class Game:

    TICK_RATE = 60 # TYpical rate of 60, equivalent to FPS

    def __init__(self, image_path, title, width, height): # Initialazer for the game class to set up the width, height and title
        self.title = title
        self.width = width
        self.height = height

        self.game_display = pygame.display.set_mode((width, height)) # Create the window of specified size in white to display the game
        self.game_display.fill(BLUE_COLOR) # Set the game window color to white
        pygame.display.set_caption(title)

        background_image = pygame.image.load(image_path) # Load and set the background image for the scene
        self.image = pygame.transform.scale(background_image, (width, height))

    def run_game_loop(self, level_speed):
        is_game_over = False
        did_win = False
        direction = 0

        player_character = PlayerCharacter('player.png', 520, 700, 70, 70)
        enemy_0 = NonPlayerCharacter('satellite0.png', 20, 600, 70, 70)
        enemy_0.SPEED *= level_speed # Speed increased as we advance in difficulty

        enemy_1 = NonPlayerCharacter('satellite2.png', self.width -40, 400, 100, 100) # Create another enemy
        enemy_1.SPEED *= level_speed

        enemy_2 = NonPlayerCharacter('satellite.png', 30, 200, 100, 100) # Create another enemy
        enemy_2.SPEED *= level_speed

        treasure = GameObject('moon.png', 505, 10, 100, 100)

        while not is_game_over: # Main game loop, used to update all gameplay (movement, checks, graphics). Runs until is_game_over = True

            for event in pygame.event.get(): # A loop to get all of the events (mouse and button clicks) occuring at any given time
                if event.type == pygame.QUIT: # If we have a quite type event(exit out) then exit out of the game loop
                    is_game_over = True
                elif event.type == pygame.KEYDOWN: # Detect when key is pressed down
                    if event.key == pygame.K_UP: # Move up if up key pressed
                        direction = 1
                    elif event.key == pygame.K_DOWN: # Move down if down key pressed
                        direction = -1
                elif event.type == pygame.KEYUP: # Detect when key is released
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN: # Stop movement when key no longer pressed
                        direction = 0
                print (event)

            self.game_display.fill(BLUE_COLOR) # Redraw the screen to be a blank purple window
            self.game_display.blit(self.image, (0, 0)) # Draw the image onto the background
            treasure.draw(self.game_display) # Draw the treasure
            player_character.move(direction, self.height) # Update the player position
            player_character.draw(self.game_display) # Draw the player at the new position

            enemy_0.move(self.width)
            enemy_0.draw(self.game_display)

            if level_speed > 1: # Move and draw more enemies when we reach higher levels of difficulty
                enemy_1.move(self.width)
                enemy_1.draw(self.game_display)

            if level_speed > 2:
                enemy_2.move(self.width)
                enemy_2.draw(self.game_display)

            if player_character.detect_collision(enemy_0): # End game if collision between enemy and treasure. Close game if we lose. Restart game if we win
                is_game_over = True
                did_win = False
                text = font.render("YOU CRASHED :(", True, PURPLE_COLOR)
                self.game_display.blit(text, (420,350))
                pygame.display.update()
                clock.tick(2)
                break
            elif player_character.detect_collision(treasure):
                is_game_over = True
                did_win = True
                text = font.render("You landed! :)", True, GREEN_COLOR)
                self.game_display.blit(text, (420,350))
                pygame.display.update()
                clock.tick(2)
                break

            pygame.display.update() # Update all game graphics
            clock.tick(self.TICK_RATE) # Tick the clock to update everything within the game

        if did_win: # Restart game loop  if we won. Break out of game loop and quit if we lose
            self.run_game_loop(level_speed + 0.5)
        else:
            return

class GameObject: # super class. Generic game object class to be subclassed by other objects in the game

    def __init__(self, image_path, x, y, width, height):
        object_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(object_image, (width,height)) # scale image up

        self.x_pos = x
        self.y_pos = y

        self.width = width
        self.height = height

    def draw(self, background):
        background.blit(self.image, (self.x_pos, self.y_pos))

class PlayerCharacter(GameObject): # Class to represent the character controlled by the player

    SPEED = 10 # How many tiles the the character moves per second

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, direction, max_height): # Move function  will move character up if direction > 0 and down if < 0
        if direction > 0:
            self.y_pos -= self.SPEED
        elif direction < 0:
            self.y_pos += self.SPEED

        if self.y_pos >= max_height - 20: # border for object
            self.y_pos = max_height -20

    def detect_collision (self, other_body): # Return False (no collision) if y_pos and x_pos do not overlap. Return True x_pos and y_pos overlap
        if self.y_pos > other_body.y_pos + other_body.height:
            return False
        elif self.y_pos + self.height < other_body.y_pos:
            return False

        if self.x_pos > other_body.x_pos + other_body.width:
            return False
        elif self.x_pos + self.width < other_body.x_pos:
            return False

        return True

class NonPlayerCharacter(GameObject): # Class to represent the noncharacter-enemy moving left to right and right to left

    SPEED = 5 # How many tiles the the character moves per second

    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height)

    def move(self, max_width): # Move function will move character right once it hits the far left of the scren and left once it hits the far right of  the scren
        if self.x_pos <= 20:
            self.SPEED = abs(self.SPEED) # if +SPEED then do -SPEED and naooborot
        elif self.x_pos >= max_width - 40:
            self.SPEED = -abs(self.SPEED)
        self.x_pos += self.SPEED

pygame.init()

new_game = Game('background.png', SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
new_game.run_game_loop(1)

pygame.quit() #Quit pygame and the program
quit()


# earth.draw(self.game_display) # Draw the earth
    #earth = GameObject ('globe.png', 350, 750, 100, 100)

#player_image = pygame.image.load('player.png')
#player_image = pygame.transform.scale(player_image, (50,50)) # scale image up

    # pygame.draw.rect(game_display, BLACK_COLOR, [350, 350, 100, 100]) # Draw objects to the Display. Create black kwadrat.(x,y, width, height)
    # pygame.draw.circle(game_display, BLACK_COLOR, (400, 300), 50) # Draw a circle on  top of the game screen (x,y, radius)

    #game_display.blit(player_image, (375,375))
