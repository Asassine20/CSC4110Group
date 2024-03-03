import random
import time
import turtle
import tkinter as tk

class SnakeGame:
    ''' SnakeGame class represents the main game logic for a
    simple Snake game implemented using the Turtle module
    '''

    SEGMENT_SIZE = 20
    DELAY = 0.1
    DIRECTIONS = {"up": (0, SEGMENT_SIZE), 
                  "down": (0, -SEGMENT_SIZE), 
                  "left": (-SEGMENT_SIZE, 0), 
                  "right": (SEGMENT_SIZE, 0)}

    def __init__(self, canvas, score_canvas, root):
        self.canvas = canvas
        self.canvas.config(bg="green")

        self.score_canvas = score_canvas
        self.score_canvas.config(bg="blue")

        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor("green")

        self.score_screen = turtle.TurtleScreen(self.score_canvas)
        self.score_screen.bgcolor("blue")

        self.root = root
        self.game_over = False
        root.protocol("WM_DELETE_WINDOW", self.end_game)

        self.head = self.create_turtle("square", "white", (0, 0))
        self.head.direction = "stop"  
        self.food = self.create_food()
        self.segments = []
        self.score = 0
        self.high_score = 0
        self.score_display = self.create_score_display()

        self.canvas.bind("<Up>", lambda event: self.change_direction("up"))
        self.canvas.bind("<Down>", lambda event: self.change_direction("down"))
        self.canvas.bind("<Left>", lambda event: self.change_direction("left"))
        self.canvas.bind("<Right>", lambda event: self.change_direction("right"))
        self.canvas.focus_set()

        self.speed = 10
        self.update_score_display()


    def create_turtle(self, shape, color, start_pos, screen=None):
        if screen is None:
            screen = self.screen
        turtle_obj = turtle.RawTurtle(screen)
        turtle_obj.speed(0)
        turtle_obj.shape(shape)
        turtle_obj.color(color)
        turtle_obj.penup()
        turtle_obj.goto(start_pos)
        return turtle_obj

    def create_food(self):
        return self.create_turtle("circle", "red", (random.randint(-290, 290), random.randint(-290, 290)))

    def create_score_display(self):
        score_display = self.create_turtle("square", "white", (0, -20), self.score_screen)
        score_display.hideturtle()
        return score_display

    def change_direction(self, direction):
        if self.head.direction == "stop" or self.DIRECTIONS.get(direction) != (-self.DIRECTIONS[self.head.direction][0], -self.DIRECTIONS[self.head.direction][1]):
            self.head.direction = direction

    def move(self):
        # Move only if direction is set
        if self.head.direction != "stop":
            self.head.setpos(self.head.pos() + self.DIRECTIONS[self.head.direction])

    def check_collision(self):
        if abs(self.head.xcor()) > 290 or abs(self.head.ycor()) > 290 or any(segment.distance(self.head) < self.SEGMENT_SIZE for segment in self.segments):
            self.reset_game()

    def update_score(self):
        food_pos = self.food.pos()
        while any(food_pos == segment.pos() for segment in self.segments):
            self.food.goto(random.randint(-290, 290), random.randint(-290, 290))
            food_pos = self.food.pos()

        if self.head.distance(self.food) < self.SEGMENT_SIZE:
            self.food.goto(random.randint(-290, 290), random.randint(-290, 290))
            self.segments.append(self.create_turtle("square", "grey", self.head.position()))
            self.update_segments()
            self.DELAY *= 0.9
            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score
            self.update_score_display()
            #self.speed += 2
            #self.DELAY = 1 / self.speed

    def update_score_display(self):
        self.score_display.clear()
        self.score_display.color("white")  
        self.score_display.penup()
        self.score_display.goto(0, -20)
        self.score_display.write("Score: {}  High Score: {}".format(self.score, self.high_score), align="center",
                            font=("Courier", 24, "normal"))

    def reset_game(self):
        time.sleep(1)
        self.head.goto(0, 0)
        self.head.direction = "stop"
        for segment in self.segments:
            segment.goto(1000, 1000)
        self.segments.clear()
        self.score_display.clear()
        self.score = 0
        self.update_score_display()
        self.food.goto(random.randint(-290, 290), random.randint(-290, 290))

    def update_segments(self):
        if self.segments:
            for index in range(len(self.segments) - 1, 0, -1):
                self.segments[index].goto(self.segments[index - 1].pos())
            self.segments[0].goto(self.head.pos())

    def end_game(self):
        self.game_over = True
        self.root.destroy()

    def start(self):
        while not self.game_over:
            start_time = time.time()
            self.check_collision()
            self.update_score()
            self.update_segments()
            self.move()
            end_time = time.time()
            elapsed_taken = end_time - start_time

            delay = max(self.DELAY - elapsed_taken, 0.01)
            time.sleep(delay)
            # Update screen within the loop
            self.canvas.update()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Snake Game")
    canvas = tk.Canvas(root, width=600, height=600, bg="green")
    canvas.pack(side=tk.BOTTOM)

    score_canvas = tk.Canvas(root, width=600, height=40, bg="Blue")
    score_canvas.pack(side=tk.TOP)

    game = SnakeGame(canvas, score_canvas, root)
    game.start()

    root.mainloop()
