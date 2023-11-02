import csv
import numpy as np


#CVorIV = 1 => C-V, CVorIV = 0 => I-V. direction = 1 => double, direction = 0 => single.
def fetch(path, name, CVorIV, direction):
    rowbegin = 264 if CVorIV else 259
    file = path + name
    try:
        with open(file, "r", newline='', encoding="utf-8") as csvfile:
            dataframe = csv.reader(csvfile)
            count = 0
            table = []
            for row in dataframe:
                if count >= rowbegin - 1:
                    table.append(row)
                count += 1
        matrix = np.array(table)
        Vbegin = matrix[0, 1].astype(float)
        V = matrix[:, 1].astype(float)
        """
        for vi in V:
            print(vi, type(vi))
        """
        Vmax = max(V)
        Vmin = min(V)
        if CVorIV:                     #C-V
            if Vbegin == Vmin:
                Vend = Vmax
                step = 0.05
            else:
                Vend = Vmin
                step = -0.05
            period = int((Vend - Vbegin) / step + 1)
            V1 = matrix[0:period, 1].astype(float)
            if direction:
                N = int(len(V) / period / 2)
                V2 = matrix[period:period * 2, 1].astype(float)
                result = [None] * (N * 2 + 2)
                result[0] = V1
                result[N + 1] = V2
                for i in range(0, N):
                    result[i + 1] = matrix[period * 2 * i:period * 2 * i + period, 3].astype(float)
                    result[i + N + 2] = matrix[period * (2 * i + 1):period * (2 * i + 1) + period, 3].astype(float)
            else:
                N = int(len(V) / period)
                result = [None] * (N + 1)
                result[0] = V1
                for i in range(0, N):
                    result[i + 1] = matrix[period * i:period * i + period, 3].astype(float)
        else:                     #I-V
            if Vbegin == Vmin:
                Vend = Vmax
                step = 0.02
            else:
                Vend = Vmin
                step = -0.02
            period = int((Vend - Vbegin) / step + 1)
            V1 = matrix[0:period, 1].astype(float)
            V2 = matrix[period:, 1].astype(float)
            result = [None] * 4
            result[0] = V1
            result[2] = V2
            result[1] = matrix[0:period, 3].astype(float)
            result[3] = matrix[period:, 3].astype(float)
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