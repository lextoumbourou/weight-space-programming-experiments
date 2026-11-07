Step 4 of 15: validation loss 1.9485, accuracy 0.3002.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0    10     0   350   170     0     6   310     0   145     0
               1     0   249   159   560     1     2    74     0     0    19
               2     0     0   783   154     4    11    21     0    17     0
               3     0     0   227   761     0    36     0     0     5     1
               4     0     1    85   389   261     1   213     0    27     6
               5     0     0   151   297     0   245   169     0    52     1
               6     0     0   179    54    27    12   666     0    28     1
               7     0     0    42   970     3     0     5     3    22    45
               8     0     0   481   290     0    46   175     0    17     0
               9     1     1    50   770    21     4    57     0    50     7

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.6151 | 0.1010
2 | 3.5391 | 0.1546
3 | 2.3164 | 0.2523
4 | 1.9485 | 0.3002

11 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
