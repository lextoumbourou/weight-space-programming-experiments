Step 5 of 15: validation loss 1.3371, accuracy 0.6101.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   772     9   163     0     0    24     2     0    21     0
               1     0   944    67     4     5    42     2     0     0     0
               2    14    11   562   274    26    56    22     2    22     1
               3     1     0    13   796     0   179     8     1    32     0
               4     3    40    58     9   618    13    17     1    99   125
               5     2     0     4    42     0   729   126     2    10     0
               6    36    10    13     9    11   295   567     0    25     1
               7     8    19   182   164    15    25     4   444     7   222
               8    10    25   111    77     3   125   238     5   365    50
               9    28    20    73    47     6   159    29     7   288   304

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 4.3782 | 0.4924
2 | 2.6052 | 0.5593
3 | 1.2434 | 0.5977
4 | 1.2769 | 0.5620
5 | 1.3371 | 0.6101

10 steps left. Reply with the complete build_weights() for step 6 in one Python code block.
