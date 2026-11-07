Step 3 of 15: validation loss 2.0168, accuracy 0.3084.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   726    87     5     0     8     0   155     2     8     0
               1     0  1062     1     0     0     0     0     1     0     0
               2    28   408   353     3    75     0     0    15    27    81
               3     4   754    51     5    50     0    38   122     1     5
               4     8   485     1     0   290     0     1     1    82   115
               5     4   637     4     1     9    34   218     2     1     5
               6    21   680    22     1    10     2    64     0   154    13
               7    73   515     1     3     5     0    32   357     1   103
               8     4   946     1     3    13     2     9     7    11    13
               9    33   624     0     1    92     0     5     9    15   182

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.6085 | 0.1223
2 | 1.9985 | 0.4359
3 | 2.0168 | 0.3084

12 steps left. Reply with the complete build_weights() for step 4 in one Python code block.
