Step 1 of 50: validation loss 2.3242, accuracy 0.5148.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   810    22   136     0     0     3     4    16     0     0
               1     0   924     3     0     0     0     0   137     0     0
               2    12   131   763     8     3     8     6    59     0     0
               3    10   117   104   329     0   189     9   271     0     1
               4     8   350    41     0   358     1     2   194     0    29
               5    27   229     4     1     8   481    16   147     0     2
               6   142   294    24     0     2   106   381    18     0     0
               7    12   102    35     0     6    15     0   919     0     1
               8    32   205   244    30     2    18    53   407     3    15
               9    83   216    79     0    58     8     2   335     0   180

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.3242 | 0.5148

At most 49 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 2 in one Python code block.
