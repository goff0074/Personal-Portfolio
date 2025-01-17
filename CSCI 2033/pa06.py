import random, timeit

# def mystery1(vals):
#     diff = 0
#     for i in range(len(vals)):
#         for j in range(len(vals)):
#             if(vals[i] - vals[j] > diff):
#                 diff = vals[i] - vals[j]
#     return diff

def mystery1(vals):
    minimumVal = vals[0] # set the first minimum value to the first index in the values
    maxDifference = vals[1] - vals[0] # Initialize the max difference as the second index and the first
    for value in vals[1:]: # loop through the values starting at the 2nd index
        minimumVal = min(minimumVal, value) # find a new minimum value as we move indexes
        maxDifference = max(maxDifference, value - minimumVal) # check to see if you find a new max difference using the new index values
    return maxDifference


# def mystery2(filename):
#     time = {}
#     with open(filename) as fp:
#         text = fp.read()
#         for ltr in text:
#             time[ltr] = text.count(ltr)
#     return time

def mystery2(filename):
    time = {} # Create dictionary
    with open(filename) as fp:
        text = fp.read() 
        for ltr in text: # Loop through each letter in the file
            if ltr in time:
                time[ltr] += 1 # If the letter already occupies a spot in the dictionary, add one to its count value
            else:
                time[ltr] = 1 # if the letter isnt already in the dictionary, add it, and set its count value to 1
    return time
    

# def mystery3(filename):
#     storage = []
#     with open(filename) as fp:
#         for line in fp:
#             items = line.split()
#             name = items[0]
#             time = int(items[1])
#             if time >= len(storage): #Need more spots in storage
#                 x = time - len(storage) + 1
#                 extend = ['']*x #Makes a list of x empty strings
#                 storage = storage + extend
#             storage[time] = name
#     sort_list = []
#     for spot in storage:
#         if spot != '': #Ignore empty spots
#             sort_list.append(spot)
#     return sort_list

def mystery3(filename):
    storage = {}
    with open(filename) as fp:
        for line in fp:
            items = line.split()
            name = items[0]
            time = int(items[1]) # open the file, split the lines, take the first index as the name, the second as the value
            storage[time] = name # add the name and its correct time value to the dictionary
        sorted_indexes = sorted(storage.keys()) # sort the keys, return the list of these sorted keys
        sort_list = [storage[time] for time in sorted_indexes] #iterate over the sorted indexes and find the responding name, with the names sorted by value in ascending order
    return sort_list

if __name__ == '__main__':
    lst = [random.randint(0, 9999999) for i in range(1000)]
    time1 = timeit.timeit('mystery1(lst)', globals=globals(), number = 10)
    out = mystery1(lst)
    print("mystery1(lst) output:", out)
    print("mystery1(lst) runtime:", time1, "seconds")
    print('\n------------------\n')
    time2 = timeit.timeit('mystery2("wizard.txt")', globals=globals(), number = 10)
    out = mystery2('wizard.txt')
    print("mystery2('wizard.txt') output:", out)
    print("mystery2('wizard.txt') runtime:", time2, "seconds")
    print('\n------------------\n')
    time3 = timeit.timeit('mystery3("screentime_ms.txt")', globals=globals(), number = 10)
    out = mystery3("screentime_ms.txt")
    print("mystery3('screentime_ms.txt') output:", out)
    print("mystery3('screentime_ms.txt') runtime:", time3, "seconds")
