import numpy as np
from numpy import linalg as LA
# v_row = np.array([[3, 4]])
# print("row vector v_row is {}.".format(v_row))
# print("the shape of v_row is {}".format(v_row.shape))
# print()

# v_col = np.array([[3],[4]])
# print("column vector v_col is {}".format(v_col))
# print("the shape of v_col is {}".format(v_col.shape))
# print()

# m_example = np.array([[3,2],[1,4]])
# print("Check the difference with matrix")
# print("Example for matrix \n {}".format(m_example))

v = np.array([[3],[1],[2]])
w = np.array([[1],[2],[3],[4],[5],[6]])

# tmp = w[:3]
# print("first three elements of w is \n{}".format(tmp))

v1 = np.array([[1], [2], [3]])
v2 = np.array([[1], [5], [-1]])
tmp = v1 + v2
print("v1 + v2 = \n{}".format(tmp))
print()

tmp = v1 - v2
print(tmp)

tmp = 2 *v
print(tmp)