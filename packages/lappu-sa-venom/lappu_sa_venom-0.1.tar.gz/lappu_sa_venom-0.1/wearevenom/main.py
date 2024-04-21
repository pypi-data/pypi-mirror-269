
import turtle
import random
from sketchpy import library as lib

class venom:

    def __init__(self) :
        self.venom='venom'
        self.str=''

    def draw_something_cool(self):
        def fn():
            objects_list = [getattr(lib, obj) for obj in dir(lib) if not obj.startswith('__') and callable(getattr(lib, obj))]
            selected_object = random.choice(objects_list)
            obj = selected_object()
            obj.draw()
        try:
            fn()
        except:
            fn()

    def draw_spiral_for_venom(self):

        screen = turtle.Screen()
        screen.bgcolor("black")
        screen.title("Mesmerizing Spiral")


        pen = turtle.Turtle()
        pen.speed(0)
        pen.width(2)


        def draw_spiral():

            colors = ["red", "orange", "yellow", "green", "blue", "purple"]

            for i in range(360):
                pen.color(random.choice(colors))
                pen.forward(i * 2)
                pen.right(45)

        draw_spiral()


        screen.mainloop()

   

    def get_dev_name(self):

        screen = turtle.Screen()
        screen.bgcolor("black")
        screen.title("Bouncing Name")


        name_pen = turtle.Turtle()
        name_pen.speed(0)
        name_pen.color("white")
        name_pen.penup()
        name_pen.hideturtle()


        colors = ["red", "orange", "yellow", "green", "blue", "purple"]

        x, y = 0, 0
        dx, dy = 5, 5


        def update_name_position():
            nonlocal x, y, dx, dy
            x += dx
            y += dy

            if x >= screen.window_width() // 2 or x <= -screen.window_width() // 2:
                dx *= -1
                name_pen.color(random.choice(colors))  # Change color on bounce
            if y >= screen.window_height() // 2 or y <= -screen.window_height() // 2:
                dy *= -1
                name_pen.color(random.choice(colors))  # Change color on bounce

            name_pen.clear()
            name_pen.goto(x, y)
            name_pen.write("Himanshu", align="center", font=("Arial", 50, "bold"))

        while True:
            update_name_position()

        screen.mainloop()


    











        