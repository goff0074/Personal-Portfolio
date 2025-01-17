import numpy as np
# fix  seed  for  reproducible  result. Please  do not  change  the  seed
rng = np.random.default_rng(20232033)
A = rng.random((100 ,100))
B = rng.random((100 ,200))
C = rng.random((100 ,200))
D = rng.random((100 ,100))
u = rng.random((100 ,1))
v = rng.random((200 ,1))

def mat_pow(A,p):
  # check input
  assert A.shape[0] == A.shape[1], "Matrix input needs to be square!"
  assert p > 0, "p should be a positive integer!"
  assert isinstance(p, int), "p should have the data type of integer!"

  ###### YOUR CODE STARTS HERE ######
  Ap = np.eye(A.shape[0])
  for _ in range(p):
    Ap = np.matmul(Ap, A)

  ###################################
  return Ap

solution_5_b_1 = np.matmul(mat_pow(A, 6), mat_pow(A, 8))


solution_5_b_2 = mat_pow(A, 6+8)

relative_dist_5_b = np.linalg.norm(solution_5_b_1 - solution_5_b_2) / np.linalg.norm(solution_5_b_1)

###################################
print(solution_5_b_1)
print()
print(solution_5_b_2)
print()
print("relative distance between these two matrices is: ")
print(relative_dist_5_b)

solution_5_c_1 = mat_pow(mat_pow(A, 6), 8)# put (A^6)^8 here

solution_5_c_2 = mat_pow(A, 6 * 8) # put A^(6*8) here

relative_dist_5_c = np.linalg.norm(solution_5_c_1 - solution_5_c_2) / np.linalg.norm(solution_5_c_1)

###################################
print(solution_5_c_1)
print()
print(solution_5_c_2)
print()
print("relative distance between these two matrices is: ")
print(relative_dist_5_c)
print()

solution_6_a_1 = np.linalg.inv(np.matmul(A, D)) # put (AD)^(-1) here

solution_6_a_2 = np.matmul(np.linalg.inv(D), np.linalg.inv(A)) # put (D^(-1))(A^(-1)) here

relative_dist_6_a = np.linalg.norm(solution_6_a_1 - solution_6_a_2) / np.linalg.norm(solution_6_a_1)

###################################
print(solution_6_a_1)
print()
print(solution_6_a_2)
print()
print("relative distance between these two matrices is: ")
print(relative_dist_6_a)
print()

print("Problem 2.6(c)")
###### YOUR CODE STARTS HERE ######

solution_6_c_1 = np.matmul(A, B).transpose() # put (AB)^(T) here (Updated)

solution_6_c_2 = np.matmul(B.transpose(), A.transpose()) # put (B^T)(A^T) here

relative_dist_6_c = np.linalg.norm(solution_6_c_1 - solution_6_c_2) / np.linalg.norm(solution_6_c_1)

###################################
print(solution_6_c_1)
print()
print(solution_6_c_2)
print()
print("relative distance between these two matrices is: ")
print(relative_dist_6_c)