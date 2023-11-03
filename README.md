# CVIVReader
This APP can fetch the C-V and I-V .csv files.

Only C-V and I-V are accepted.

The executable file (CVIVReadeer.exe) can be downloaded from: https://drive.google.com/file/d/1J-RBEpjEOv7zrOQxgOkmAxZUmwAF4IzQ/view?usp=sharing.

You can download the source code and customize it by yourself.

Note that this APP reads the .csv by regarding column B as voltage and column D as capacitance for the C-V files, and column B as voltage and column D as abs(I) for the I-V files. If it is not this case, the results would be wrong.

The output format is:

|  V1  |  C@f1  |  C@f2  |   ...   |  C@fi  |                                                                  (C-V single)

|  V1  |  C@f1  |  C@f2  |   ...   |  C@fi  |  V2  |  C@f1'  |  C@f2'  |   ...   |  C@fi'  |                   (C-V double)

|  V1  | abs(I) |   V2   | abs(I)' |                                                                           (I-V double)
