Step 4 of 15: validation loss 1.2769, accuracy 0.5620.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   797     9   108     0     0     5    17     0    55     0
               1     0   925    72     3    10    44     8     0     2     0
               2     4     2   336   153     9     9    19     1   453     4
               3     1     0     5   706     0    74     0     0   244     0
               4     4    21    20     0   533     4    12     0   239   150
               5     4     0     2    55     1   494    58     0   301     0
               6    36     5     1     2    13   145   450     0   314     1
               7     8    11   150    69    10    13     4   359   130   336
               8     3    13    28     0     0    18    60     0   859    28
               9    16    13    20     8    24    30    35     0   654   161

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 4.3782 | 0.4924
2 | 2.6052 | 0.5593
3 | 1.2434 | 0.5977
4 | 1.2769 | 0.5620

11 steps left. Reply with the complete build_weights() for step 5 in one Python code block.
