Step 5 of 15: validation loss 0.9762, accuracy 0.6769.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   624    17    51     0     0     4   259     0     1    35
               1     0   979    54     0     7     0     0     2    20     2
               2    59    68   461    47    84     2     2   122    26   119
               3     7     4    37   645     1   139     5    95    86    11
               4     4    21    28     2   779     1     0     8    22   118
               5     4     9    60    19     1   578    59    14   168     3
               6    17    52    30     0    71    17   648     0    91    41
               7    11     6     9    37    13    18     2   824     2   168
               8    15    95   142    10     6    11    14   107   553    56
               9    16    17    15    15    30    16    13   140    21   678

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.0586 | 0.6515
2 | 0.9969 | 0.6680
3 | 1.1485 | 0.6657
4 | 0.9467 | 0.6909
5 | 0.9762 | 0.6769

10 steps left. Reply with the complete build_weights() for step 6 in one Python code block.
