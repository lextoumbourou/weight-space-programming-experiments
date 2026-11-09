Step 3 of 15: validation loss 4.1205, accuracy 0.2481.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0     4     0     8    92     0     5    24     0   858     0
               1     0   110    17     6   137     0    32     0   745    17
               2     0     0   175   311     0     0     1     1   490    12
               3     0     0     0   923     0     2     2     0   102     1
               4     1     0     3    48    76     1    13     0   817    24
               5     0     0     5   577     0   129    44     0   159     1
               6     4     0    25    35     5    63    37     0   798     0
               7     3     0   130   271     0     4    30     1   441   210
               8     0     0    14   113     0     5     5     0   864     8
               9     0     0     2   200     1     0    12     0   584   162

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.3919 | 0.2590
2 | 1.4921 | 0.4959
3 | 4.1205 | 0.2481

12 steps left. Reply with the complete build_weights() for step 4 in one Python code block.
