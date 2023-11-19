# CVIVReader
This APP can fetch all the CSV files exported from B1500A.

The executable file (B1500AReader.exe) can be downloaded from:

https://drive.google.com/drive/folders/1UpWr1kb85wR5M4W1d9ZGoHKqC7Pc54Ve?usp=sharing.

You can download the source code and customize it by yourself.

Note that this APP reads the .csv by regarding column B as X and the selected Data column (D by default) as Y.

Examples of output format:

|  V1  |  C@f1  |  C@f2  |   ...   |  C@fi  |                                                                  (C-V single)

|  V1  |  C@f1  |  C@f2  |   ...   |  C@fi  |  V2  |  C@f1'  |  C@f2'  |   ...   |  C@fi'  |                   (C-V double)

|  V1  | abs(I) |   V2   | abs(I)' |                                                                           (I-V double)

| Time |   I1   |                                                                                              (I-t single)
