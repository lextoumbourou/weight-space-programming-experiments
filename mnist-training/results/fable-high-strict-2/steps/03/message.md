Step 2 of 15: validation loss 1.4530, accuracy 0.4972.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   372     1     0     0     3     0   373     0   117   125
               1     0   906   123     0    14     1     6    11     3     0
               2     1     9   342     5    31     0    60     4   368   170
               3     0     7    13   213    23    23   269    39   430    13
               4     0    16     0     0   499     0     1    18   223   226
               5     0     7     7    15    31    43   303    67   367    75
               6     1    25     1     0    36     0   710     0   104    90
               7     0    13    10     1    51     0    11   657    17   330
               8     0    31    79     0    14     0    20    62   746    57
               9     0    17     0     0   260     0     4   123    73   484

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.1586 | 0.4753
2 | 1.4530 | 0.4972

13 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
