#Escaping the Maze Game
#Built by Drayerh
#Visit the folowing website to run the code. https://reeborg.ca/reeborg.html 
#Choose maze in the option of challenges. 
#Hope you have fun escaping the maze home!

def turn_right():
    turn_left()
    turn_left()
    turn_left()

while front_is_clear():
    move()
turn_left()

while not at_goal():
    if right_is_clear():
        turn_right()
        move()
    elif front_is_clear():
        move()
    else:
        turn_left()

#To avoid infinite loop error, the first while loop has been put in place for Reeborg.
# #When Reeborg starts from the center an infinite loop can be encountered