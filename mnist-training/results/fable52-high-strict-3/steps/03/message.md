Step 2 of 15: validation loss 0.8203, accuracy 0.7656.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   862     4    27     0     1     8    77     0    12     0
               1     0   931    75     8     4     7     1    29     9     0
               2     9     3   752   171     5    10     6    16    15     3
               3     0     0    44   899     7    74     0     4     1     1
               4     8    14     5     4   885     3    39     4     5    16
               5     2     1     0   165     6   690    38     3    10     0
               6    64     6    15     0    30     6   842     0     1     3
               7    37     0    27    32    49    96    15   770     1    63
               8    13    27    73   151    19    61    75    34   521    35
               9    37    14     7    23   139   111    67    52     7   504

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 0.9176 | 0.7428
2 | 0.8203 | 0.7656

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
