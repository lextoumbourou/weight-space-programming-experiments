Step 5 of 50: training loss 1.9930, accuracy 0.3961.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   345     0     0     0     3     0     0     0   642     1
               1     0   931     5     0     9     0     3    51    27    38
               2     0     1    82     0    13     0     4     2   814    74
               3     0     0     0     4     0     1     1     2   997    25
               4     0     5     0     0   295     0     0     0   337   346
               5     1     0     0     0     1     2    27     2   872    10
               6     0     3     0     0   111     0   423     0   418    12
               7     0     2     4     0     0     0     0   182    55   847
               8     0    17     0     0     1     0     4     5   908    74
               9     0     4     0     0     0     0     1     6   161   789

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.2152 | 0.6072
2 | 1.2620 | 0.6013
3 | 2.4275 | 0.5608
4 | 1.4795 | 0.6030
5 | 1.9930 | 0.3961

At most 45 steps left. Reply with the complete build_weights() for step 6 in one Python code block.

