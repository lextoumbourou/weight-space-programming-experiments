Step 10 of 15: validation loss 1.3906, accuracy 0.5376.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   606     6     9     0     2    14   166     1   184     3
               1     0   794    62    31     3     1     1   170     2     0
               2    52     7   620    79     8    24    10    40   141     9
               3     1     1    30   667     3   223     4    24    72     5
               4    11    23    10     2   601     0    39    19    70   208
               5     7     6    38   102    10   429   193    13   110     7
               6    64    54    13     9    46    24   527     5   209    16
               7    15     9    26    39   129   202    16   353     5   296
               8     4    23   269   139    12    34    24    92   286   126
               9    53    21     3    11   109    84   103    33    51   493

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 6.1362 | 0.2816
2 | 3.2936 | 0.2438
3 | 1.9209 | 0.3803
4 | 1.6809 | 0.4863
5 | 2.2016 | 0.3779
6 | 1.5165 | 0.5238
7 | 5.7134 | 0.1383
8 | 1.4762 | 0.4663
9 | 1.4172 | 0.5308
10 | 1.3906 | 0.5376

5 steps left. Reply with the complete build_weights() for step 11 in one Python code block.
