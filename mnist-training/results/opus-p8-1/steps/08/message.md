Step 7 of 50: validation loss 1.3242, accuracy 0.6409.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   732     9   221     0     0     6     0     2    20     1
               1     0   884   123     0     0     1     4    48     1     3
               2    15     9   675    65     3    14    18     4   187     0
               3     2     1    46   722     0   134     7    13    95    10
               4     2    56   109     8   522     0    22     4   169    91
               5     5     8    38    95     0   459   210     2    94     4
               6    39    41    39     3     9     0   735     0   101     0
               7     3     7   137    24     8   123     0   606    10   172
               8     5    49   299     5     2     1    18    21   568    41
               9    32    31   128     5    17    29     6    31   176   506

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.7511 | 0.3148
2 | 1.2930 | 0.6248
3 | 1.5677 | 0.5552
4 | 1.3191 | 0.5505
5 | 1.2707 | 0.6192
6 | 1.8067 | 0.6464
7 | 1.3242 | 0.6409

At most 43 steps left. Reply with the complete build_weights() for step 8 in one Python code block.
