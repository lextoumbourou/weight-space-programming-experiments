Step 3 of 50: training loss 1.0856, accuracy 0.6834.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   672    17   217     1     0    53    30     1     0     0
               1     0   976    56     0     1     0     0    30     1     0
               2    23    70   612   171     3    24     1    40    38     8
               3     2    20    46   678     0   245     2    34     1     2
               4     7   128    79     5   618     6     8    35     3    94
               5     2    46    30    44     1   751     6    31     3     1
               6    67   227    43     0    10    98   517     0     0     5
               7    10    17    39     9    19    21     0   919     0    56
               8    17   147    51    23     5    61    32    74   522    77
               9    23    89    36    27    24    56     0   137     0   569

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.6415 | 0.6010
2 | 1.1281 | 0.6957
3 | 1.0856 | 0.6834

At most 47 steps left. Reply with the complete build_weights() for step 4 in one Python code block.

