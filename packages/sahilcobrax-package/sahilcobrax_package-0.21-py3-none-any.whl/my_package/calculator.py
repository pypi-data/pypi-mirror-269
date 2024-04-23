import my_package.mult
import my_package.sub
import my_package.sum

print("enter value to calculate: ")
print(" 1) summation \n 2) subtraction \n 3) multiplication ")

val=int(input("Enter choice: "))

x=float(input("operand 1: "))
y=float(input("operand 2: "))

if (val==1):
    print(my_package.sum.summation(x,y))
elif (val==2):
    print(my_package.sub.subtraction(x,y))
elif (val==3):
    print(my_package.mult.multiplication(x,y))
else:
    print("Operation not in list.")
    

