import pygame
import random

class Background:
    def __init__(self, screen, size, color1, color2):
        self.screen = screen
        self.size = size
        self.color1 = color1
        self.color2 = color2

    def draw(self):
        colors = [self.color1, self.color2]
        block_size = self.size
        for y in range(0, self.screen.get_height(), block_size):
            for x in range(0, self.screen.get_width(), block_size):
                rect = pygame.Rect(x, y, block_size, block_size)
                pygame.draw.rect(self.screen, colors[((x//block_size % 2) + (y//block_size % 2)) % 2], rect)

class Button:
    def __init__(self, color, x, y, width, height, text='', toggleable=False):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.toggleable = toggleable
        self.toggled = False

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (255, 255, 255))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

    def toggle(self):
        if self.toggleable:
            self.toggled = not self.toggled



class SnakeGame:
    SEGMENT_SIZE = 20
    DELAY = 0.1
    DIRECTIONS = {"up": (0, -SEGMENT_SIZE),
                  "down": (0, SEGMENT_SIZE),
                  "left": (-SEGMENT_SIZE, 0),
                  "right": (SEGMENT_SIZE, 0)}

    def __init__(self):
        pygame.init()

        # Initialize sound effects and background sounds
        self.level_up_sound = pygame.mixer.Sound("level_up.wav")
        self.losing_sound = pygame.mixer.Sound("player_loses.wav")
        self.background_music = pygame.mixer.music.load("background_music.mp3")

        # Play background music to infinitely loop
        pygame.mixer.music.play(loops=-1)

        self.music_paused = False
        self.sfx_paused = False

        self.width = 600
        self.height = 600
        self.score_screen = pygame.Surface((self.width, 40))
        self.score_screen.fill((0, 0, 0))  # Fill it with black color

        #self.height -= 100
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        self.head = [self.width // 2, self.height // 2]
        self.direction = "stop"
        self.segments = []
        self.score = 0
        self.high_score = 0
        self.background = Background(self.screen, 20, (0, 128, 0), (0, 100, 0))


        self.font = pygame.font.Font(None, 36)
        self.food = self.create_food()
        self.game_over = False

        self.pause_button = Button((255, 0, 0), 20, 5, 70, 30, 'Pause')
        self.reset_button = Button((255, 0, 0), self.width // 2 - 50, self.height // 2 - 100, 100, 50, 'Reset')
        self.quit_button = Button((255, 0, 0), self.width // 2 - 50, self.height // 2 + 80, 100, 50, 'Quit')

        # Create buttons for toggling music and SFX
        self.music_button = Button((255, 0, 0), self.width // 2 - 100, self.height // 2 - 40, 200, 50, 'Toggle Music', toggleable=True)
        self.sfx_button = Button((255, 0, 0), self.width // 2 - 100, self.height // 2 + 20, 200, 50, 'Toggle SFX', toggleable=True)
        self.start_button = Button((0, 255, 0), self.width // 2 - 50, self.height // 2 - 25, 100, 50, 'Start')


    def create_food(self):
        while True:
            food = [random.randrange(20, self.width - self.SEGMENT_SIZE - 20, self.SEGMENT_SIZE),
                    random.randrange(60, self.height - self.SEGMENT_SIZE - 20, self.SEGMENT_SIZE)]
            if food not in self.segments and food != self.head:
                return food
            
    def draw_text(self, text, color, x, y, surface=None, size=None):
        font_size = size if size is not None else 36
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        rect = text_surface.get_rect(center=(x, y))  # Get a rect with the center at the given position
        (surface if surface is not None else self.screen).blit(text_surface, rect)

    def draw_segment(self, color, pos):
        pygame.draw.rect(self.screen, color, (pos[0], pos[1], self.SEGMENT_SIZE, self.SEGMENT_SIZE))

    def change_direction(self, direction):
        if self.direction == "stop" or self.DIRECTIONS.get(direction) != (-self.DIRECTIONS[self.direction][0], -self.DIRECTIONS[self.direction][1]):
            self.direction = direction

    def move(self):
        if self.direction != "stop":
            # Move the segments to follow the head
            if self.segments:
                for i in range(len(self.segments)-1, 0, -1):
                    self.segments[i] = list(self.segments[i-1])
                self.segments[0] = list(self.head)

            # Move the head
            new_head = [self.head[0] + self.DIRECTIONS[self.direction][0], self.head[1] + self.DIRECTIONS[self.direction][1]]
            self.head = new_head

    def check_collision(self):
        # Check if the snake has hit the score board
        if self.head[1] < 40:
            if not self.sfx_paused:
                self.losing_sound.play()
            self.game_over = True
            pygame.mixer.music.stop()
        # Check if the snake has hit the edge of the screen or itself
        elif self.head[0] < 0 or self.head[0] >= self.width or self.head[1] < 40 or self.head[1] >= self.height or self.head in self.segments:
            if not self.sfx_paused:
                self.losing_sound.play()
            self.game_over = True
            pygame.mixer.music.stop()

    def update_score(self):
        if self.head == self.food:
            # Play level up sound effect
            if not self.sfx_paused:
                self.level_up_sound.play()
            self.food = self.create_food()
            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score
            # Add a new segment to the snake's body
            new_segment = self.head[:]
            self.segments.insert(0, new_segment)

    def reset_game(self):
        self.head = [self.width // 2, self.height // 2]
        self.direction = "stop"
        self.segments.clear()
        self.score = 0
        self.game_over = False
        if not self.music_paused:
            pygame.mixer.music.play(loops=-1)

    def update_score_screen(self):
        # Clear the score screen
        self.score_screen.fill((0, 0, 0))

        # Draw the score and high score
        self.draw_text("Score: " + str(self.score) + "  High Score: " + str(self.high_score), (255, 255, 255), 300, 25, self.score_screen)

        # Draw the pause button
        self.pause_button.draw(self.score_screen, (0, 0, 0))

    def update_screen(self):
        # Draw the checkered background
        self.background.draw()

        # Draw snake segments
        for segment in self.segments:
            self.draw_segment((0, 255, 0), segment)

        # Draw snake head
        self.draw_segment((0, 200, 0), self.head)

        # Draw food as a circle
        pygame.draw.circle(self.screen, (255, 0, 0), (self.food[0] + self.SEGMENT_SIZE // 2, self.food[1] + self.SEGMENT_SIZE // 2), self.SEGMENT_SIZE // 2)

        # Draw score
        #self.draw_text("Score: " + str(self.score) + "  High Score: " + str(self.high_score), (255, 255, 255), 300, 20)

        self.screen.blit(self.score_screen, (0, 0))

        pygame.display.flip()

    def game_over_screen(self):
        self.screen.fill((0, 0, 0))  # Fill the screen with black color
        self.draw_text("GAME OVER", (255, 0, 0), self.width // 2, self.height // 2 - 50)  # Draw "GAME OVER" text in the center of the screen
        self.draw_text("Press SPACE to play again", (255, 255, 255), self.width // 2, (self.height // 2))  # Draw instructions below the "GAME OVER" text
        pygame.display.flip()  # Update the screen

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYUP:  # Wait for a key press to restart the game
                    if event.key == pygame.K_SPACE:  # Only continue if the space bar is pressed
                        waiting = False

    def start_screen(self):
        start = False

        while not start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.is_over(pygame.mouse.get_pos()):
                        start = True
            self.screen.fill((0, 200, 0))
            self.draw_text("SNAKE GAME", (255, 255, 255), self.width // 2, self.height // 2 - 50, size=50)
            # Draw the start button
            self.start_button.draw(self.screen, (255, 255, 255))
            pygame.display.flip()

    def toggle_music(self):
        self.music_paused = not self.music_paused
        if self.music_paused:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def toggle_sfx(self):
        if self.sfx_paused:
            self.sfx_paused = False
        else: 
            self.sfx_paused = True

    def start(self):
        self.start_screen()
        running = True
        paused = False
        self.game_over = False
        move_counter = 0


        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.change_direction("up")
                    elif event.key == pygame.K_DOWN:
                        self.change_direction("down")
                    elif event.key == pygame.K_LEFT:
                        self.change_direction("left")
                    elif event.key == pygame.K_RIGHT:
                        self.change_direction("right")
                    elif event.key == pygame.K_ESCAPE:  # Pause the game when ESC is pressed
                        paused = not paused
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.pause_button.is_over(pygame.mouse.get_pos()):
                        paused = not paused
                    elif self.reset_button.is_over(pygame.mouse.get_pos()):
                        self.reset_game()
                        paused = False
                    elif self.quit_button.is_over(pygame.mouse.get_pos()):  # Quit button
                        running = False

                    elif self.music_button.is_over(pygame.mouse.get_pos()):  # Toggle music button
                        self.toggle_music()
                        if self.music_paused:
                            pygame.mixer.music.pause()  
                        else:
                            pygame.mixer.music.play(loops=-1)

                    elif self.sfx_button.is_over(pygame.mouse.get_pos()):  # Toggle SFX button
                        self.toggle_sfx()

                        
                elif self.reset_button.is_over(pygame.mouse.get_pos()):  
                    self.reset_button.color = (255, 0, 0)
                elif self.music_button.is_over(pygame.mouse.get_pos()):
                    if self.music_paused:
                        self.music_button.color = (0, 0, 255)
                    else:  
                        self.music_button.color = (255, 0, 0)
                elif self.sfx_button.is_over(pygame.mouse.get_pos()):
                    if self.sfx_paused:
                        self.sfx_button.color = (0, 0, 255)
                    else:  
                        self.sfx_button.color = (255, 0, 0)
                elif self.quit_button.is_over(pygame.mouse.get_pos()):  
                    self.quit_button.color = (255, 0, 0) 
                else:
                    self.reset_button.color = (200, 0, 0)
                    if self.music_paused:
                        self.music_button.color = (0, 0, 200)
                    else:
                        self.music_button.color = (200, 0, 0)
                    if self.sfx_paused:
                        self.sfx_button.color = (0, 0, 200)
                    else:
                        self.sfx_button.color = (200, 0, 0)
                    self.quit_button.color = (200, 0, 0)

            if not self.game_over and not paused:
                # Only move the snake every 6 frames (for example)
                if move_counter % 4 == 0:
                    self.move()
                    self.check_collision()
                    self.update_score()

                self.update_score_screen()
                self.update_screen()
                self.clock.tick(60)  

            elif paused:
                self.draw_text("GAME PAUSED", (255, 255, 255), self.width // 2, self.height // 2 - 150, size=50)  
                self.reset_button.draw(self.screen, (0, 0, 0))
                self.music_button.draw(self.screen, (0, 0, 0))
                self.sfx_button.draw(self.screen, (0, 0, 0))
                self.quit_button.draw(self.screen, (0, 0, 0))
                pygame.display.flip()  # Update the screen

            move_counter += 1
            if self.game_over:
                self.game_over_screen()
                self.reset_game()
                self.game_over = False

            self.pause_button.draw(self.screen, (0, 0, 0))
            if self.pause_button.is_over(pygame.mouse.get_pos()):
                self.pause_button.color = (255, 0, 0)
            else:
                self.pause_button.color = (200, 0, 0)

        pygame.quit()




if __name__ == "__main__":
    game = SnakeGame()
    game.start()
