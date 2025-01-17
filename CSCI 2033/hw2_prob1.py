# import numpy as np

# #Initializing matrix for test case a) in Problem 1.1
# A1_square = np.array([[1, 0, 1, 0], [0, 0, 0, 0], [0, 0, 3, 1], [0, 0, 3, 0]], dtype=np.float64)

# #Initializing matrix for test case b) in Problem 1.1
# A2_square = np.array([[0, 1, 1], [2, 6, 4], [1, 1, 4]], dtype=np.float64)

# # def GE_square(A, print_flag):
# #   R = A.copy()
# #   n = R.shape[0]
# #   pvt_list = []
# #   k = 0
# #   eps = np.finfo(np.float32).eps
# #   #################### YOUR CODE STARTS HERE ####################
# #   for r in range(n):
# #     while np.amax(np.abs(R[r:n, k])) <= eps:
# #       k += 1
# #       if k == n:
# #         if print_flag:
# #                 print("Final R: ")
# #                 print(R)
# #                 print("Pivot list: ", pvt_list)
# #         return R, pvt_list
# #     i = np.argmax(np.abs(R[r:n, k])) + r
# #     R[[r, i], :] = R[[i, r], :]
# #     pvt_list.append(k)
# #     print("Current R: ")
# #     print(R)
# #     print("Pivot list: ", pvt_list)
# #     for j in range(r+1, n):
# #       lambda_val = R[j, k] / R[r, k]
# #       R[[j], :] -= lambda_val * R[[r],:]
# #     print("Current R: ")
# #     print(R)
# #     print("Pivot list: ", pvt_list)
# #   print("Final R")
# #   print(R)
# #   print("Pivot list: ", pvt_list)
# #   ###############################################################
# #   return R, pvt_list

# # R, pvt_idx_list = GE_square(A1_square, True)
# # # print out the row echelon form
# # print("row echelon form of A1_square:")
# # print(R)
# # # print out the indices of pivot values
# # print("Indices of pivot values:")
# # print(pvt_idx_list)

# # R, pvt_idx_list = GE_square(A2_square, True)
# # # print out the row echelon form
# # print("row echelon form of A2_square:")
# # print(R)
# # # print out the indices of pivot values
# # print("Indices of pivot values:")
# # print(pvt_idx_list)

# #Initializing matrix for test case a) in Problem 1.2
# A1_rect = np.array([[1, 2, 2, -1], [4, 8, 9, 6], [0, 3, 2, 9]], dtype=np.float64)

# #Initializing matrix for test case b) in Problem 1.2
# A2_rect = np.array([[1, 2, 3, 1, 2], [0, 4, 6, 0, 1], [2, 4, 8, 0, 0], [0, 1, 2, 0, 9]], dtype=np.float64)

# def GE_rectangular(A, print_flag):
#   R = A.copy()
#   n = R.shape[0] #number of rows in A
#   m = R.shape[1] #number of columns in A
#   pvt_list = []
#   k = 0
#   eps = np.finfo(np.float32).eps
#   #################### YOUR CODE STARTS HERE ####################
#   for r in range(n):
#     while np.amax(np.abs(R[r:n, k])) <= eps:
#       k += 1
#       if k == m:
#         if print_flag:
#             print("Final R:")
#             print(R)
#             print("Indices of the pivots:", pvt_list)
#         return R, pvt_list
#     i = np.argmax(np.abs(R[r:n, k])) + r
#     R[[r, i], :] = R[[i, r], :]
#     pvt_list.append(k)
#     print("Current R: ")
#     print(R)
#     print("Indices of the pivots: ", pvt_list)
#     for j in range(r+1, n):
#       lambda_val = R[j, k] / R[r, k]
#       R[[j], :] -= lambda_val * R[[r],:]
#     print("Current R ")
#     print(R)
#     print("Indices of the pivots: ", pvt_list)
#   print("Final R")
#   print(R)
#   print("Indices of the pivots: ", pvt_list)
#   ###############################################################
#   return R, pvt_list

# R, pvt_idx_list = GE_rectangular(A1_rect, True)
# # print out the row echelon form
# print("row echelon form of A1_rect:")
# print(R)
# # print out the indices of pivot values
# print("Indices of pivot values:")
# print(pvt_idx_list)

# R, pvt_idx_list = GE_rectangular(A2_rect, True)
# # print out the row echelon form
# print("row echelon form of A2_rect:")
# print(R)
# # print out the indices of pivot values
# print("Indices of pivot values:")
# print(pvt_idx_list)


