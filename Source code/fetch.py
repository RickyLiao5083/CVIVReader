import csv
import numpy as np


def fetch(path, name, XdataColumn, YdataColumn):
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
        Xbegin = matrix[0, 1].astype(float)
        X = matrix[:, XdataColumn].astype(float)
        step = X[1] - X[0] if len(X) > 1 else 1
        Xmax = max(X)
        Xmin = min(X)
        Xend = Xmax if Xbegin == Xmin else Xmin
        period = round((Xend - Xbegin) / step + 1)
        X1 = matrix[0:period, XdataColumn]
        direction = 1 if (len(X) / len(X1)) % 2 == 0 and X[0] == X[2 * period - 1] and X[period - 1] == X[period] else 0

        if direction:  # Double
            N = int(len(X) / period / 2)
            X2 = matrix[period:period * 2, XdataColumn]
            result = [None] * (N * 2 + 2)
            result[0] = X1
            result[N + 1] = X2
            for i in range(0, N):
                result[i + 1] = matrix[period * 2 * i:period * 2 * i + period, YdataColumn]
                result[i + N + 2] = matrix[period * (2 * i + 1):period * (2 * i + 1) + period, YdataColumn]
        else:  # Single
            N = round(len(X) / period) if len(X) % period == 0 else 1  # 1 is for the non-uniform step like I-t
            result = [None] * (N + 1)
            if N == 1:
                result[0] = matrix[:, XdataColumn]
                result[1] = matrix[:, YdataColumn]
            else:
                result[0] = X1
                for i in range(0, N):
                    result[i + 1] = matrix[period * i:period * i + period, YdataColumn]

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
