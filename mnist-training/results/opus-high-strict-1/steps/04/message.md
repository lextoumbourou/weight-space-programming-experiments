Step 3 of 15: validation loss 1.2434, accuracy 0.5977.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   663     8   258     5     0     2    25     1    29     0
               1     0   869   123     0     3     9     4    55     1     0
               2    10     9   552   131     7     2    24     2   232    21
               3     3     1    65   843     0    36     2     2    75     3
               4     1    76   102     2   406     2    70    15    82   227
               5     9     2    19    84     0   482   113     1   204     1
               6    72    17    11     6     7    56   697     0   100     1
               7     7    28   228    30    19     3     2   565    66   142
               8    10    44   142    12     2    15   164    11   584    25
               9    37    32   106    14    25    16    83    33   299   316

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 4.3782 | 0.4924
2 | 2.6052 | 0.5593
3 | 1.2434 | 0.5977

12 steps left. Reply with the complete build_weights() for step 4 in one Python code block.
