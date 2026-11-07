Step 15 of 50: validation loss 0.9234, accuracy 0.7504.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   804     9   123     0     1    16     1     0    36     1
               1     0   940    52     3    34    12     2    12     0     9
               2    34     9   659   130   110    20     8     6    13     1
               3     9     0    16   774     0   138     6     3    83     1
               4     3    20    36     1   701     5     1     6    35   175
               5    11     0     5    23     1   644    28     5   197     1
               6    44     6    18     0    28    54   811     0     5     1
               7     6     0    45    48     9     4     1   851    11   115
               8    25    21    44    68     7    92    62    42   607    41
               9    17     5    22    13    12    28     4    48    99   713

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 4.3782 | 0.4924
2 | 2.6052 | 0.5593
3 | 1.2434 | 0.5977
4 | 1.2769 | 0.5620
5 | 1.3371 | 0.6101
6 | 1.3076 | 0.6173
7 | 2.1437 | 0.5085
8 | 1.2513 | 0.6359
9 | 1.0575 | 0.7023
10 | 1.0173 | 0.7092
11 | 1.0146 | 0.7208
12 | 0.9488 | 0.7302
13 | 0.9289 | 0.7448
14 | 0.9244 | 0.7485
15 | 0.9234 | 0.7504

The step budget has been extended. Step 15 was not your last step: you now have up to 35 more steps, up to step 50 in total.

At most 35 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 16 in one Python code block.
