import csv
import numpy as np


def fetch(path, name, dataColumn):
    file = path + name
    try:
        with open(file, 'r', newline='', encoding="utf-8") as csvfile:
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
        step = V[1] - V[0] if len(V) > 1 else 1
        Vmax = max(V)
        Vmin = min(V)
        Vend = Vmax if Vbegin == Vmin else Vmin
        period = round((Vend - Vbegin) / step + 1)
        V1 = matrix[0:period, 1]
        direction = 1 if (len(V) / len(V1)) % 2 == 0 and V[0] == V[2 * period - 1] and V[period - 1] == V[period] else 0

        if direction:  # Double
            N = int(len(V) / period / 2)
            V2 = matrix[period:period * 2, 1]
            result = [None] * (N * 2 + 2)
            result[0] = V1
            result[N + 1] = V2
            for i in range(0, N):
                result[i + 1] = matrix[period * 2 * i:period * 2 * i + period, dataColumn]
                result[i + N + 2] = matrix[period * (2 * i + 1):period * (2 * i + 1) + period, dataColumn]
        else:  # Single
            N = round(len(V) / period) if len(V) % period == 0 else 1  # 1 is for the non-uniform step like I-t
            result = [None] * (N + 1)
            result[0] = V1
            for i in range(0, N):
                print(i)
                result[i + 1] = matrix[period * i:period * i + period, dataColumn]

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
