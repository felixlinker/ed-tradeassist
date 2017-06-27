from math import ceil


__TAB_WIDTH = 8

def write(matrix):
    tabs = [0 for i in range(len(matrix[0]))]
    for j in range(len(matrix[0])):
        for i in range(len(matrix)):
            tabs[j] =  max(tabs[j], ceil((len(str(matrix[i][j])) + 1) / __TAB_WIDTH))

    for line in matrix:
        line_str = ''
        for i in range(len(line)):
            cell = str(line[i])
            line_str += cell
            line_str += '\t' * ceil(
                ((tabs[i] * __TAB_WIDTH) - len(cell)) / __TAB_WIDTH
            )
        print(line_str)
