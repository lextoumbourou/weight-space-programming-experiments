Step 7 of 50: training loss 0.9306, accuracy 0.7290.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   798    13    27     0     8     2     4     0   139     0
               1     0   991    45     4     4     6     5     7     0     2
               2     9     5   569    28   163     3     6     9   192     6
               3     3    11     5   680     4   121     8    16   170    12
               4     1    27     1     0   825     1     5     6    11   106
               5    10     5     5    16     5   628    95     6   141     4
               6    30    21     4     0    97     1   800     0    13     1
               7    17     3    36    27     5     6     0   761    16   219
               8     3   153    53     2    11    10    59    69   549   100
               9    23    23     3     5    54    10    14    87    53   689

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.2152 | 0.6072
2 | 1.2620 | 0.6013
3 | 2.4275 | 0.5608
4 | 1.4795 | 0.6030
5 | 1.9930 | 0.3961
6 | 1.0068 | 0.6843
7 | 0.9306 | 0.7290

At most 43 steps left. Reply with the complete build_weights() for step 8 in one Python code block.

