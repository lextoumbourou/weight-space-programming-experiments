Step 3 of 50: validation loss 1.9548, accuracy 0.5810.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   711    41   194     1     3    15     6    19     0     1
               1     0   899    87     0     5     0     0    72     1     0
               2     8    61   739    46    84     5     1    38     3     5
               3     5    22    60   507     6   143     5   272     0    10
               4     3   215    63     1   492     1     3    60     1   144
               5    13    35    16    15    34   590    62   136     7     7
               6    86   169    28     0   230    33   415     3     0     3
               7     5    49    58     9    24    41     0   880     0    24
               8    25   197   236     6    12     4    84   246    73   126
               9    23    96    56    11    36     7     8   220     0   504

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.2203 | 0.6525
2 | 1.0061 | 0.6721
3 | 1.9548 | 0.5810

At most 47 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 4 in one Python code block.
