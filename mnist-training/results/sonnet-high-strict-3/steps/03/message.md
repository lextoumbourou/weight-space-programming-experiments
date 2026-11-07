Step 2 of 15: validation loss 2.1968, accuracy 0.2092.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0     0     0   610     0     0   376     0     0     5     0
               1     0     0   120     0     0   747     0     0   197     0
               2     0     0   846     8     3   121     0     0    12     0
               3     0     0   829    26     1   152     0     5    17     0
               4     0     0   223     5   231   347     0     0   177     0
               5     0     0   646     5     3   238     0     9    14     0
               6     0     0   674     0     0   229     0     0    64     0
               7     0     0    57    92    50   310     0   535    46     0
               8     0     0   508     1     1   271     0    12   216     0
               9     0     0   223     7   215   301     0    82   133     0

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 7.1815 | 0.2094
2 | 2.1968 | 0.2092

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
