from input import Input
from solution import Solution

#read file and get file values
D = None
I = None
S = None
V = None
F = None
RoadName = {}
RoadLength = {}

with open('prishtina_instance.txt', 'r') as file:
    content = file.read()
    arrValues = []
    for line in file:
        arrValues = line.split()
        if(line.index == 0):
            D = arrValues[0]
            I = arrValues[1]
            S = arrValues[2]
            V = arrValues[3]
            F = arrValues[4]

        # okay but validate for the last 4 rows 
        index = str(arrValues[0]) + str(arrValues[1])
        RoadName[index] = arrValues[2] # to be checked
        RoadLength[index] = arrValues[3] # to be checked

# initialization of input list
input_data = Input()

input_data.D = D
input_data.I = I
input_data.S = S
input_data.V = V
input_data.F = F
input_data.RoadName = RoadName
input_data.RoadLength = RoadLength

# do smth with our input ...

# initialization of solution
solution_data = Solution()
# fill solution data somehow