Step 24 of 50: validation loss 0.8659, accuracy 0.7267.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   856    13    62     4     0     3     8     0    44     1
               1     0   956     6     0    11     9     1    37    35     9
               2     2    10   720    76    42     9     7    27    97     0
               3     0     0    30   717     2   135     6    40    90    10
               4     7    79    13     9   769     0     5     5    24    72
               5    14     3     0    77     5   468   201    18    88    41
               6    39    64     7     9    51     2   763     0    28     4
               7    20     2    55    65    61     3     2   782     1    99
               8     7    23    58    56     5     7    26    29   639   159
               9    84    20    45    87    27     2    33    45    21   597

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4231 | 0.5723
2 | 1.3882 | 0.6128
3 | 1.1668 | 0.6014
4 | 1.0664 | 0.6522
5 | 1.0340 | 0.6710
6 | 1.0275 | 0.6668
7 | 1.0119 | 0.6788
8 | 1.0305 | 0.6521
9 | 1.1631 | 0.6279
10 | 1.0417 | 0.6767
11 | 1.0431 | 0.6827
12 | 0.9757 | 0.6870
13 | 0.9501 | 0.6891
14 | 0.9757 | 0.6901
15 | 0.9493 | 0.6901
16 | 0.9385 | 0.6967
17 | 0.9444 | 0.6945
18 | 0.9462 | 0.6999
19 | 0.9015 | 0.7112
20 | 0.8694 | 0.7234
21 | 0.8620 | 0.7257
22 | 0.8711 | 0.7286
23 | 0.8569 | 0.7327
24 | 0.8659 | 0.7267

At most 26 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 25 in one Python code block.
