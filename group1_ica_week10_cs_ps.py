import turtle
import random as r
import datetime as d
import tkinter as tk
from hashlib import sha256
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# The Turtle barcode drawing code will be converted into a function.
def draw_barcode(spokes, color):
    t = turtle.Turtle()
    t.penup()
    t.goto(-400, -200)
    t.pendown()
    for i in range(len(spokes)):
        t.pencolor(color)
        t.forward(10)
        t.left(90)
        t.forward(spokes[i] * 10)
        t.right(90)
        t.forward(10)
        t.right(90)
        t.forward(spokes[i] * 10)
        t.left(90)
    turtle.done()

# Function to autonomously create a user specified amount of orders as a dictionary
def create_orders(num_orders):
    orders = []
    single_order = {}
    product_sample = ['product1', 'product2', 'product3', 'product4']

    for _ in range(num_orders):
        single_order['orderID'] = r.randint(1, 5000)
        single_order['customerID'] = r.randint(1, 5000)
        single_order['date'] = d.date(r.randint(2022, 2024), r.randint(1, 12), r.randint(1, 30)).strftime("%x")
        single_order['product'] = r.choice(product_sample)
        orders.append(single_order)

    return orders

# Function to create hashes for tuples and convert them to barcodes
def create_barcode_hashes():
    # Function call below automates 10 order creations
    orders = create_orders(10)  
    # List comprehension below creates a list of tuples of the order values
    order_tuple = [tuple(order.values()) for order in orders]
    hash_result = sha256(str(order_tuple).encode()).hexdigest()
    spokes = [int(x, 16) % 10 + 1 for x in hash_result[:10]]  # Taking the first 10 hex chars and converting to int
    draw_barcode(spokes, "red")

# Tkinter GUI setup
root = tk.Tk()
root.title("Barcode Generator")

# Matplotlib figure for Turtle graphics
canvas = FigureCanvasTkAgg(plt.figure(figsize=(5, 2)), master=root)
canvas.draw()
canvas.get_tk_widget().pack()

# Button to create a barcode
button = tk.Button(root, text="Generate Barcode", command=create_barcode_hashes)
button.pack()

# Run the Tkinter loop
root.mainloop()