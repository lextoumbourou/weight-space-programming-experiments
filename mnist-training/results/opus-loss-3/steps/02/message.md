Step 1 of 50: validation loss 1.3858, accuracy 0.5462.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   785     2    72     3     0     1   115     0     9     4
               1     0   823   115     1    14     1    94     2    12     2
               2    23    11   301    88    16     1    21    15   396   118
               3     6     0    27   776     0    74    10     4   127     6
               4    13    33    15     2   324     0    33     0   240   323
               5     7     1    12    70     6   294   275     3   246     1
               6   129     3     0     0    26     6   619     0   182     2
               7    32    48   396    28    25    34    10   139    34   344
               8     4     8    35    11     2     1   109     0   817    22
               9    44    14   106    11    20     1    74     0   107   584

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.3858 | 0.5462

At most 49 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 2 in one Python code block.
