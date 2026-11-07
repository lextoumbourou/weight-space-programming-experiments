Step 3 of 15: validation loss 6.4219, accuracy 0.3542.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   441     2     0    22    90     0    27     4   383    22
               1     0   591     0     4     1     2     0   466     0     0
               2    51   114   366    15   213     6    28    69     1   127
               3     2    39    47   597   131    54     2     9    90    59
               4     8    16     1     0   718     1     8    15     7   209
               5     0   100     0   227   159   168   115    55    84     7
               6     5   156    10    25   245    39   401    23    29    34
               7     4   250    24    15   234   107     0    30    34   392
               8     0   254   172   103   107    18    17   166    48   124
               9     8    39     1    13   699     2     2     6     9   182

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 3.8220 | 0.2083
2 | 18.7136 | 0.1463
3 | 6.4219 | 0.3542

12 steps left. Reply with the complete build_weights() for step 4 in one Python code block.
