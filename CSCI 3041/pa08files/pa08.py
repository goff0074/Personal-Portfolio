import traceback
#SortStudents function. Takes as input a list of Student objects,
#sorted alphabetically by name (last, then first), and outputs a list of
#Student objects, sorted by the following priority:
#house, then year, then name.
def SortStudents(studentList):
    #TODO: Implement this function
    maxYear = max(student.year for student in studentList) #find the max year
    maxHouse = 4
    studentList = CountingSort(studentList, len(studentList), maxYear, extractYear) #sort based off the years
    studentList = CountingSort(studentList, len(studentList), maxHouse, extractHouse) #sort based off house value
    return studentList

def CountingSort(A, n, k, wantedKey): #helper counting sort funtion
    B = [0] * n #output array, is the length of the A array
    C = [0] * (k + 1) #counting array, temporary
    for i in range(n):
        C[wantedKey(A[i])] += 1 #count occurances of each element in the array
    for i in range(1, k + 1):
        C[i] += C[i -1] #alter counting array to help show positions of element in the end sorted array
    for j in range(n-1, -1, -1):
        B[C[wantedKey(A[j])] - 1] = A[j]
        C[wantedKey(A[j])] -= 1 #build the sorted output array
    return B
def extractYear(student):
    return student.year #get the year from a student object
def extractHouse(student):
    return houseToInt(student.house) #get the house from a student object
def houseToInt(house):
    if house == "Eagletalon":
        houseInt = 1 #if the house is eagletalon, assign it to 1
    elif house == "Lannister":
        houseInt = 2 # if the house is lannister, assign it to 2
    elif house == "Pufflehuff":
        houseInt = 3 #if the house is pufflehuff, assign it to 3
    elif house == "SNAKES":
        houseInt = 4 #if the house is snakes, assign it to 4
    return houseInt



#  DO NOT EDIT BELOW THIS LINE

#Student class
#Each task has three instance variables:
#   self.name is a string representing the name of the student
#   self.house is a string representing which house the student is in
#   self.year is an integer representing what year the student is
class Student:
    def __init__(self,csvstring):
        csvdata = csvstring.split(",")
        self.name = csvdata[0]
        self.house = csvdata[1]
        self.year = int(csvdata[2])
    def __repr__(self):
        return "\n{:25}: {:12} {}".format(self.name,self.house,self.year)
    def __eq__(self,other):
        return type(self) == type(other) and \
               self.name == other.name and \
               self.house == other.house and \
               self.year == other.year

      



#Takes a string filename as an argument, and constructs a list
#  of Students from the information in the CSV file at filename
def getStudentList(filename):
    fp = open(filename)
    fp.readline()
    studentList = []
    for line in fp:
        studentList.append(Student(line))
    return studentList


if __name__ == '__main__':
    tests = ['roster1.csv','roster2.csv','roster3.csv','roster4.csv',
             'roster5.csv','roster6.csv']
    correct = ['roster1sorted.csv','roster2sorted.csv',
               'roster3sorted.csv','roster4sorted.csv',
               'roster5sorted.csv','roster6sorted.csv']


    #Run test cases, check whether sorted list correct
    count = 0

    try:
        for i in range(len(tests)):
            print("\n---------------------------------------\n")
            print("TEST #",i+1)
            print("Reading student data from:",tests[i])
            roster = getStudentList(tests[i])
            print("Reading sorted student data from",correct[i])
            rosterSorted = getStudentList(correct[i])
            print("Running: SortStudents() on data list\n")
            output = SortStudents(roster)
            print("Expected:",rosterSorted,"\n\nGot:",output)
            assert len(output) == len(rosterSorted), "Output list length "\
                   +str(len(output))+\
                      ", but should be "+str(len(rosterSorted))
            for j in range(len(output)):
                assert output[j] == rosterSorted[j],"Student #"\
                           +str(j+1)+" incorrect: "+\
                        str(output[j])+" \nshould be "+str(rosterSorted[j])
            print("Test Passed!\n")
            count += 1
    except AssertionError as e:
        print("\nFAIL: ",e)

    except Exception:
        print("\nFAIL: ",traceback.format_exc())

    #Check for less than or greater than signs anywhere in the file
    cursed = False
    with open(__file__) as f:
        source = f.read()
        for ch in source:
            if ord(ch) == 60:
                print("Less than sign detected: Curse activated!")
                count = 0
                cursed = True
            if ord(ch) == 62:
                print("Greater than sign detected: Curse activated!")
                count = 0
                cursed = True

    print()
    if cursed:
        print("You are now a newt.  Don't worry, you'll get better.")
    print(count,"out of",len(tests),"tests passed.")


