Step 3 of 15: validation loss 2.3164, accuracy 0.2523.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0     0     1   726     6   152    65     6     5    30     0
               1     0   281   580    43   151     9     0     0     0     0
               2     0     1   747     3   232     4     3     0     0     0
               3     0    13   645   259    62    41     0    10     0     0
               4     0     6    14     2   960     1     0     0     0     0
               5     0    19   329    38   277   243     3     4     2     0
               6     0     3   205     0   743    13     3     0     0     0
               7     0    26   301   371   354     8     0    30     0     0
               8     0     8   851     5   122    23     0     0     0     0
               9     0    11    79    52   803    13     0     3     0     0

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.6151 | 0.1010
2 | 3.5391 | 0.1546
3 | 2.3164 | 0.2523

12 steps left. Reply with the complete build_weights() for step 4 in one Python code block.
