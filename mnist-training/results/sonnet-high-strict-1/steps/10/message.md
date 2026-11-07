Step 9 of 15: validation loss 1.3440, accuracy 0.5742.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   835     5   105     6    28     1     2     4     4     1
               1     0   699    69     1    19     4    10   257     5     0
               2     7    28   567    19   236    12    28    17    75     1
               3     7     7    48   694    24   164     3    55    25     3
               4     6    80     4     0   401    57    56     7   217   155
               5    10    36     6   100    15   497   182    16    52     1
               6    91     9     0     2    47   140   595     0    75     8
               7     4    42    87    24     0    22     0   697    15   199
               8    13   113   174   133     7    52   120   178   192    27
               9    45    89    31     5    18    74     4    47    83   565

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 28.9933 | 0.1083
2 | 1.7764 | 0.4517
3 | 2.0240 | 0.3052
4 | 1.6377 | 0.5136
5 | 1.4611 | 0.5491
6 | 1.4698 | 0.5288
7 | 1.3827 | 0.5680
8 | 1.3262 | 0.5729
9 | 1.3440 | 0.5742

6 steps left. Reply with the complete build_weights() for step 10 in one Python code block.
