Step 2 of 15: validation loss 3.2936, accuracy 0.2438.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0     0     3     0     1     0     6     0     3   978     0
               1     0   605     0     2     0   220     0   229     7     1
               2     0     3     2    32     4   338     0    17   593     1
               3     0     1     0    48     0   863     0     6   103     9
               4     0    16     0     0   194   173     0    36   494    70
               5     0     1     0     3     0   833     0     6    69     3
               6     0     4     0     0     0   410     0     4   549     0
               7     0     6     0     9     0   217     0   128    86   644
               8     0     8     0     0     0   516     0   102   382     1
               9     0    11     0     0     1   224     0    37   442   246

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 6.1362 | 0.2816
2 | 3.2936 | 0.2438

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
