Step 2 of 15: validation loss 1.9302, accuracy 0.3116.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   693    37     4     2     1    54    17   164     6    13
               1     0   859     0     0     0     1     0   204     0     0
               2     6   385   253   133     9    29    54   115     6     0
               3     0   611     5    59    36     4     3   237     2    73
               4     7   486     0     0   382     0    20    45    43     0
               5    12   409     1     1    64   166    78    80     6    98
               6    55   348    27     1    19     6   374    12   125     0
               7    26   426     0    31    60    15     0   312     3   217
               8     1   584     4     0    43    12     9   348     4     4
               9    26   556     0     2   178     7    11   150    17    14

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.4126 | 0.1130
2 | 1.9302 | 0.3116

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
