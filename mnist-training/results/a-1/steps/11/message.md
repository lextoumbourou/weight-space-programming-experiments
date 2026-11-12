Step 10 of 50: training loss 1.3620, accuracy 0.5906.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   893     7     1    56     0     4    18     4     5     3
               1     0   850     5     6     0     9     1   193     0     0
               2    63   100   425    77     2     7   153    94    60     9
               3     2     7     2   761     0    85     6    57    10   100
               4     6    39     0     6   479     8   165    55     3   222
               5    35    52     0   154     4   238   231     4    27   170
               6    17    21     0    13     1    23   887     3     2     0
               7    42    18     5   190     2   135     0   423     0   275
               8     7    93    11    29     2     8    28   187   196   448
               9    77     8     1     6    22    33    14    45     1   754

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.5822 | 0.2385
2 | 1.7274 | 0.4707
3 | 4.1961 | 0.3259
4 | 6.2699 | 0.1342
5 | 1.5338 | 0.5524
6 | 1.4481 | 0.5577
7 | 1.3823 | 0.5594
8 | 1.4405 | 0.5443
9 | 1.5657 | 0.5843
10 | 1.3620 | 0.5906

At most 40 steps left. Reply with the complete build_weights() for step 11 in one Python code block.

