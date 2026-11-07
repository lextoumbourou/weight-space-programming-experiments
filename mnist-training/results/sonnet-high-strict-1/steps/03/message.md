Step 2 of 15: validation loss 1.7764, accuracy 0.4517.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   676     0    85     4   153     3    47     1     1    21
               1     0   350     0     0   542     4   163     2     0     3
               2     0     3   198     6   611     0   133    11     5    23
               3     2     7     7   364   232    75    38    52    11   242
               4     0     6     0     0   627     1   205     1     8   135
               5     3     8     0    67    63   247   423     7    33    64
               6     2     0     0     0    52     1   904     0     2     6
               7     0     8    16     0    29     2     1   305     8   721
               8     3    30    46    17    91     6   512    87    74   143
               9     6    10     2     1   106     4    50     8     2   772

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 28.9933 | 0.1083
2 | 1.7764 | 0.4517

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
