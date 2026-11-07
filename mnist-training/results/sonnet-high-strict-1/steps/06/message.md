Step 5 of 15: validation loss 1.4611, accuracy 0.5491.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   693    10   200    16    49    10     4     6     2     1
               1     0   669    52     1   158     4    23   156     1     0
               2     1    20   452    17   398    15    52    11    18     6
               3     1    19    40   668    60   147     8    61     7    19
               4     0    48     0     0   565    37   116     1    57   159
               5     4    40     7   121    30   431   231    13    30     8
               6    19     0     0     3    72    94   738     0    32     9
               7     1    36    44    13     6    16     0   513    10   451
               8     5   148   167   122    25    77   198   137    92    38
               9    13    88    13     4    38    65     7    23    40   670

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 28.9933 | 0.1083
2 | 1.7764 | 0.4517
3 | 2.0240 | 0.3052
4 | 1.6377 | 0.5136
5 | 1.4611 | 0.5491

10 steps left. Reply with the complete build_weights() for step 6 in one Python code block.
