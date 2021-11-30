import colorgram
import turtle as t
import random as rand

color_list = []
colors = colorgram.extract('hirst_img.jpg', 30)
for color in colors:
    if color.rgb.r < 250 and color.rgb.g < 250 and color.rgb.b < 250:
        r = color.rgb.r
        g = color.rgb.g
        b = color.rgb.b
        new_color = (r, g, b)
        color_list.append(new_color)

t.colormode(255)
tim = t.Turtle()
screen = t.Screen()


def more_dots(x, y):

    tim.goto(x, y)
    for i in range(10):
        screen.colormode(255)
        tim.dot(20, rand.choice(color_list))
        tim.forward(50)


def main():
    tim.hideturtle()
    tim.penup()
    tim.speed("fastest")
    x_pos = -225
    y_pos = -225

    for i in range(10):
        more_dots(x_pos, y_pos)
        y_pos += 50

    screen.exitonclick()


main()

