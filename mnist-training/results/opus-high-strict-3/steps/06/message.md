Step 5 of 15: validation loss 1.0513, accuracy 0.7082.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   802    12    33     0     2     0   130     0     1    11
               1     0   915   125     1     1     4     1    17     0     0
               2    20    34   595    67    17     1     9    18   185    44
               3     4     9    34   674     0   196    29    12    66     6
               4     3    82    14     2   679    13    36    11    43   100
               5     8    20     2    97     3   449   239    16    21    60
               6    31    56     4     0     4     1   845     0     3    23
               7     8    13    33    15     2    30     1   884     1   103
               8     9   130   167    41     1     2    38    56   510    55
               9    20    43    17     9     4    20    10   100     9   729

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 4.8050 | 0.4403
2 | 1.0673 | 0.6866
3 | 1.3639 | 0.6626
4 | 2.2082 | 0.6541
5 | 1.0513 | 0.7082

10 steps left. Reply with the complete build_weights() for step 6 in one Python code block.
