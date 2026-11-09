Step 1 of 15: validation loss 1.5227, accuracy 0.5126.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   648     0     0     0     0     0   181     0   159     3
               1     0   665   141     4     1     8     8   194    23    20
               2    25     0   176    46     0     0    12     7   648    76
               3     0     0     0   341     0    20     2     1   660     6
               4     8     1     0     0   178     0     5     2   556   233
               5     1     0     0     6     0   220   109     2   575     2
               6    15     0     0     0     0     1   806     0   145     0
               7    18     0     5     7     2     6     0   475   185   392
               8     1     1     0     1     1     0     6     4   964    31
               9    14     0     0     1     0     0    10     4   279   653

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5227 | 0.5126

14 steps left. Reply with the complete build_weights() for step 2 in one Python code block.
