Step 26 of 50: validation loss 0.8608, accuracy 0.7342.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   845    16    61     2     0     2     6     0    58     1
               1     0   950     6     0     9     3     1    44    39    12
               2     3     8   728    69    40    17     8    24    92     1
               3     2     0    30   640     0   224     2    41    81    10
               4     8    92    10     9   742     0     6     6    31    79
               5    12     3     0    25     4   610   134    18    81    28
               6    36    67     7     7    40     1   774     0    31     4
               7    15     1    56    66    47     5     2   806     2    90
               8     9    21    55    57     4     7    25    29   651   151
               9    85    16    43    85    18     4    33    53    28   596

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
24 | 0.8659 | 0.7267
25 | 0.8632 | 0.7298
26 | 0.8608 | 0.7342

At most 24 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 27 in one Python code block.
