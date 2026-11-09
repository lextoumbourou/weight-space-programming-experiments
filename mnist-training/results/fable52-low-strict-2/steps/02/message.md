Step 1 of 15: validation loss 1.0586, accuracy 0.6515.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   591    14   132     0     0     9   244     0     0     1
               1     0   951    90     0     5    14     0     2     1     1
               2    11    46   664    95    40     1     2    54    10    67
               3     1     0    44   817     3   101     5    53     3     3
               4     6   131    95     1   480     1     5    17    48   199
               5     3     6    59   128     4   558   114    37     6     0
               6    49    59    60     0    32    27   705     0    13    22
               7     7    13    20    17     7    26    11   850     1   138
               8    10   130   258    50     2    22    73   105   291    68
               9     7    32    30    26     1    27    29   193     8   608

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.0586 | 0.6515

14 steps left. Reply with the complete build_weights() for step 2 in one Python code block.
