import numpy as np
import matplotlib.pyplot as plt

pos_M = np.array([[-10, -8, -9, -8, -7, -6, -5, -4, -5, -3, -4, -3, -2, -1, 0, -1, 1,0, 1, 2, 3, 4, 3, 5, 4, 5, 6, 7, 8, 9, 8, 10],
                  [-1, -1, -1, 0, 1, 2, 3, 4, 4, 4, 4, 3, 2, 1, 0, 0, 0, 0, 1, 2, 3, 4, 4, 4, 4, 3, 2, 1, 0, -1, -1, -1]])
# each column corresponding to a data point

print("Shape of pos_M is {}".format(pos_M.shape))

def plot_shape(P):
  # P is a 2-by-N matrix for
  plt.figure()
  plt.plot(P[0], P[1])
  ax = plt.gca()
  #ax.axes.xaxis.set_visible(False)
  #ax.axes.yaxis.set_visible(False)
  ax.set_aspect('equal')
  plt.show()


plot_shape(pos_M)

def plot_resulting_shape(pos_M_result, pos_M):
  plt.figure()
  plt.plot(pos_M[0], pos_M[1])
  plt.plot(pos_M_result[0], pos_M_result[1])
  ax = plt.gca()
#   ax.axes.xaxis.set_visible(False)
#   ax.axes.yaxis.set_visible(False)
  ax.set_aspect('equal') # Updated here
  plt.show()

# Scaling
# Please scale the shape so that it has
# twice the current width in the x direction
# half the current height in the y direction
print("Scaling result:")
################Your codes start here#################
A_scale = np.array([[2, 0], [0, 0.5]])        # transformation matrix itself
pos_M_scale = np.dot(A_scale, pos_M)        # resulting shape
plot_resulting_shape(pos_M_scale, pos_M)    # plotting
#######################################################

# Rotation
# Please rotate the shape counterclockwise by 60 degrees
print("Rotation result:")
################Your codes start here#################
A_rotate = np.array([[np.cos(np.radians(60)), -np.sin(np.radians(60))],
                     [np.sin(np.radians(60)), np.cos(np.radians(60))]])
pos_M_rotate = np.dot(A_rotate, pos_M)
plot_resulting_shape(pos_M_rotate, pos_M)
#######################################################

# Translation
# Please translate the shape along x axis with length 10
# and along y axis with length 20
print("Translation result:")
################Your codes start here#################
A_translate = np.array([[10], [20]])
pos_M_translate = pos_M + A_translate
plot_resulting_shape(pos_M_translate, pos_M)
#######################################################

# Shearing 1
# Please shear the shape along the x-direction with a shearing factor 3
# and keep the shape along the y-direction
print("Shearing 1 result:")
################Your codes start here#################
A_shear_h = np.array([[1, 3], [0, 1]]) 
pos_M_shear_h = np.dot(A_shear_h, pos_M)
plot_resulting_shape(pos_M_shear_h, pos_M)
#######################################################

# Shearing 2
# Please shear the shape along the y-direction with a shearing factor 6
# and keep the shape along the x-direction
print("Shearing 2 result:")
################Your codes start here#################
A_shear_v = np.array([[1, 0], [6, 1]])
pos_M_shear_v = np.dot(A_shear_v, pos_M)
plot_resulting_shape(pos_M_shear_v, pos_M)
#######################################################

# # Sequence 1
# # Please do the following two things in sequence
# # 1. scale the shape so that it has
# #    * twice the current width in the x direction
# #    * half the current height in the y direction
# # 2. rotate the resulting shape counterclockwise by 60 degrees
# print("Sequence 1 result: ")
# ################Your codes start here#################
# A_seq1 = np.dot(A_scale, A_rotate)
# pos_M_seq1 = np.dot(A_seq1, pos_M)
# plot_resulting_shape(pos_M_seq1, pos_M)
# #######################################################

