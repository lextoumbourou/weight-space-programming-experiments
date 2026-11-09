Step 7 of 15: validation loss 0.8344, accuracy 0.7409.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   844    14    56     0     0    21    47     0     5     4
               1     0   970    47     0     7     0     0     2    36     2
               2    59    71   562    84    44     2     8    47    66    47
               3     5     2    48   752     1   108     6    60    43     5
               4     7    31    42     3   720     0     4     1    61   114
               5     6     6    42    44     0   640   111     3    62     1
               6    48    39    14     0    20    23   739     0    48    36
               7    15    21    16    47    14    14     6   803     2   152
               8    26    44    70    15     5    19    23    43   718    46
               9    17    29    35    19    14    14    30   110    32   661

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

8 steps left. Reply with the complete build_weights() for step 8 in one Python code block.
