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

        self.width = 600
        self.height = 600
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


    def create_food(self):
        while True:
            food = [random.randrange(0, self.width - self.SEGMENT_SIZE, self.SEGMENT_SIZE),
                    random.randrange(0, self.height - self.SEGMENT_SIZE, self.SEGMENT_SIZE)]
            if food not in self.segments and food != self.head:
                return food
            
    def draw_text(self, text, color, x, y):
        surface = self.font.render(text, True, color)
        rect = surface.get_rect(center=(x, y))  # Get a rect with the center at the given position
        self.screen.blit(surface, rect)

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
        if self.head[0] < 0 or self.head[0] >= self.width or self.head[1] < 0 or self.head[1] >= self.height or self.head in self.segments:
            # Play losing sound effect
            self.losing_sound.play()
            self.game_over = True
            # Stop the background music when player loses
            pygame.mixer.music.stop()

    def update_score(self):
        if self.head == self.food:
            # Play level up sound effect
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
        # Start background music again when the game resets
        pygame.mixer.music.play(loops=-1)


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
        self.draw_text("Score: " + str(self.score) + "  High Score: " + str(self.high_score), (255, 255, 255), 300, 20)

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

    def start(self):
        running = True
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

            if not self.game_over:
                # Only move the snake every 6 frames (for example)
                if move_counter % 4 == 0:
                    self.move()
                    self.check_collision()
                    self.update_score()

                self.update_screen()
                self.clock.tick(60)  

            move_counter += 1
            if self.game_over:
                self.game_over_screen()
                self.reset_game()
                self.game_over = False

        pygame.quit()



if __name__ == "__main__":
    game = SnakeGame()
    game.start()