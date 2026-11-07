Step 9 of 15: validation loss 1.7416, accuracy 0.4558.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   675     3    10    30     8     2   175     0    88     0
               1     0   656    21     3     0     5     0   373     6     0
               2    28    13   562   123    52    14     1    10   186     1
               3     1    29    22   552    12   193     0     7   212     2
               4     3    30     0     2   443    26    20     5   425    29
               5    19    27    18    46    27   287    14     7   469     1
               6    26    19     1     2    57    19   375     1   467     0
               7     9    74     6   130    63   114     6   121    47   520
               8     5    50   183     9    16    60     0    73   610     3
               9    21    59     0    14   130    95     9    23   333   277

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 9.5504 | 0.1653
2 | 2.2641 | 0.1767
3 | 2.5593 | 0.3107
4 | 1.9442 | 0.3359
5 | 1.9561 | 0.3891
6 | 1.8661 | 0.4150
7 | 1.9247 | 0.3907
8 | 1.7631 | 0.4471
9 | 1.7416 | 0.4558

6 steps left. Reply with the complete build_weights() for step 10 in one Python code block.
