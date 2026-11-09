Step 4 of 15: validation loss 0.9467, accuracy 0.6909.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   701    28   114     0     1     6   104     2     1    34
               1     0   975    48     0     7     0     0     4    28     2
               2    57    64   548    65    65     2     1    92    28    68
               3     9     3    46   631     1   114     3   136    79     8
               4     4    33    50     1   754     0     0    10    13   118
               5     4     8    77    20     0   577    59    21   146     3
               6    15    66    62     0    67     9   647     0    72    29
               7     5     7    10    25     9    10     2   884     4   134
               8    13   110   158     6     7    11    13   111   529    51
               9    14    20    25    14    15    13    11   173    13   663

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.0586 | 0.6515
2 | 0.9969 | 0.6680
3 | 1.1485 | 0.6657
4 | 0.9467 | 0.6909

11 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
