def fact(n):
	if n == 0 or n == 1:
		return 1
	else:
		return n * fact(n-1)
n = int(input("Enter the Number to Get Factorial:"))
res = fact(n)
print(f"Factorial of Number {n}:",res)
