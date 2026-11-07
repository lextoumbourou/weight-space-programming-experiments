Step 9 of 15: validation loss 1.4172, accuracy 0.5308.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   590     7     9     0     7     8   118     4   246     2
               1     0   791    62    28     8     0     0   173     2     0
               2    46     8   627    62    14    13     7    46   161     6
               3     1     1    32   656     7   200     2    32    96     3
               4    10    24     8     2   698     0    16    24    84   117
               5     8     7    45   115    22   395   124    18   175     6
               6    58    57    17     9    83     9   424     6   297     7
               7    15     9    23    42   205   158    11   411    11   205
               8     2    24   279   107    26    19    17   137   324    74
               9    51    21     4    15   177    78    69    51   103   392

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 6.1362 | 0.2816
2 | 3.2936 | 0.2438
3 | 1.9209 | 0.3803
4 | 1.6809 | 0.4863
5 | 2.2016 | 0.3779
6 | 1.5165 | 0.5238
7 | 5.7134 | 0.1383
8 | 1.4762 | 0.4663
9 | 1.4172 | 0.5308

6 steps left. Reply with the complete build_weights() for step 10 in one Python code block.
