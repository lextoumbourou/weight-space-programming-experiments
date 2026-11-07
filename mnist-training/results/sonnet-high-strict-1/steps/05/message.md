Step 4 of 15: validation loss 1.6377, accuracy 0.5136.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   672    10   193     5    40     3     9     3    55     1
               1     0   692    38     0   100     4    36   142    52     0
               2     1    19   416     8   319     2    73    12   136     4
               3     1    25    35   487    38    84     9    77   254    20
               4     0    35     0     0   370     3   124     1   371    79
               5     5    35     3    62    12   296   227    12   257     6
               6     7     0     0     1    32    12   704     0   207     4
               7     1    37    36     2     5     8     0   513    62   426
               8     2   108    69    11     8    11   153    86   542    19
               9    11    53     8     0    11     7     7    19   401   444

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 28.9933 | 0.1083
2 | 1.7764 | 0.4517
3 | 2.0240 | 0.3052
4 | 1.6377 | 0.5136

11 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
