Step 10 of 15: validation loss 1.6706, accuracy 0.4832.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   676     9    29    51     8     2   211     0     5     0
               1     0   895     4    18     0    37     0   105     5     0
               2    28     9   668   135    64    24     7     9    46     0
               3     1    19    51   633    19   249     3     7    48     0
               4     3    72    16     6   533    69    75    13   161    35
               5    21   120    31    71    33   369    65     4   201     0
               6    30    87     9     8    84    48   585     1   115     0
               7     9    39    15   269    74   412    15   159    10    88
               8     6   137   395    37    27   138     2    83   184     0
               9    21    84     4    57   163   267    40    42   153   130

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 9.5504 | 0.1653
2 | 2.2641 | 0.1767
3 | 2.5593 | 0.3107
4 | 1.9442 | 0.3359
5 | 1.9561 | 0.3891
6 | 1.8661 | 0.4150
7 | 1.9247 | 0.3907
8 | 1.7631 | 0.4471
9 | 1.7416 | 0.4558
10 | 1.6706 | 0.4832

5 steps left. Reply with the complete build_weights() for step 11 in one Python code block.
