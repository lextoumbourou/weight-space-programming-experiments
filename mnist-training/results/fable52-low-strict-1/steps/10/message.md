Step 9 of 15: validation loss 1.1220, accuracy 0.6314.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   860    22    10     0     0     0     3     0    95     1
               1     0  1012    36     0     7     5     0     2     2     0
               2   101    52   322    11    25     1     5    38   426     9
               3     7     5     5   395     1    46     0    18   546     7
               4    12   109     1     0   653     0     0     2   176    30
               5    13    21     2     6     5   417    15     3   432     1
               6    94    95     1     0    23     3   611     0   140     0
               7    57    20     9    16    37     0     0   697    70   184
               8     9   203     6     0     4     0     1    17   739    30
               9    56    51     0     2    27     2     2    28   185   608

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5227 | 0.5126
2 | 1.2842 | 0.6440
3 | 0.9794 | 0.7006
4 | 1.8724 | 0.4922
5 | 1.0033 | 0.6914
6 | 1.0466 | 0.6887
7 | 1.2388 | 0.6587
8 | 0.9143 | 0.7293
9 | 1.1220 | 0.6314

6 steps left. Reply with the complete build_weights() for step 10 in one Python code block.
