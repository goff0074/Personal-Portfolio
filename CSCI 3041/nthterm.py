import math

def find_nth_term(a0, a1, a2, a3, n):
    # Find the characteristic polynomial coefficients
    c1 = a2 - a0
    c2 = (a3 - a1) - c1
    c3 = a1 - a0 - c1 - c2

    # Find the roots of the characteristic polynomial
    discriminant = c2**2 - 4 * c1 * c3

    if discriminant >= 0:
        root1 = (-c2 + math.sqrt(discriminant)) / (2 * c1)
        root2 = (-c2 - math.sqrt(discriminant)) / (2 * c1)

        # Check if the roots are equal
        if root1 == root2:
            # General form for repeated root
            A = a0
            B = (a1 - a0 * root1) / root1
            return round(A * root1**n + B * n * root1**(n-1))
        else:
            # General form for distinct roots
            A = (a3 - root2 * a2) / (root1 - root2)
            B = a2 - A
            return round(A * root1**n + B * root2**n)
    else:
        # Complex roots are not considered in this implementation
        raise ValueError("Characteristic polynomial has complex roots")

# Example usage
a0, a1, a2, a3, n = 3, 5, 11, 21, 30
result = find_nth_term(a0, a1, a2, a3, n)
print(result)

