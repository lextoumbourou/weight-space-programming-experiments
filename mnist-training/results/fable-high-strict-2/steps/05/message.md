Step 4 of 15: validation loss 1.3876, accuracy 0.4982.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   531     9     0     0     0     0    16     0   365    70
               1     0   961    85     9     0     6     1     0     1     1
               2     1    29   226   124     4    13    10     0   461   122
               3     1    10     0   617     0    96    36     1   259    10
               4     0    60     0     0   328     3     0     7   424   161
               5     1    22     1   139     0   276    33     4   396    43
               6     4    58     1     9     2    50   114     0   663    66
               7     0    57     6    27     6     1     1   583    51   358
               8     0    87    24    59     0    13     0     6   795    25
               9     1    69     1     8    41    10     0    57   223   551

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.1586 | 0.4753
2 | 1.4530 | 0.4972
3 | 1.2907 | 0.5670
4 | 1.3876 | 0.4982

11 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
