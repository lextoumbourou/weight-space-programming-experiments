Step 5 of 15: validation loss 1.9561, accuracy 0.3891.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   482    33     0     8     2     0   440     5    17     4
               1     0   815     0     1     0     3     0   245     0     0
               2    24   211   362   142     7    11    17   116    96     4
               3     0   368     9   406     4   121    25     9    73    15
               4     5   247     0     0   259     5   179    43   134   111
               5    14   385     5    25    13   214   101    14   136     8
               6    15   198     7     0    17     5   600     2   123     0
               7     3   295     0    37    36    19    24    64     2   610
               8     3   532    15     4     7    20     8   101   307    12
               9    17   387     0     4    55    23    51    11    31   382

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 9.5504 | 0.1653
2 | 2.2641 | 0.1767
3 | 2.5593 | 0.3107
4 | 1.9442 | 0.3359
5 | 1.9561 | 0.3891

10 steps left. Reply with the complete build_weights() for step 6 in one Python code block.
