Step 10 of 15: validation loss 0.8536, accuracy 0.7432.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   785    20    43     0     0     0   140     0     2     1
               1     0   989    57     0     5     9     0     2     0     2
               2    44    30   612   123    18     3     4    22    99    35
               3     3     0     9   800     1   138     3     8    63     5
               4     9   100    26     2   650     0     8     5    99    84
               5     4    12     5    47     5   717    83     6    32     4
               6    67    80     1     0    21    19   760     0    16     3
               7    33    10    16    10    23    29     7   830    10   122
               8     8   169    96    25     3     7    23    42   575    61
               9    30    33    10    11    17    15    17    78    36   714

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5227 | 0.5126
2 | 1.2842 | 0.6440
3 | 0.9794 | 0.7006
4 | 1.8724 | 0.4922
5 | 1.0033 | 0.6914
6 | 1.0466 | 0.6887
7 | 1.2388 | 0.6587
8 | 0.9143 | 0.7293
9 | 1.1220 | 0.6314
10 | 0.8536 | 0.7432

5 steps left. Reply with the complete build_weights() for step 11 in one Python code block.
