Step 6 of 15: validation loss 1.5165, accuracy 0.5238.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   567     7    38    18     0    46   304     0     6     5
               1     0   805   135    43     0     3     1    77     0     0
               2    12     6   844    72     5    23    15     6     2     5
               3     0     1    63   726     0   222     8     8     1     1
               4     9    32    37     9   481     7    91     7     7   303
               5     2     7    91   174     3   480   148     2     2     6
               6    36    53    86    47    15    84   615     2     1    28
               7     5    18    62   121    47   258    19   241     0   319
               8     1    23   508   260     3    47    34    34    16    83
               9    35    25    49    54    61   145   113    10     6   463

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 6.1362 | 0.2816
2 | 3.2936 | 0.2438
3 | 1.9209 | 0.3803
4 | 1.6809 | 0.4863
5 | 2.2016 | 0.3779
6 | 1.5165 | 0.5238

9 steps left. Reply with the complete build_weights() for step 7 in one Python code block.