# X = np.array([[1, 2, 4, 1], [3, 6, 12, 3], [4, 8, 16, 4]], dtype=np.float64)
# Y = np.array([[1, 2, 4, 1], [3, 6, 12, 3], [4, 8, 16, 6]], dtype=np.float64)
# Z = np.array([[1, 2, 4, 1], [3, 5, 12, 3], [4, 8, 16, 6]], dtype=np.float64)
# please use GE_rectangular to generate the reduced row echelon form of matrices X, Y, Z
# And then check the rank of each matrix visually
############################# YOUR CODE STARTS HERE #############################
# R_X, pvt_list_X = GE_rectangular(X, True)
# R_Y, pvt_list_Y = GE_rectangular(Y, True)
# R_Z, pvt_list_Z = GE_rectangular(Z, True)
# X_rank = len(pvt_list_X)
# Y_rank = len(pvt_list_Y)
# Z_rank = len(pvt_list_Z)
# print("Rank of X: ", X_rank)
# print("Rank of Y: ", Y_rank)
# print("Rank of Z: ", Z_rank)
# from numpy.linalg import matrix_rank
# r_X = matrix_rank(X)
# r_Y = matrix_rank(Y)
# r_Z = matrix_rank(Z)
# print("Rank of X: ", r_X)
# print("Rank of Y: ", r_Y)
# print("Rank of Z: ", r_Z)
################################################################################

# import numpy as np
# # 

# A = np.array([[1, 2, 0], [0, 1, 1], [1, 0, 1]], dtype=np.float64)

# def QR(A):
#   #################### YOUR CODE STARTS HERE #################################
#   n = A.shape[1]
#   m = A.shape[0]
#   Q = np.zeros((m, n), dtype=np.float64)
#   R = np.zeros((n, n), dtype=np.float64)

#   for i in range(n):
#     v = A[:, i]
#     for k in range(i):
#       R[k, i] = np.dot(Q[:, k], v)
#       v -= R[k, i] * Q[:, k]
#     R[i, i] = np.linalg.norm(v)
#     Q[:, i] = v / R[i, i]
#   #############################################################################
#   return Q, R

# Q, R = QR(A)

# print("QR Factorization:")
# print(Q)
# print(R) # Please check your anwsers with the example of problem 2.3 shown in the pdf file

# B = np.array([[0.488894, 0.888396, 0.325191, 0.319207],
#               [1.03469, -1.14707, -0.754928, 0.312859],
#               [0.726885, -1.06887, 1.3703, -0.86488],
#               [-0.303441, -0.809499, -1.71152, -0.0300513],
#               [0.293871, -2.94428, -0.102242, -0.164879],
#               [-0.787283, 1.43838, -0.241447, 0.627707]], dtype=np.float64)

# Q_1, R_1 =QR(B)


# print("QR Factorization:")
# print(Q_1) # Print out Q_1, R_1 matrix out and you can check Q_1^T@Q_1 = I
# print(Q_1.T @ Q_1)
# print(R_1) # R_1 should be a up-triangular matrix

import numpy as np
import matplotlib.pyplot as plt
# fix  seed  for  reproducible  result. Please  do not  change  the  seed
np.random.seed(2022)
A = np.random.randn(20, 20)
x = np.random.randn(20,1)
b = A@x


def QR(A): # please directly copy QR function from Problem 2 here.
  #################### YOUR CODE STARTS HERE #################################
  n = A.shape[1]
  m = A.shape[0]
  Q = np.zeros((m, n), dtype=np.float64)
  R = np.zeros((n, n), dtype=np.float64)

  for i in range(n):
    v = np.copy(A[:, i])
    for k in range(i):
      R[k, i] = np.dot(Q[:, k], v)
      v -= R[k, i] * Q[:, k]
    R[i, i] = np.linalg.norm(v)
    Q[:, i] = v / R[i, i]
  #############################################################################
  return Q, R



def backSubstitute(R, b_Q):
  ####################### YOUR CODE STARTS HERE ###############################
  n = R.shape[0]
  x = np.zeros(n)
  for i in range(n - 1, -1, -1):
    x[i] = (b_Q[i] - (np.sum(R[i, i + 1:] * x[i + 1:]))) / R[i, i]
  #############################################################################
  return x


def mySolver(A, b):
  Q, R = QR(A)
  b_Q = Q.T@b
  x = backSubstitute(R, b_Q)
  return x

def relative_diff(x, x_hat):
  ######################### YOUR CODE STARTS HERE ##############################
  err = np.linalg.norm(x - x_hat) / np.linalg.norm(x)  # Please use formula(23)
  ##############################################################################
  return err

x_hat = mySolver(A, b)
print("The relative error:")
print(relative_diff(x, x_hat))

b_consumption = np.array([
        63122, 60953, 59551, 58785, 59795, 60083, 61819, 63107, 64978, 66090,
        66541, 67186, 67396, 67619, 69006, 70258, 71880, 73597, 74274, 75975,
        76928, 77732, 78457, 80089, 83063, 84558, 85566, 86724, 86046, 84972,
        88157, 89105, 90340, 91195 ], dtype=np.float64)

n = len(b_consumption)
############################# YOUR CODE STARTS HERE #######################
year = np.arange(1980, 2014)
A_consumption = np.hstack((year.reshape(-1, 1), np.zeros((n, 1)) + 1)) # Generate the matrix A according to formula (30)
  #  Hint: numpy.vstack, numpy.hstack, and numpy.zeros may be useful for you;
  #        check numpy doc (particularly their examples) to see how to use them
x_hat_consumption  = mySolver(A_consumption,b_consumption)
###########################################################################

# plot the line fitting
plt.figure()
plt.scatter(np.arange(1980,2014), b_consumption)
plt.plot(np.arange(1980,2014), A_consumption @ x_hat_consumption, 'r')
plt.show()