# import colorgram

# rgb_colors = []
# colors = colorgram.extract("image.jpg", 30)
#
# for color in colors:
#     r = color.rgb.r
#     g = color.rgb.g
#     b = color.rgb.b
#     new_color = (r, g, b)
#     rgb_colors.append(new_color)


import turtle as t
import random

t.colormode(255)
tim = t.Turtle()
tim.speed("fastest")
tim.penup()
tim.hideturtle()

color_list = [(237, 249, 243), (250, 238, 246), (232, 226, 93), (209, 158, 113),
              (118, 175, 209), (217, 132, 170), (187, 76, 27), (224, 59, 127), (48, 101, 156), (195, 7, 62),
              (122, 191, 159), (193, 165, 15), (36, 186, 120), (234, 164, 195), (18, 29, 163), (12, 20, 58),
              (232, 225, 5), (189, 39, 124), (153, 216, 190), (18, 183, 212), (49, 129, 76), (104, 94, 204),
              (133, 217, 231), (14, 40, 25), (35, 21, 17), (226, 81, 51), (194, 11, 5), (171, 180, 233)]

tim.setheading(225)
tim.forward(300)
tim.setheading(0)
number_of_dots = 100

for dot_count in range(1, number_of_dots + 1):
    tim.dot(20,random.choice(color_list))
    tim.forward(50)

    if dot_count % 10 == 0:
        tim.setheading(90)
        tim.forward(50)
        tim.setheading(180)
        tim.forward(500)
        tim.setheading(0)


screen = t.Screen()
screen.exitonclick()
