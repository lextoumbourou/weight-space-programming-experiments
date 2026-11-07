Step 4 of 50: validation loss 1.7558, accuracy 0.5974.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   635    15   225     1     0    74    39     2     0     0
               1     1   986    18     0     2     1     0    56     0     0
               2    34    38   688   138    15    27     5    28    15     2
               3     4    21    58   722     0   134     1    73     2    15
               4    20   240    82     1   345     8    34    31     0   222
               5    13    46    43   101     3   615    66    26     0     2
               6    88   141    57     2   148    19   509     3     0     0
               7     4    38    40    23     1    32     0   854     0    98
               8    57   114   215    18     6    39   127   173   152   108
               9    66    85    55     3     1    79    37   164     3   468

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4065 | 0.6314
2 | 1.8335 | 0.5049
3 | 1.3679 | 0.6182
4 | 1.7558 | 0.5974

At most 46 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
