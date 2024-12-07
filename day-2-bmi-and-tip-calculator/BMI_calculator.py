# BMI CALCULATOR

height = input("enter your height in m: ")
weight = input("enter your weight in kg: ")

#check data type of variables using type function - height and weight are str 
#convert data type from str to float
BMI = float(weight)/float(height)**2
print(f"your BMI is {BMI}")
#round off BMI to 2decimal places
print(round(BMI, 2))



