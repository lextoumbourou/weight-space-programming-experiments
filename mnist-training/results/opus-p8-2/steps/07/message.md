Step 6 of 50: validation loss 1.1397, accuracy 0.6529.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   701    13    52     0     0    72   151     0     1     1
               1     0   932    87     1     5     1     2    34     0     2
               2     9    21   504   195    22    54    16    23   143     3
               3     1     8    19   712     1   217     3    34    12    23
               4     2    65    18     0   520     4   104     0    78   192
               5     2    10     9    19     2   747   119     0     3     4
               6    15    60     5     2    33    27   816     0     7     2
               7    10    12    80    32    24    91    20   555     8   258
               8     1   112   168    24     3    53   103    33   428    84
               9    25    55    24     2     7   105    48    19    62   614

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4065 | 0.6314
2 | 1.8335 | 0.5049
3 | 1.3679 | 0.6182
4 | 1.7558 | 0.5974
5 | 1.3255 | 0.5417
6 | 1.1397 | 0.6529

At most 44 steps left. Reply with the complete build_weights() for step 7 in one Python code block.
