Step 10 of 50: training loss 0.6970, accuracy 0.8092.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   877     0    57     0     0    17    29     0     8     3
               1     3  1044     6     0     1     1     0     9     0     0
               2    70    19   626   103     2    15     6    52    88     9
               3     7     1    15   854     0    96     9    14    28     6
               4    22    34    12     5   813     0    14    13    11    59
               5    16    14    13    16     1   783    47    15     6     4
               6   112    51    31     2    43    13   707     2     6     0
               7    14     7     9    24    13     3     4   992     0    24
               8    25    27    80     7     1    16    60    44   675    74
               9    50    13     9    13     2    30     3   113     7   721

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.0324 | 0.7147
2 | 0.9703 | 0.7579
3 | 0.9390 | 0.7680
4 | 119.7083 | 0.1230
5 | 0.8829 | 0.7778
6 | 4.5389 | 0.0215
7 | 2.5610 | 0.1328
8 | 0.8959 | 0.7820
9 | 1.2554 | 0.6317
10 | 0.6970 | 0.8092

At most 40 steps left. Reply with the complete build_weights() for step 11 in one Python code block.

