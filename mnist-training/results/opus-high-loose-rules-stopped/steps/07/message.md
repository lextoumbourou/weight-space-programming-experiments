Step 6 of 50: validation loss 0.9087, accuracy 0.8054.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   901     0     7     1     6     0    66     0     0    10
               1     1   907   103     0    11     3     9     7    23     0
               2    15     3   700   157    25     3    20    27    33     7
               3     5     0    25   725     2   204    31     9    20     9
               4     3    16     0     2   856     0     7     1    19    79
               5     5     6     1    26     3   701    50     8   108     7
               6     7     3     0     1    25    16   879     0    13    23
               7     4     1    22     1    20     2    13   879     1   147
               8    19    14    37    37     7    20    40    18   740    77
               9     4     0     6    15    25    13    24    63    45   766

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.9468 | 0.2540
2 | 1.2629 | 0.5742
3 | 1.0920 | 0.6503
4 | 1.0095 | 0.7297
5 | 0.9636 | 0.7647
6 | 0.9087 | 0.8054

44 steps left. Reply with the complete build_weights() for step 7 in one Python code block.
