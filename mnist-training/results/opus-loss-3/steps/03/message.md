Step 2 of 50: validation loss 1.2956, accuracy 0.5868.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   766     4    84     7     1    47    74     6     0     2
               1     0   675    30     0    44     2    17   296     0     0
               2    34     4   254    99    91     9    18   324   107    50
               3     2     0    17   748     4   190     4    58     5     2
               4     7    18    37     4   691    10    39    65    38    74
               5     3     1     7    70    47   513   195    54    25     0
               6   134     3     0     0   121    63   600     6    39     1
               7    23     4   275     5    21    73     3   656     3    27
               8    12     9    84    68     5    15   137    92   563    24
               9    59     7   127    19   137    10    48   132    20   402

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.3858 | 0.5462
2 | 1.2956 | 0.5868

At most 48 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 3 in one Python code block.
