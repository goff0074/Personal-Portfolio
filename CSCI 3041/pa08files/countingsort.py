def counting_sort(A, k):
    n = len(A)
    B = [0] * n
    C = [0] * (k + 1)

    # Initialize count array
    for i in range(n):
        C[A[i]] += 1

    # Modify count array to store the position of each element in the sorted output
    for i in range(1, k + 1):
        C[i] += C[i - 1]

    # Build the sorted array
    for j in range(n - 1, -1, -1):
        B[C[A[j]] - 1] = A[j]
        C[A[j]] -= 1

    return B

# Example usage
A = [4, 2, 2, 8, 3, 3, 1]
k = max(A)
sorted_array = counting_sort(A, k)
print(sorted_array)
