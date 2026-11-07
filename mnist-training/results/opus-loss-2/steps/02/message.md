Step 1 of 50: validation loss 1.2203, accuracy 0.6525.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   743    11   199     0     0    27     9     0     1     1
               1     0   983    36     0     5     5     1    34     0     0
               2    18    25   657    88    49    21    25    10    96     1
               3     2     4    22   743     1   205     7    32     6     8
               4    25    85    34     1   327     8    54     7    38   404
               5     4    11     9    54     2   606   205     5    17     2
               6    46    49     8     0     8    43   803     0    10     0
               7     2    25    79    39     4    82     2   659     2   196
               8    14   120   161     9     0    63   148    45   374    75
               9    39    38    56    21    13    46    51    41    26   630

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.2203 | 0.6525

At most 49 steps left. The run stops early, after any step, once the best validation loss has not improved by at least 1% over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 2 in one Python code block.
