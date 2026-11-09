Step 7 of 15: validation loss 1.2388, accuracy 0.6587.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   757    62    46     0     0     3   111     0     4     8
               1     0  1016     6     0     0    32     2     3     0     5
               2    81    48   590    48    16    16    34    82    45    30
               3    16     8    45   669     1   138    26    61    20    46
               4    13   190    11     0   421     7    14     3    13   311
               5    25    31    32    47     2   593    83    11    30    61
               6    18    65     5     0    23    80   769     1     2     4
               7    14     8     3    13     8     0     2   718     0   324
               8    13   288    45     2     1    26    42   140   222   230
               9    16    31     1     3     0     3     1    74     0   832

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

8 steps left. Reply with the complete build_weights() for step 8 in one Python code block.
