Step 10 of 15: validation loss 1.6589, accuracy 0.5387.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   833     8    28     0    72     1    15     2    28     4
               1     0   737     7     3     1     6     0   310     0     0
               2    39    22   497   109   209    30    10    13    59     2
               3     6    10    10   715    19   139     0    40    60    31
               4    89    77    37    19   312    37    10    89    12   301
               5    18    34    27   175    19   484    49    60    44     5
               6   108    73    22    20   213    68   430     4    27     2
               7    15    20    34   102     2    39     0   615     8   255
               8    11    55   144    64   121    59    44   142   286    83
               9    69    63    15    18    57    97     2   128    34   478

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 7.1815 | 0.2094
2 | 2.1968 | 0.2092
3 | 1.9429 | 0.3361
4 | 1.7848 | 0.3318
5 | 1.7825 | 0.3806
6 | 1.7746 | 0.3360
7 | 2.9444 | 0.2186
8 | 3.9520 | 0.4274
9 | 1.7466 | 0.4891
10 | 1.6589 | 0.5387

5 steps left. Reply with the complete build_weights() for step 11 in one Python code block.
