Step 2 of 50: training loss 1.2620, accuracy 0.6013.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   747    21   167     0     0     6    48     0     1     1
               1     0  1050     6     0     0     8     0     0     0     0
               2    11    39   607   194     0    23    56     5    55     0
               3     3    12    32   836     0   123     4    10     9     1
               4    11   271    18    14   157    64   141     2     2   303
               5    10    28    15    67     0   617   171     3     4     0
               6    46    87     4     0     0    53   776     0     1     0
               7     9    31   352   120     0    47     0   471     2    58
               8     7   224   123    44     0    42   197    36   256    80
               9    47   112    91    15     0   101    35    51    13   496

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.2152 | 0.6072
2 | 1.2620 | 0.6013

At most 48 steps left. Reply with the complete build_weights() for step 3 in one Python code block.

