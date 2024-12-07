# MY TIP CALCULATOR

#If the bill was $150.00, split between 5 people, with 12% tip. 
#Each person should pay (150.00 / 5) * 1.12 = 33.6
#Format the result to 2 decimal places = 33.60

#Write your code below this line 👇

#Tip Calculator
print("Welcome to my tip calculator.")
total_bill = input("what is the total bill? ")
total_bill_as_int = int(total_bill)

#total number of people to split the bill
no_of_people_to_split = input("How many people are splitting the bill? ")
no_of_people_to_split_as_int = int(no_of_people_to_split)

#Tip Percentage
desired_tip_percentage = input("What percentage tip would you like to give? ")
desired_tip_percentage_as_int = int(desired_tip_percentage)
total_tip = desired_tip_percentage_as_int * total_bill_as_int / 100

#Individual amount without tip
individual_amount = total_bill_as_int / no_of_people_to_split_as_int 

#Individual bill including 12% tip
individual_bill = individual_amount + total_tip/no_of_people_to_split_as_int

message = round(individual_bill, 2)
print(f"Your individual bill is: ${message}")