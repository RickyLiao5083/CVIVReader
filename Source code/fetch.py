import csv
import numpy as np


#CVorIV = 1 => C-V, CVorIV = 0 => I-V. direction = 1 => double, direction = 0 => single.
def fetch(path, name, CVorIV, direction):
    file = path + name
    try:
        with open(file, "r", newline='', encoding="utf-8") as csvfile:
            dataframe = csv.reader(csvfile)
            table = []
            flag = 0
            for row in dataframe:
                if flag:
                    table.append(row)
                    continue
                if row[0] and 'DataName' in row[0]:
                    flag = 1
        matrix = np.array(table)
        Vbegin = matrix[0, 1].astype(float)
        V = matrix[:, 1].astype(float)
        step = V[1] - V[0]
        Vmax = max(V)
        Vmin = min(V)
        if CVorIV:                     #C-V
            Vend = Vmax if Vbegin == Vmin else Vmin
            period = round((Vend - Vbegin) / step + 1)
            V1 = matrix[0:period, 1]
            if direction:
                N = int(len(V) / period / 2)
                V2 = matrix[period:period * 2, 1]
                result = [None] * (N * 2 + 2)
                result[0] = V1
                result[N + 1] = V2
                for i in range(0, N):
                    result[i + 1] = matrix[period * 2 * i:period * 2 * i + period, 3]
                    result[i + N + 2] = matrix[period * (2 * i + 1):period * (2 * i + 1) + period, 3]
            else:
                N = int(len(V) / period)
                result = [None] * (N + 1)
                result[0] = V1
                for i in range(0, N):
                    result[i + 1] = matrix[period * i:period * i + period, 3]
        else:                     #I-V
            if Vbegin == Vmin:
                Vend = Vmax
                step = 0.02
            else:
                Vend = Vmin
                step = -0.02
            period = round((Vend - Vbegin) / step + 1)
            V1 = matrix[0:period, 1]
            V2 = matrix[period:, 1]
            result = [None] * 4
            result[0] = V1
            result[2] = V2
            result[1] = matrix[0:period, 3]
            result[3] = matrix[period:, 3]
        output = np.array(result)
        output = output.T
        newFile = path + 'output_' + name
        with open(newFile, 'w', newline='', encoding="utf-8") as csvfile2:
            writer = csv.writer(csvfile2)
            writer.writerows(output)
        csvfile.close()
        csvfile2.close()
        return 0
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        return 1