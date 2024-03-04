import random
import time
import turtle
import tkinter as tk
from tkinter import ttk

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
        # menu and tk stuff added by asad 
        # Creating a new tkinter window to ask for user input
        menu = tk.Frame(root, bg="green")
        menu.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(menu, text="Choose a color:", width=20, bg="green", fg="white", font=("Helvetica", 14)).pack(side=tk.TOP, pady=10)
        self.color = tk.StringVar(menu)
        self.color.set("white")  # default value
        color_options = ["white", "blue", "red", "green", "yellow"]
        for option in color_options:
            tk.Radiobutton(menu, text=option, variable=self.color, value=option, bg="green", font=("Helvetica", 12)).pack(side=tk.TOP)

        tk.Label(menu, text="Choose a shape:", width=20, bg="green", fg="white", font=("Helvetica", 14)).pack(side=tk.TOP, pady=10)
        self.shape = tk.StringVar(menu)
        self.shape.set("square")  # default value
        shape_options = ["square", "circle", "triangle"]
        for option in shape_options:
            tk.Radiobutton(menu, text=option, variable=self.shape, value=option, bg="green", font=("Helvetica", 12)).pack(side=tk.TOP)

        tk.Button(menu, text="OK", command=menu.destroy, width=10, bg="green", fg="white", font=("Helvetica", 14)).pack(side=tk.TOP, pady=10)
        # This will block until the menu frame is destroyed
        root.wait_window(menu)

        self.canvas = canvas
        self.canvas.config(bg="green")

        self.score_canvas = score_canvas
        self.score_canvas.config(bg="blue")

        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.bgcolor("green")

        self.score_screen = turtle.TurtleScreen(self.score_canvas)
        self.score_screen.bgcolor("blue")

        self.draw_background()
    
        self.root = root
        self.game_over = False
        root.protocol("WM_DELETE_WINDOW", self.end_game)

        self.head, self.eyes = self.create_turtle(self.shape.get(), self.color.get(), (0, 0), eyes=True)
        self.head.direction = "stop"  
        self.food = self.create_food()
        self.segments = []
        self.score = 0
        self.high_score = 0
        self.score_label = tk.Label(self.score_canvas, bg="blue", fg="white", font=("Courier", 24, "normal"), width=31)
        self.score_label.pack()


        self.canvas.bind("<Up>", lambda event: self.change_direction("up"))
        self.canvas.bind("<Down>", lambda event: self.change_direction("down"))
        self.canvas.bind("<Left>", lambda event: self.change_direction("left"))
        self.canvas.bind("<Right>", lambda event: self.change_direction("right"))
        self.canvas.focus_set()

        self.speed = 10
        self.update_score_display()

    # by asad to draw background
    def draw_background(self):
        background_turtle = turtle.RawTurtle(self.screen)
        background_turtle.speed(0)
        background_turtle.shape("square")
        background_turtle.penup()

        start_x = -290
        start_y = 290  
        colors = ["green", "dark green"]

        self.screen.tracer(0)

        for i in range(30):  
            for j in range(30):  
                background_turtle.color(colors[(i + j) % 2])
                background_turtle.goto(start_x + j * self.SEGMENT_SIZE, start_y - i * self.SEGMENT_SIZE)
                background_turtle.stamp()
        self.screen.tracer(1)
        self.screen.update()
        
        background_turtle.hideturtle()


    def create_turtle(self, shape, color, start_pos, screen=None, eyes=False):
        if screen is None:
            screen = self.screen
        turtle_obj = turtle.RawTurtle(screen)
        turtle_obj.speed(0)
        turtle_obj.shape(shape)
        turtle_obj.color(color)
        turtle_obj.penup()
        turtle_obj.goto(start_pos)

        #added by asad to draw eyes
        eyes_turtles = []
        if eyes:
            eye_color = "black"  
            eye_size = 0.1  
            eye_offset = (5, 5)  
            for _ in range(2):
                eye = turtle.RawTurtle(screen)
                eye.speed(0)
                eye.shape("circle")
                eye.color(eye_color)
                eye.shapesize(eye_size)
                eye.penup()
                eye.goto(start_pos[0] + eye_offset[0], start_pos[1] + eye_offset[1])
                eye_offset = (eye_offset[0], -eye_offset[1]) 
                eyes_turtles.append(eye)
        return turtle_obj, eyes_turtles

    def create_food(self):
        food, _ = self.create_turtle("circle", "red", (random.randint(-290, 290), random.randint(-290, 290)))
        return food

    def change_direction(self, direction):
        if self.head.direction == "stop" or self.DIRECTIONS.get(direction) != (-self.DIRECTIONS[self.head.direction][0], -self.DIRECTIONS[self.head.direction][1]):
            self.head.direction = direction

    def move(self):
        new_pos = (self.head.xcor(), self.head.ycor())
        eye_offset = (-5, 5)
        eye_offset2 = (5, 5)

        # Move only if direction is set
        if self.head.direction != "stop":
            new_pos = (self.head.xcor() + self.DIRECTIONS[self.head.direction][0], self.head.ycor() + self.DIRECTIONS[self.head.direction][1])            
            self.head.setpos(new_pos)

            #added by asad to move the eyes with the head
            if self.head.direction == "up":
                eye_offset = (-5, 5)  
                eye_offset2 = (5, 5)  
            elif self.head.direction == "down":
                eye_offset = (-5, -5)  
                eye_offset2 = (5, -5)  
            elif self.head.direction == "left":
                eye_offset = (-5, -5)  
                eye_offset2 = (-5, 5)  
            elif self.head.direction == "right":
                eye_offset = (5, -5)  
                eye_offset2 = (5, 5)  
            
        for i, eye in enumerate(self.eyes):
            if i == 0:
                eye.goto(new_pos[0] + eye_offset[0], new_pos[1] + eye_offset[1])
            else:
                eye.goto(new_pos[0] + eye_offset2[0], new_pos[1] + eye_offset2[1])

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
            new_segment, _ = self.create_turtle("square", "grey", self.head.position())
            self.segments.append(new_segment)
            self.update_segments()
            if self.score == 0:
                self.DELAY = 0.1
            else:
                self.DELAY *= 0.99
            
            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score
            self.update_score_display()
            #self.speed += 2
            #self.DELAY = 1 / self.speed

    def update_score_display(self):
        self.score_label.config(text="Score: {}  High Score: {}".format(self.score, self.high_score))

    def reset_game(self):
        time.sleep(1)
        self.head.goto(0, 0)
        self.head.direction = "stop"
        for segment in self.segments:
            segment.goto(1000, 1000)
        self.segments.clear()
        self.score_label.config(text="")
        self.score = 0
        self.update_score_display()
        self.food.goto(random.randint(-290, 290), random.randint(-290, 290))

    def update_segments(self):
        if self.segments:
            for index in range(len(self.segments) - 1, 0, -1):
                self.segments[index].goto(self.segments[index - 1].pos())
            self.segments[0].goto(self.head.pos())

    #by asad
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
