Step 5 of 15: validation loss 0.8736, accuracy 0.7192.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   818    11    46     0     1     7    83     0    25     0
               1     0   965    70     5     5     5     0     6     8     0
               2     4     9   764   174     3     2     1    17    13     3
               3     0     1    51   944     4    24     0     4     2     0
               4     2    76    40     6   806     2    21     2    13    15
               5     2     9     1   320     9   532    28     3    11     0
               6    62    38    38     0    40     2   779     0     2     6
               7    26     9    75    28    62    97    15   734     4    40
               8    10    91   174   149    16    13    43    27   469    17
               9    27    51    45   117   144    73    63    55     5   381

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 0.9176 | 0.7428
2 | 0.8203 | 0.7656
3 | 0.8671 | 0.7260
4 | 1.3566 | 0.5882
5 | 0.8736 | 0.7192

10 steps left. Reply with the complete build_weights() for step 6 in one Python code block.
