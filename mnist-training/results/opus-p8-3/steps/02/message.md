Step 1 of 50: validation loss 1.8708, accuracy 0.4273.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   539    70   296     0     0    12    29    45     0     0
               1     0  1049     0     0     0     0     0    15     0     0
               2     4   296   219   182     0     6    14   269     0     0
               3     0   307     9   405     4    32    13   260     0     0
               4     0   546     6     1   338     0    11    81     0     0
               5     0   486     8    35    18   281    43    43     0     1
               6     5   430    17     0     2    51   456     6     0     0
               7     0   189     6     0    23     1     0   871     0     0
               8    12   460    26    83     4    12    48   361     0     3
               9    27   319    32     3    61     7     2   395     0   115

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.8708 | 0.4273

At most 49 steps left. Reply with the complete build_weights() for step 2 in one Python code block.
