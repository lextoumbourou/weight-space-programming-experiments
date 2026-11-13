Step 2 of 50: training loss 0.9703, accuracy 0.7579.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   784     0    75     2     0    58    51     0    19     2
               1     3  1029    16     0     3     3     0    10     0     0
               2    28     7   544   136     2     7    11    14   233     8
               3     1     0     7   696     0   126    26     4   146    24
               4     9    19    15     5   753     1    48    10    22   101
               5    10     9     8    45     2   576   215     8    40     2
               6    27    19     9     1   115     6   778     0    11     1
               7    10     2    25    40     2     6     7   913    11    74
               8    14    21    52     7     4     3    71    33   730    74
               9    18     9     0     5     1    26    29    83    14   776

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.0324 | 0.7147
2 | 0.9703 | 0.7579

At most 48 steps left. Reply with the complete build_weights() for step 3 in one Python code block.

