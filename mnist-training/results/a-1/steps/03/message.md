Step 2 of 50: training loss 1.7274, accuracy 0.4707.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   587     3     9     8     0     0    61     1   322     0
               1     0   755    52     9     0     6     9   206    24     3
               2     8     6   217    92     0     4    59     2   600     2
               3     0     0     1   758     0    29     6     2   227     7
               4     3    13     1     6    32     0   256     2   571    99
               5     7     0     2   101     0   108   349     8   321    19
               6     6     6     0     2     0     0   884     1    68     0
               7    11     4   149   267     0   145     1   100    89   324
               8     0    11    17    17     0     0    20    12   898    34
               9    27     4     4    29     0     5    23     3   498   368

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.5822 | 0.2385
2 | 1.7274 | 0.4707

At most 48 steps left. Reply with the complete build_weights() for step 3 in one Python code block.

