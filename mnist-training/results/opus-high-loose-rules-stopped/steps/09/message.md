Step 8 of 50: validation loss 0.5529, accuracy 0.8265.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   935     0    10     0     5     0    35     0     0     6
               1     0   974    67     0     7     0     0     4    12     0
               2    10     3   768   119    24     1    15    21    24     5
               3     6     0    33   775     1   151    27    12    15    10
               4     3    27     0     1   854     0     4     1    18    75
               5     7     7     2    30     1   713    48    15    85     7
               6    14     8     0     1    40     9   859     0    10    26
               7     7     2    22     3    15     1     4   919     1   116
               8    29    32    57    39     7    17    38    28   692    70
               9     9     2     7    19    22     2    18    83    23   776

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.9468 | 0.2540
2 | 1.2629 | 0.5742
3 | 1.0920 | 0.6503
4 | 1.0095 | 0.7297
5 | 0.9636 | 0.7647
6 | 0.9087 | 0.8054
7 | 0.8223 | 0.7877
8 | 0.5529 | 0.8265

42 steps left. Reply with the complete build_weights() for step 9 in one Python code block.
