Step 5 of 15: validation loss 1.7825, accuracy 0.3806.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   699    58    48     0     0     3     2     0   176     5
               1     1   897     0     4     0     3     0     0   159     0
               2    33    27   298   230     8    93     0    14   248    39
               3     9     9    29   272     1    33     0    43   627     7
               4    14   169     2     4   145     0     0     1   551    97
               5    64    14    39    18     7    93    10    37   593    40
               6    27   131   114     0     0    30     0     0   571    94
               7    50    87     0   196    11     3     1   560   165    17
               8     3   149    18     7     1    15     0    26   785     5
               9    23   135     0    33    31     2     0    85   595    57

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 7.1815 | 0.2094
2 | 2.1968 | 0.2092
3 | 1.9429 | 0.3361
4 | 1.7848 | 0.3318
5 | 1.7825 | 0.3806

10 steps left. Reply with the complete build_weights() for step 6 in one Python code block.
