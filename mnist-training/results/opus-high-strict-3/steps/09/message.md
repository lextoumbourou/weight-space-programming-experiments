Step 8 of 15: validation loss 0.9795, accuracy 0.7212.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   877    23    21     0     3     0    52     0     1    14
               1     0  1025    18     1     1    13     3     3     0     0
               2    24    29   607    68    24     2     8    29   162    37
               3     7    10    17   673     0   237    17     4    60     5
               4     6   129     2     2   711    14     8     3    28    80
               5     9    21     0   111     4   466   191    10    44    59
               6    49    83     3     0     9     6   783     0     4    30
               7    15    19    21    16     4    46     0   844     0   125
               8     8   198    82   109     0     7    24    41   488    52
               9    23    58     7    18     8    35     5    61     8   738

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 4.8050 | 0.4403
2 | 1.0673 | 0.6866
3 | 1.3639 | 0.6626
4 | 2.2082 | 0.6541
5 | 1.0513 | 0.7082
6 | 1.0357 | 0.7054
7 | 1.6683 | 0.6427
8 | 0.9795 | 0.7212

7 steps left. Reply with the complete build_weights() for step 9 in one Python code block.
