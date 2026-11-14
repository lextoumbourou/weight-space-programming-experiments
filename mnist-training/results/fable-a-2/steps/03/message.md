Step 2 of 50: training loss 1.3785, accuracy 0.5515.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   260    10     8     0     0    87   514     0   104     8
               1     0   972    23     0     3     0     2     1    36    27
               2     4     3   196     2     5    22     7     2   723    26
               3     0     0     1     6     0   466     5     3   546     3
               4     1    24     0     0   473     0     2     1   248   234
               5     0     2     1     0     0   582    45     0   284     1
               6     0    16     0     0     8     7   791     0   144     1
               7     0     4     6     1     2    80     6   590    91   310
               8     0    21     1     0     2     5    13     0   963     4
               9     0    11     0     0     0    69    37    11   151   682

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.2181 | 0.6165
2 | 1.3785 | 0.5515

At most 48 steps left. Reply with the complete build_weights() for step 3 in one Python code block.

