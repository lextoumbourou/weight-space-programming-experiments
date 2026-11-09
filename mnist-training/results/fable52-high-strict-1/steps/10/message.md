Step 9 of 15: validation loss 0.8597, accuracy 0.7217.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   843     0     0     0     0     0    95     0    51     2
               1     2   994    13     2     9     2    26    11     0     5
               2   177     1   462    72     6     4    23     2   162    81
               3    40     0     2   833     0    82     7     0    53    13
               4    44    13     4     2   730     0    11    11     1   167
               5    91     0     8   103     1   582    68     6    36    20
               6   137     4     5     0    21     7   733     0    50    10
               7    87     4    10     9    22     7     1   638     1   311
               8    40     3   100   117     1    20    23    12   620    73
               9    99     9     2    16     8     9     1    28     7   782

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.3919 | 0.2590
2 | 1.4921 | 0.4959
3 | 4.1205 | 0.2481
4 | 2.9187 | 0.3582
5 | 378.0263 | 0.1887
6 | 1.6447 | 0.5262
7 | 1.2630 | 0.5479
8 | 264.5562 | 0.0551
9 | 0.8597 | 0.7217

6 steps left. Reply with the complete build_weights() for step 10 in one Python code block.
