Step 2 of 15: validation loss 2.1738, accuracy 0.2905.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0     0   193     0     0   158   188   384     0    43    25
               1     0  1045     0     0     0     4     9     0     6     0
               2     0    48     2    24     7   178   729     0     2     0
               3     0    25     0    36     0   930    37     0     1     1
               4     0   393     0     0   384    27   171     0     8     0
               5     0    15     0     0     1   759   136     0     3     1
               6     0   191     0     0    95    11   670     0     0     0
               7     0   267     0     7   152   612     6     0     1    45
               8     0   335     0     0     3   459   211     0     1     0
               9     0   317     0     0   153   439    41     0     3     8

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 6.9037 | 0.1502
2 | 2.1738 | 0.2905

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
