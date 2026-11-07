Step 3 of 15: validation loss 1.9209, accuracy 0.3803.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   619   124   148    13     0     0    44     7    34     2
               1     0   948     6     0     0     0     0   110     0     0
               2     0   285   574    42     3     0    49    32     1     4
               3     0   548   163   115     0    12     4    43     0   145
               4     1   537     1     0   364     0    62     5     0    13
               5     2   569    10    24     1   113    58    15     2   121
               6     3   477     2     0     1     0   475     1     8     0
               7     0   267     3     2     2     0     0   339     0   477
               8     0   760    30     1     1     3    13   186     7     8
               9     6   613     1     1    29     0    21    31    10   249

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 6.1362 | 0.2816
2 | 3.2936 | 0.2438
3 | 1.9209 | 0.3803

12 steps left. Reply with the complete build_weights() for step 4 in one Python code block.
