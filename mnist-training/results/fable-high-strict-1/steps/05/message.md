Step 4 of 15: validation loss 1.6809, accuracy 0.4863.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   594    53     4    10     2     0   324     4     0     0
               1     0  1013     9     0     0     0     0    41     0     1
               2    26   191   542    42     6     0    27   146     7     3
               3     0    94    18   690     1    65    28   116    12     6
               4    12   278    10     0   408     0    45     8     3   219
               5     4   274     2   108    14   186   246    10    49    22
               6    66   342    12     2    15     6   485     1     1    37
               7    15   190     9    21    46    38    20   477     6   268
               8     2   384   106    87     4     0    41   258    35    92
               9    45   218     1    15    73     2    99    32    43   433

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 6.1362 | 0.2816
2 | 3.2936 | 0.2438
3 | 1.9209 | 0.3803
4 | 1.6809 | 0.4863

11 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
