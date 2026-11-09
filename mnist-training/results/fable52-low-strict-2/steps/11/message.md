Step 10 of 15: validation loss 0.8312, accuracy 0.7424.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   857    13    63     0     0     9    41     0     5     3
               1     0   963    49     1     6     0     0     2    41     2
               2    62    62   571    94    45     0     6    46    62    42
               3     8     2    53   784     1    89     4    51    33     5
               4     7    24    46     4   761     0     3     1    55    82
               5     8     5    49    60     1   650    90     3    48     1
               6    44    35    14     0   101    45   666     0    39    23
               7    16    17    17    56    13    12     3   817     3   136
               8    29    42    74    16     8    13    22    44   718    43
               9    19    24    39    25    18    17    26   121    35   637

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.0586 | 0.6515
2 | 0.9969 | 0.6680
3 | 1.1485 | 0.6657
4 | 0.9467 | 0.6909
5 | 0.9762 | 0.6769
6 | 0.8629 | 0.7278
7 | 0.8344 | 0.7409
8 | 0.9137 | 0.7124
9 | 0.8746 | 0.7264
10 | 0.8312 | 0.7424

5 steps left. Reply with the complete build_weights() for step 11 in one Python code block.
