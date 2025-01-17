def turns(n):
    count = 0
    while n >= 9:
        count += 1
        n -= 9
    while n >= 7:
        count += 1
        n -= 7
    while n >= 1:
        count += 1
        n -= 1
    return count

# Example usage:
n = 15
result = turns(n)
print(f"The minimum number of turns to reach 0 sticks with {n} starting sticks is: {result}")
