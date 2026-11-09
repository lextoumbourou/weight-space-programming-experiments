Step 2 of 15: validation loss 1.2842, accuracy 0.6440.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   747    28   152     0     0     0    60     3     0     1
               1     0   882   119     0     0     2     0    61     0     0
               2    28    68   771    52     8     3     4    47     0     9
               3     7     2    71   689     1   149     9    98     0     4
               4    12   246   127     0   460     4     3    33     2    96
               5     6    34    17    23     5   668    81    75     0     6
               6    78   176    38     0     9     4   659     1     0     2
               7    14    25    15     1     6    13     3   983     0    30
               8    31   225   295    30     2    11    44   296    22    53
               9    36    82    26     6     1    11     9   231     0   559

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5227 | 0.5126
2 | 1.2842 | 0.6440

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
