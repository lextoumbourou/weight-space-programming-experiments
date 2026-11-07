Step 5 of 50: validation loss 1.3255, accuracy 0.5417.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   653    14    10     0     0    18   176     0   119     1
               1     0   972    67     0     0     0     2    16     5     2
               2     1    19   370   110     0     2    12    18   453     5
               3     1    11     7   519     0    12     0    20   437    23
               4     3    75     1     0   128     0    16     0   388   372
               5     3    13     1    17     0   247   107     0   518     9
               6    11    66     1     0     0     1   770     0   117     1
               7     5    29    43    28     0    13     0   428   130   414
               8     2   107    35     0     0     3    21     7   789    45
               9    13    50     1     0     0     4    16     5   331   541

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4065 | 0.6314
2 | 1.8335 | 0.5049
3 | 1.3679 | 0.6182
4 | 1.7558 | 0.5974
5 | 1.3255 | 0.5417

At most 45 steps left. Reply with the complete build_weights() for step 6 in one Python code block.
