Step 4 of 15: validation loss 1.6030, accuracy 0.4847.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   645     4     2     1     0    26    91     0   217     5
               1     0   670   126   250     1     5     1     2     4     5
               2    33    18   359    11    36    49     5    14   378    87
               3     7     0    18    83     0   205    10    40   637    30
               4     2     2     3     8   193    69     0     2   242   462
               5     0     9     3    67     6   283    45    14   444    44
               6     5    26     2    15     4   176   475     0   257     7
               7     2     7    22    41    29    75     1   745    12   156
               8     0    19   118    34     1    25     0    45   677    90
               9     4     3     7    19    25    32     1    45   108   717

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.9434 | 0.3796
2 | 1.6381 | 0.4687
3 | 1.4273 | 0.5260
4 | 1.6030 | 0.4847

11 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
