Step 2 of 15: validation loss 1.2553, accuracy 0.6304.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   525    16   203     0     0     2   233     0    10     2
               1     0   889    89     0    78     0     1     0     7     0
               2     6    13   826    89     1     0     8     0    39     8
               3     0     2   192   714     0    44    24     0    51     3
               4     2    60    53    56   594     1   195     0    16     6
               5     2     5    29    34     0   549   260     0    35     1
               6     1    38    25     0     1     3   874     0    25     0
               7     3    29   109   239     6    18    40   230     4   412
               8     4    36   150    10     1     6   165     1   613    23
               9     9    25    58    96    12    32   225     0    14   490

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 0.9981 | 0.6911
2 | 1.2553 | 0.6304

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
