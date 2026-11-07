Step 22 of 50: validation loss 0.8711, accuracy 0.7286.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   861    13    56     3     0     4    11     0    42     1
               1     0   965     6     0    10     3     1    33    42     4
               2     2    11   716    73    39    16     9    27    97     0
               3     0     0    28   642     0   227     2    40    89     2
               4    12    92    11    11   779     0     5     7    29    37
               5    13     4     0    30     6   611   148    15    73    15
               6    40    66     7     6    46     2   774     0    25     1
               7    23     2    55    64    64     4     2   802     1    73
               8     9    28    66    64     5     7    29    38   667    96
               9   101    31    57   115    33     8    43    73    31   469

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

At most 28 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 23 in one Python code block.
