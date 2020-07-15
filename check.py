
def check():
    output = open('output.txt', 'r')
    o_lines = output.readlines()

    solution = open('sudokus_finish.txt')
    s_lines = solution.readlines()
    count = 0
    for i in range(400):
        if s_lines[i] != o_lines[i]:
            print("Shit", i, s_lines[i], o_lines[i])
            return
        else: count += 1   

    return count

inputfile = 'output.txt'
import numpy as np
def readme(inputfile):
    input = open(inputfile, 'r')
    data = [float(x) for x in input.readlines()]
    readme = open('README.txt','x')
    minimum = min(data)
    maximum = max(data)
    std = np.std(data)
    mean = np.mean(data)

    readme.write("minimum: " + str(minimum))
    readme.write('\n')
    readme.write("maximum: " + str(maximum))
    readme.write('\n')
    readme.write("mean: " + str(mean))
    readme.write('\n')
    readme.write("std: " + str(std))
    readme.write('\n')
    return 'success'


readme(inputfile)
