#My Treasure Island Game
#Built by Drayerh
#Art Generated from ASCII Art Generator
#Hope you have fun seeking the hidden treasure!

print('''
*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
|                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/_____ /
*******************************************************************************
''')
print("Welcome to Treasure Island.")
print("Your mission is to find the treasure.") 

#https://www.draw.io/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=Treasure%20Island%20Conditional.drawio#Uhttps%3A%2F%2Fdrive.google.com%2Fuc%3Fid%3D1oDe4ehjWZipYRsVfeAx2HyB7LCQ8_Fvi%26export%3Ddownload

#Write your code below this line 👇
left_or_right = input("Which path would you like to take? left or right? ")
left_or_right_lower_case = left_or_right.lower() 
if left_or_right_lower_case == "left":
    print("You just arrived at the River bank.\n ")
    swim_or_wait = input("Would you like to swim or wait? ")
    swim_or_wait_lower_case = swim_or_wait.lower()
    if swim_or_wait_lower_case == "wait":
        print("You made it to the door of no return.\n ")
        which_door = input("Which door would you like to take? Red, Yellow or Blue? ")
        which_door_lower_case = which_door.lower()
        if which_door_lower_case == "yellow":
            print(''' __   __  _______  __   __    _     _  ___   __    _  __  
|  | |  ||       ||  | |  |  | | _ | ||   | |  |  | ||  | 
|  |_|  ||   _   ||  | |  |  | || || ||   | |   |_| ||  | 
|       ||  | |  ||  |_|  |  |       ||   | |       ||  | 
|_     _||  |_|  ||       |  |       ||   | |  _    ||__| 
  |   |  |       ||       |  |   _   ||   | | | |   | __  
  |___|  |_______||_______|  |__| |__||___| |_|  |__||__| \n You just found the hidden treasure. ''')
        elif which_door_lower_case == "red":
            print("Burned by fire! Game Over! ")
        elif which_door_lower_case == "blue":
            print("Eaten by beasts. Game Over! ") 
        else: 
            print("Game Over! ")
    else: print("Game Over!")
else: 
    print("Game Over!")





