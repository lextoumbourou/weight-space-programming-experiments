Step 23 of 50: validation loss 0.8569, accuracy 0.7327.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   856    13    60     3     0     5    10     0    43     1
               1     0   961     6     0     9     4     1    35    36    12
               2     2    11   719    72    40    16     8    26    96     0
               3     0     0    28   637     1   230     2    37    84    11
               4     7    83    13     9   765     0     5     3    24    74
               5    13     4     0    29     5   610   139    15    73    27
               6    38    66     7     8    48     1   769     0    26     4
               7    22     2    56    64    59     4     2   781     1    99
               8     8    25    61    58     5     7    27    29   633   156
               9    86    21    45    87    24     4    33    44    21   596

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4231 | 0.5723
2 | 1.3882 | 0.6128
3 | 1.1668 | 0.6014
4 | 1.0664 | 0.6522
5 | 1.0340 | 0.6710
6 | 1.0275 | 0.6668
7 | 1.0119 | 0.6788
8 | 1.0305 | 0.6521
9 | 1.1631 | 0.6279
10 | 1.0417 | 0.6767
11 | 1.0431 | 0.6827
12 | 0.9757 | 0.6870
13 | 0.9501 | 0.6891
14 | 0.9757 | 0.6901
15 | 0.9493 | 0.6901
16 | 0.9385 | 0.6967
17 | 0.9444 | 0.6945
18 | 0.9462 | 0.6999
19 | 0.9015 | 0.7112
20 | 0.8694 | 0.7234
21 | 0.8620 | 0.7257
22 | 0.8711 | 0.7286
23 | 0.8569 | 0.7327

At most 27 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 24 in one Python code block.
