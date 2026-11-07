Step 2 of 15: validation loss 1.0673, accuracy 0.6866.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   783     8    17     0     1     0   154     4     0    24
               1     0   882   169     1     0     4     2     5     0     1
               2    19    31   576    54     7     0    12    17   211    63
               3     5     7    37   614     0   167    55    14   119    12
               4     5    53    13     3   616     9    50    17    55   162
               5     7    18     2    92     2   348   302    25    34    85
               6    22    34     6     0     3     0   873     0     3    26
               7     7    10    32    11     3    17     2   865     0   143
               8    12    94   161    28     0     0    52    45   548    69
               9    19    27    16     8     2    11     8    97    12   761

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 4.8050 | 0.4403
2 | 1.0673 | 0.6866

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
