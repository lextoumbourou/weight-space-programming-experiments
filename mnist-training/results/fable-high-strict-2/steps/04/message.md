Step 3 of 15: validation loss 1.2907, accuracy 0.5670.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   689     9    14     0    10     0   159     9    14    87
               1     0   972    74     1     3     4     3     7     0     0
               2    10    21   566    63   110    15    44    14    57    90
               3     1    20    13   508    33   263   119    50    19     4
               4     1    36     9     0   751    19     0    63    10    94
               5     5    40     4    56    42   472   107   150     4    35
               6    15    72     8     4   178    83   519     0     5    83
               7     6    29     9     9    86    13     2   831     0   105
               8     0    94   244   103    43    76    24   214   162    49
               9     4    43     3     3   460    20     1   221     6   200

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.1586 | 0.4753
2 | 1.4530 | 0.4972
3 | 1.2907 | 0.5670

12 steps left. Reply with the complete build_weights() for step 4 in one Python code block.
