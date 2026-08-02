import math

a = 1
print(type(a))

a = 1.0
print(type(a))

b = 0.1 * 3 
if b == 0.3:
    print("True")
else: 
    print("False")
    
if math.isclose(b, 0.3):
    print("True")
    
else : 
    print("False")
    
print(7/2)
print(8/2)
print(type(8/2))
print(8//2)
print(5//3)
print(5//3.0)
print(5%3)
print(10/3)
print(10//3)