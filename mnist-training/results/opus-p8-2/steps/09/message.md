Step 8 of 50: validation loss 1.0999, accuracy 0.6685.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   766    10    38     0     1    38    94     2    41     1
               1     0   902    81     1     9     0     0    69     0     2
               2    10    20   493   155    42    14     6    32   218     0
               3     3     7    18   710     1    95     1    44   132    19
               4     2    55    15     0   610     0    11     1   175   114
               5     7    10    14    50     8   632   102     3    86     3
               6    24    59    10     1    70     9   753     0    40     1
               7    18     8    62    31    33    51     3   616    47   221
               8     2    92   106     8     7    17    40    47   635    55
               9    37    48    15     4    23    35    16    30   185   568

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4065 | 0.6314
2 | 1.8335 | 0.5049
3 | 1.3679 | 0.6182
4 | 1.7558 | 0.5974
5 | 1.3255 | 0.5417
6 | 1.1397 | 0.6529
7 | 1.3018 | 0.5786
8 | 1.0999 | 0.6685

At most 42 steps left. Reply with the complete build_weights() for step 9 in one Python code block.
