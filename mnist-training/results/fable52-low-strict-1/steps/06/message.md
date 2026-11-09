Step 5 of 15: validation loss 1.0033, accuracy 0.6914.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   763    23    33     0     0     0   165     0     0     7
               1     0   979    51     0     1    15     3     9     0     6
               2    66    26   492   185     6     3    27    36    86    63
               3    11     0     4   835     0   105    28    12    26     9
               4    12   101    21     1   412     2    20     6    76   332
               5    11    10     6    52     0   610   191    13    16     6
               6    32    51     1     0     2     4   870     0     0     7
               7    28     1    10    18     5     6     8   784     6   224
               8     9   135    92    96     2     6    53   102   373   141
               9    30    14     7    14     0     4    12    77     7   796

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5227 | 0.5126
2 | 1.2842 | 0.6440
3 | 0.9794 | 0.7006
4 | 1.8724 | 0.4922
5 | 1.0033 | 0.6914

10 steps left. Reply with the complete build_weights() for step 6 in one Python code block.
