Step 21 of 50: validation loss 0.8620, accuracy 0.7257.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   862    13    55     3     0     4    10     0    43     1
               1     0   968     5     0     7     3     1    33    39     8
               2     2     9   703    74    52    17     9    27    96     1
               3     1     0    24   636     1   226     2    40    91     9
               4     5    74     4    24   738     0     3     5    23   107
               5    12     4     0    29    10   599   141    15    76    29
               6    28    65     5     7   122     1   708     0    26     5
               7    23     3    57    86    26     5     3   812     2    73
               8     8    26    45    58     4     7    28    27   617   189
               9    84    20    33   100    15     5    35    37    18   614

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

At most 29 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 22 in one Python code block.
