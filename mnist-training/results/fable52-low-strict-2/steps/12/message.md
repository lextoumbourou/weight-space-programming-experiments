Step 11 of 15: validation loss 0.8435, accuracy 0.7374.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   842    12    59     0     0    12    58     0     4     4
               1     0   954    53     0     6     1     0     2    45     3
               2    56    51   581    67    62     0     9    57    60    47
               3     7     2    57   739     1   107     6    71    36     4
               4     9    26    51     3   693     0     7     2    69   123
               5     8     4    45    44     0   660   108     3    42     1
               6    43    29    14     0    22    55   727     0    48    29
               7    14    14    21    51    19    14     8   819     3   127
               8    25    34    75    13     5    18    27    52   716    44
               9    18    21    43    26     9    23    32   110    36   643

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.0586 | 0.6515
2 | 0.9969 | 0.6680
3 | 1.1485 | 0.6657
4 | 0.9467 | 0.6909
5 | 0.9762 | 0.6769
6 | 0.8629 | 0.7278
7 | 0.8344 | 0.7409
8 | 0.9137 | 0.7124
9 | 0.8746 | 0.7264
10 | 0.8312 | 0.7424
11 | 0.8435 | 0.7374

4 steps left. Reply with the complete build_weights() for step 12 in one Python code block.
