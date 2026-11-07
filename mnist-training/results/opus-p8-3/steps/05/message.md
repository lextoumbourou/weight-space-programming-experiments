Step 4 of 50: validation loss 1.5245, accuracy 0.5778.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   720     8    78     0     7    26     0     3   149     0
               1     0   874    18     1     8     3     0   160     0     0
               2     2    16   463    42    88    35     3     9   332     0
               3     0    13    10   458    17   234     0    29   263     6
               4     1    38     3     0   818     0     0    13    95    15
               5    14    19     2    63    32   655     2    25   100     3
               6    26    50     6     7   127   119   173     7   452     0
               7     7    12   215     5    97   159     0   555    24    16
               8     0    48    36    15    20    22     1   119   732    16
               9    16    42    17     8   171    23     0    69   285   330

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.8708 | 0.4273
2 | 1.4873 | 0.5904
3 | 1.5014 | 0.6332
4 | 1.5245 | 0.5778

At most 46 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
