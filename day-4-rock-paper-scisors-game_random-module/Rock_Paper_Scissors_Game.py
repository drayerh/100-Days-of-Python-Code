#My Rock Paper Scissors Game
#Built by Drayerh
#Art Generated from ASCII Art Generator
#Hope you have fun seeking the hidden treasure!
#For detailed rules of the game, visit: https://wrpsa.com/the-official-rules-of-rock-paper-scissors/

# Basic Rules of Game


# Rock wins against scissors.
# Scissors win against paper.
# Paper wins against rock.


rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

#Write your code below this line 👇
game_images = [rock, paper, scissors]

import random

user_choice = int(input("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors.\n "))
if user_choice >= 3 or user_choice < 0:
  print("You typed an invalid number, you lose!")
else:  
  print(f"You chose: {game_images[user_choice]}")

  computer_choice = random.randint(0, 2)
  print(f"Computer chose: {game_images[computer_choice]}")


  if user_choice == 0 and computer_choice == 2:
    print("You win!")
  elif computer_choice == 0 and user_choice == 2:
    print("You lose! ")
  elif computer_choice > user_choice:
    print("You lose!")
  elif user_choice > computer_choice:
    print("You win! ")
  elif computer_choice == user_choice:
    print("It's a draw! ")


