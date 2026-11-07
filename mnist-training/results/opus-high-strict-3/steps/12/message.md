Step 11 of 15: validation loss 0.8657, accuracy 0.7409.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   891    15    31     0     2     1    26     0    13    12
               1     0   989    40     0     0     3     1    22     9     0
               2    24    22   662    89    33     6     3    25    95    31
               3     6     5    26   750     0   186     1     4    45     7
               4     6    95     5    12   734    21     4     7    36    63
               5    11    10     0   178     4   475    92    10    98    37
               6    54    77     3     0    14    18   760     0    14    27
               7    22    14    24    23     3    48     1   858     2    95
               8    24    99    78    89     1    10    13    38   599    58
               9    29    46    18    37     8    48     4    71     9   691

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 4.8050 | 0.4403
2 | 1.0673 | 0.6866
3 | 1.3639 | 0.6626
4 | 2.2082 | 0.6541
5 | 1.0513 | 0.7082
6 | 1.0357 | 0.7054
7 | 1.6683 | 0.6427
8 | 0.9795 | 0.7212
9 | 0.9277 | 0.7288
10 | 0.9119 | 0.7315
11 | 0.8657 | 0.7409

4 steps left. Reply with the complete build_weights() for step 12 in one Python code block.
