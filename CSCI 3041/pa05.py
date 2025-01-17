import math
def get_nth(initial, n):
    a0, a1, a2, a3 = initial #get the initial values of the sequence
    d, c = recurr_relation(a0, a1, a2, a3) #call the function that gets the c and d coeffecients of the equation

    roots = find_roots(c, d) #call the function that  will find the roots (terms) in the closed formula
    if roots[0] == roots[1]:
        r = roots[0]
        a = a0
        b = (a1 - a0 * r) / r
        result = (a)*(r**n) + (b)*(n)*(r**n) #if the roots are equal, we apply the repeated root case
    else: #otherwise, we will continue calling functions as normal
        u, v = find_constants(a0, a1, roots, n) #call the function that finds the constants, u and v
        
        result = find_nth(u, v, roots, n) #call the function the uses variables from before to find the nth term
    # print(result)
    return int(result) # round the answer to an integer

def recurr_relation(a0, a1, a2, a3):
    matrix1 = [[a1, a0], [a2, a1]] #2x2 matrix with the coefficients of the relation
    matrix2 = [-a2, -a3] #column vector with the constants

    determinant = matrix1[0][0] * matrix1[1][1] - matrix1[0][1] * matrix1[1][0] #determinant of matrix 1

    if determinant != 0: #check to see if the determinant is not 0 so we can invert the matrix
        inv_matrix1 = [
            [matrix1[1][1] / determinant, -matrix1[0][1] / determinant],
            [-matrix1[1][0] / determinant, matrix1[0][0] / determinant]
        ] #calculating the inverse of the matrix at hand

        c = round(inv_matrix1[0][0] * matrix2[0] + inv_matrix1[0][1] * matrix2[1])
        d = round(inv_matrix1[1][0] * matrix2[0] + inv_matrix1[1][1] * matrix2[1])
        #calculating the constants c and d by multiplying the inverse of matrix 1 by matrix2

        # print(c, d)
        return d, c

def find_roots(c, d):
    descriminant = c**2 - 4*d # calculate the descriminant, to make doing the quadratic formula easier

    root1 = (-c + math.sqrt(descriminant)) / 2
    root2 = (-c - math.sqrt(descriminant)) / 2
    #calculate each root using the quadratic formula

    # print(root1, root2)
    roots = root1, root2
    return roots

def find_constants(a0, a1, roots, n):
    root1, root2 = roots
    u_expression = f"{a0} - v" # set the expression of u
    equation_with_substitution = f"{root1} * ({u_expression}) + {root2} * v - {a1}" #substitute u_expression in the recurrance equation
    v_solution = eval(f"({a1 - root1 * a0}) / ({root2 - root1})") #solve for v after substitution
    
    u_solution = eval(f"{a0} - {v_solution}") # use the value of v to help solve for u
    
    # print(u_solution, v_solution)
    return u_solution, v_solution

def find_nth(u, v, roots, n):
    root2, root1 = roots
    nth_term = (u)*((root2)**n) + (v)*((root1)**n) #use the closed form formula with the appropriate variables to solve for the nth term
    # round(nth_term)
    # print(nth_term)
    return nth_term

# print(get_nth([1,4,15,54], 4))