def is_bst_sequence(seq):
    stack = []
    root = float('-inf')
    
    for value in seq:
        if value < root:
            return False
        while len(stack) > 0 and stack[-1] < value:
            root = stack.pop()
        stack.append(value)
    return True

# Test the function with the given sequences
sequences = [
    [2, 252, 401, 398, 330, 344, 397, 363],
    [924, 220, 911, 244, 898, 258, 362, 363],
    [925, 202, 911, 240, 912, 245, 363],
    [2, 399, 387, 219, 266, 382, 381, 278, 363],
    [935, 278, 347, 621, 299, 392, 358, 363]
]

for i in range(len(sequences)):
    print(f"Sequence {chr(ord('a') + i)}: {is_bst_sequence(sequences[i])}")
    
