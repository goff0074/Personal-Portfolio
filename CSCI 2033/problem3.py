import numpy as np
from numpy.linalg import norm
# fix  seed  for  reproducible  result. Please  do not  change  the  seed
rng = np.random.default_rng(20232033)
n = 300
A = rng.random((n,n))
b = rng.random((n,1))
#print("A = {}; \n b = {}".format(A,b))

def gauss_elim_v0(A,b,print_flag=True):
  # check whether the calculation is valid
  assert A.shape[0] == A.shape[1],"A must be square!" # Make sure A is square
  assert A.shape[0] == b.shape[0],"Input dimension doesn't match!" # Make sure dimmension matches
  assert b.shape[1] == 1,"b is not a vector!" # Make sure b is a vector

  n = A.shape[0]
  ###### YOUR CODE STARTS HERE ######
  # U = ... # Using A and b to generate the augmented matrix
  #   print your augmented matrix each step while it is modified
  #   you could symply use print(U) to print for each step
  U = np.concatenate((A, b), axis = 1)
  for k in range(0, n-1):
    for j in range(k + 1, n):
      lambda_value = U[j, k] / U[k, k]
      U[[j],:] = U[[j], :] - lambda_value * U[[k], :]
    if (print_flag):
      print(U)
      print("==============================================")
  ###################################
  return U

A_example1 = np.array([[1,-1,1],[2,-1,3],[2,0,3]],dtype=np.float64)
b_example1 = np.array([[1],[4],[5]],dtype=np.float64)

U_example1 = gauss_elim_v0(A_example1,b_example1,True)

print(U_example1)

# this function will check whether the matrix is in row echelon form
def check_row_echelon(U):
  eps = np.finfo(np.float32).eps # updated here!!!
  # Previous version: eps = np.finfo(np.float64).eps
  test = np.tril(U,-1)
  #print(test) np.abs(test)
  return np.all(abs(test)<=eps)

def back_subs(U,print_flag = True):
  assert  check_row_echelon(U),"U must be in row echelon form"

  n = U.shape[0]
  x = np.zeros((n,1))
  ###### YOUR CODE STARTS HERE ######
  # print x[i] in the loop
  c = U[:, [-1]]
  D = U[:,:-1]
  x[n-1] = c[n-1]/D[n-1, n-1]
  for i in range(n-2, -1, -1):
    x[i] = (c[i] - np.sum(D[i, i + 1:] * x[i + 1:, 0])) / D[i, i]
    if(print_flag):
        print(x[i])
  ###################################
  return x

x_example1 = back_subs(U_example1,True)
print(x_example1)

def my_solver_v0(A,b):
  U = gauss_elim_v0(A,b,False)
  ###### YOUR CODE STARTS HERE ######
  x = back_subs(U,False)
  ###################################

  return x

###### YOUR CODE STARTS HERE ######

x1 = my_solver_v0(A,b)
dist = np.linalg.norm(np.matmul(A, x1) - b) / np.linalg.norm(A)


###################################
print("The relative error ||Ax1-b||/||A|| = {}".format(dist))

###### YOUR CODE STARTS HERE ######

x2 = np.linalg.solve(A, b)
dist = np.linalg.norm(x1 - x2) / np.linalg.norm(x2) 


###################################
print("The relative distance ||x1-x2||/||x2|| = {}".format(dist))


def gauss_elim_v1(A,b,print_flag):
  # check whether the calculation is valid
  assert A.shape[0] == A.shape[1],"A must be square" # Make sure A is square
  assert A.shape[0] == b.shape[0],"Input dimension doesn't match" # Make sure dimmension matches
  assert b.shape[1] == 1,"b is not a vector" # Make sure b is a vector

  n = A.shape[0]
  U = np.concatenate((A, b), axis=1)
  ###### YOUR CODE STARTS HERE ######
  # U = ... # Using A and b to generate the augmented matrix
  #   print your augmented matrix each step while it is modified
  #   you could symply use print(U) to print for each step
  for k in range(n-1):
    max_value = np.argmax(np.abs(U[k:, k])) + k
    U[[k, max_value], :] = U[[max_value, k], :]
    if print_flag:
            print(U)
            print("==============================================")
    for j in range(k+1, n):
      lambda_value = U[j, k] / U[k,k]
      U[[j], :] = U[[j], :] - lambda_value * U[[k], :]
      if (print_flag):
        print(U)
        print("==============================================")
  ###################################
  return U

def my_solver_v1(A,b):
  U = gauss_elim_v1(A,b,False)
  ###### YOUR CODE STARTS HERE ######
  x = back_subs(U,False) # reuse your back_substitution function here
  ###################################

  return x

A_example2 = np.array([[0,1,1],[2,6,4],[1,1,4]],dtype=np.float64)
b_example2 = np.array([[-1],[6],[9]],dtype=np.float64)

U_example2 = gauss_elim_v1(A_example2,b_example2,True)

print(U_example2)

###### YOUR CODE STARTS HERE ######

x1 = my_solver_v1(A,b)
dist = np.linalg.norm(np.matmul(A, x1) - b) / np.linalg.norm(A)


###################################
print("The relative error ||Ax1-b||/||A|| = {}".format(dist))

###### YOUR CODE STARTS HERE ######

x2 = np.linalg.solve(A, b)
dist = np.linalg.norm(x1 - x2) / np.linalg.norm(x2)


###################################
print("The relative distance ||x1-x2||/||x2|| = {}".format(dist))