# # Sequence 2
# # Please do the following two things in sequence
# # 1. rotate the shape counterclockwise by 60 degrees
# # 2. scale the resulting shape so that it has
# #    * twice the current width in the x direction
# #    * half the current height in the y direction
# print("Sequence 2 result: ")
# ################Your codes start here#################
# A_seq2 = np.dot(A_rotate, A_scale)
# pos_M_seq2 = np.dot(A_seq2, pos_M)
# plot_resulting_shape(pos_M_seq2, pos_M)
# #######################################################

# # Sequence 3
# # Please do the following three things in sequence
# # 1. rotate the shape counterclockwise by 60 degrees
# # 2. shear the resulting shape along the y-direction with a shearing factor 6
# #      while keeping the shape along the x-direction
# # 3. scale the resulting shape so that it has
# #    * twice the current width in the x direction
# #    * half the current height in the y direction
print("Sequence 3 result: ")
# ################Your codes start here#################
A_seq3 = np.dot(A_scale, A_shear_v, A_rotate)
pos_M_seq3 = np.dot(A_seq3, pos_M)
plot_resulting_shape(pos_M_seq3, pos_M)
# #######################################################

# # Sequence 4
# # Please do the following three things in sequence
# # 1. shear the shape along the y-direction with a shearing factor 6
# #     while keeping the shape along the x-direction;
# # 2. rotate the shape counterclockwise by 60 degrees;
# # 3.  scale the resulting shape so that it has
# #     * twice the current width in the x direction
# #     * half the current height in the y direction
# print("Sequence 4 result: ")
# ################Your codes start here#################
A_seq4 = np.dot(A_shear_v, A_rotate, A_scale)
pos_M_seq4 = np.dot(A_seq4, pos_M)
plot_resulting_shape(pos_M_seq4, pos_M)
# #######################################################

# Please undo the rotation in Problem 1.1, i.e.,
# rotate the resulting shape pos_M_rotate there clockwise by 60 degrees
print("Undo Rotation Result: ")
################Your codes start here#################
A_inverse_rotate = np.linalg.inv(A_rotate)
pos_M_rotate_back = np.dot(A_inverse_rotate, pos_M_rotate)
plot_shape(pos_M_rotate_back)
#######################################################

# Please undo the shearing 1 of Problem 1.1, i.e.,
# tranform the pos_M_shear_h in Problem 1.1 back to pos_M (original shape)
print("Undo Shearing 1 Result: ")
################Your codes start here#################
A_inverse_shear_h = np.array([[1, -3], [0, 1]])
pos_M_shear_h_back = np.dot(A_inverse_shear_h, pos_M_shear_h)
plot_shape(pos_M_shear_h_back)
#######################################################

# # Please find the inverse of Sequence 1 in Problem 1.2
# # and apply it to pos_M_seq1
# print("Undo Sequence 1 Result: ")
# ################Your codes start here#################
# A_inverse_seq1 = np.linalg.inv(A_seq1)
# pos_M_seq1_back = np.dot(A_inverse_seq1, pos_M_seq1)
# plot_shape(pos_M_seq1_back)
# #######################################################

# # Please find the inverse of Sequence 2 in Problem 1.2
# # and apply it to pos_M_seq2
# print("Undo Sequence 2 Result: ")
# ################Your codes start here#################
# A_inverse_seq2 = np.linalg.inv(A_seq2)
# pos_M_seq2_back = np.dot(A_inverse_seq2, pos_M_seq2)
# plot_shape(pos_M_seq2_back)
# #######################################################

import numpy as np
import matplotlib.pyplot as plt

# Please construct the unnormalized  matrix based on the figure above
##################Your codes start here####################
# edges = [(0, 1), (0, 2), (0, 4), (0, 5), (1, 2), (1, 3), (1, 4), (1, 5), (2, 0), (2, 1), (2, 3), (3, 1), (3, 2), (3, 4), (4, 1), (4, 3), (5, 0), (5, 1)]
# G = np.zeros((6, 6))
# for edge in edges:
#     i, j = edge
#     G[i, j] = G[j, i] = 1
# ############################################################
# print("Matrix generated based on the network above is")
# print(G)

