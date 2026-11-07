Step 5 of 50: validation loss 1.2707, accuracy 0.6192.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   821    15   140     0     0     4     4     5     2     0
               1     0   908    92     0     0     3     3    58     0     0
               2    29    29   641   147     3    12    30    10    89     0
               3    14    25    45   692     1    83    23    50    70    27
               4    13   137    67    17   420     0    48     6    94   181
               5    31    19    40   131     0   343   251     9    46    45
               6    60    98    23     8     0    27   734     0    17     0
               7    28    29   125    21     5    95     0   714     2    71
               8    14   116   302    19     1     2    26    95   338    96
               9    69    81   104     9    12     6    12    58    29   581

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.7511 | 0.3148
2 | 1.2930 | 0.6248
3 | 1.5677 | 0.5552
4 | 1.3191 | 0.5505
5 | 1.2707 | 0.6192

At most 45 steps left. Reply with the complete build_weights() for step 6 in one Python code block.
