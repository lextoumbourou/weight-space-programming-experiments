Step 6 of 15: validation loss 0.8629, accuracy 0.7278.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   899    12    55     0     0    15     9     0     0     1
               1     1   984    48     0     7     0     0     2    22     0
               2   103    90   552    83    75     1     3    41    34     8
               3    10     6    44   813     2    96     8    33    16     2
               4    11    28    41     2   846     0     1     1    18    35
               5     9    10    55    66     2   606   136     3    27     1
               6    79    51    23     0    67    10   714     0    16     7
               7    37    35    18    57    24    11     6   832     0    70
               8    45   114   111    17     8    13    27    57   586    31
               9    55    40    38    45   129    10    47   147     4   446

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.0586 | 0.6515
2 | 0.9969 | 0.6680
3 | 1.1485 | 0.6657
4 | 0.9467 | 0.6909
5 | 0.9762 | 0.6769
6 | 0.8629 | 0.7278

9 steps left. Reply with the complete build_weights() for step 7 in one Python code block.