# # Please finish the normalization function here
# def normalize_graph(G):
#   ########################Your codes start here#################
#   column_sums = np.sum(G, axis = 0)
#   G_N = G / column_sums
#   ##############################################################
#   return G_N

# G_N = normalize_graph(G)
# print("The matrix after normalization is:")
# print(G_N)

# # implement algorithm 1 here:
# def find_importance_vector(G_N):
#   ####################Your codes start here ##########################
#   n = G_N.shape[0]
#   v_new = np.ones(n, dtype=np.float64) / n
#   v_old = np.copy(v_new)
#   while True:
#      v_new = np.dot(G_N, v_old)
#      v_new = v_new/np.sum(v_new)
#      if np.linalg.norm(v_old - v_new) / np.linalg.norm(v_old) <= 1e-6:
#         break
#      v_old = np.copy(v_new)
#   ##################################################################
#   return v_new

# v = find_importance_vector(G_N)  # v is the resulting vector from the loop.
# print("The important vector found is:\{}".format(v))
# # v should be close to
# # [0.2 ,0.25, 0.15, 0.15, 0.15, 0.1 ]^⊺ (Updated here)
# # there could exist some small difference between your result and this vector

# # Here you need to check the relative difference
# # between v you generated and v_hat
# v_hat = np.array(
#     [[0.2 ,0.25, 0.15, 0.15, 0.15, 0.1 ]] #Updated here
#     ).T
# print("Given v_hat is \n{}".format(v_hat))
# # ####################Your codes start here ##########################
# relative_dist = np.linalg.norm(v - v_hat) / np.linalg.norm(v)

# # ##################################################################
# print("The relative dist between v and v_hat is {}".format(relative_dist))

# # A new unnormalized matrix G is given:
# np.random.seed(2033)
# G_half = np.random.randint(0,2,(100, 100))
# G = (G_half+G_half.T)
# G = (np.sign(G))
# G = G.astype(np.float32)
# for i in range(100):
#   G[i, i] = 0.
# print(np.linalg.norm(G-G.T))
# print(G)

# # Step (a)
# # Compute the normalized matrix G_N based on G in Porblem 2.3: 100-by-100 matrix
# #######################Your codes start here ##########################
# G_N = normalize_graph(G)
# #########################################################################
# from numpy . linalg import eig
# # Step (b)
# # Use the built-in function np.linalg.eig to find the eigenvector corresponding
# # to the eigenvalue = 1
# ######################Your codes start here ##########################
# w, V = eig(G_N) # w is the 1-D array stores the eigenvalues and V[:, i] is the corresponding eigenvector  for eigenvalue = w[i].
# eigen_vector = V[:, np.argmax(np.abs(w))]

# #########################################################################
# print("Eigenvector found (while eigenvalue = 1) is: ")
# print(eigen_vector)

# # Step (c)
# # Fix the eigenvector correponding to the eigenvalue = 1 from V
# # according to the code hints in 2.3 (c) on Page 5 of pdf file
# #######################Your codes start here ##########################
# v_abs = np.abs(eigen_vector)
# v_PageRank = v_abs / np.sum(v_abs)

# #########################################################################
# print("Page Rank Vector is:")
# print(v_PageRank)

# # Use your find_importance_vector() to generate imp_vec
# # check relative distance between imp_vec and v_PageRank
# # should be close to 0 (non-negative values less than 1e-5 are acceptable)
# #######################Your codes start here ##########################

# imp_vec = find_importance_vector(G_N)
# relative_dist = np.linalg.norm(imp_vec - v_PageRank) / np.linalg.norm(imp_vec)

# #########################################################################
# print("Relative Dist between imp_vec and v_PageRank is {}".format(relative_dist))
# print("importance vector is \n{}".format(imp_vec))

# # Find the indices of the 5 most important webpages from v_PageRank
# # i.e., find the largest 5 elements from v_PageRank
# #######################Your codes start here ##########################
# ind_top_5 = np.argsort(v_PageRank)[-5:][::-1] # list of indices these 5 most important webpages

# #########################################################################
# print("Top 5 indices are: ")
# print(ind_top_5)