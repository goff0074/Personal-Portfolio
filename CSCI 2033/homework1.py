import numpy as np
# fix  seed  for  reproducible  result. Please  do not  change  the  seed
rng = np.random.default_rng(20232033)
u = rng.random((10000 ,1))
v = rng.random((10000 ,1))
w = rng.random((10000 ,1))

###### YOUR CODE STARTS HERE ######

solution_1_a = v[2022]

solution_1_b = v[2022: 2033]

solution_1_c = np.concatenate((v[:30], w[-100:]))

###################################
print(solution_1_a)
print()
print(solution_1_b)
print()
print(solution_1_c)

###### YOUR CODE STARTS HERE ######
solution_2_a = u + v + w

solution_2_b = 2*u + 3*v + 3*w

###################################
print(solution_2_a)
print()
print(solution_2_b)

###### YOUR CODE STARTS HERE ######

solution_3_a = np.inner(u.flatten(), u.flatten())

solution_3_b = np.inner((u-2*v).flatten(), w.flatten())

solution_3_c = np.inner((3*u).flatten(), (2*v+w).flatten())

###################################
print(solution_3_a)
print()
print(solution_3_b)
print()
print(solution_3_c)

###### YOUR CODE STARTS HERE ######

solution_4_a = np.linalg.norm(u)

solution_4_b = np.linalg.norm(v + 3 * w)
###################################
print(solution_4_a)
print()
print(solution_4_b)