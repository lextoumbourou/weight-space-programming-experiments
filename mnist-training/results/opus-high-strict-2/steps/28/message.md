Step 27 of 50: validation loss 0.8714, accuracy 0.7309.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   823    13    84     3     0     8     8     0    51     1
               1     0   935     7     0    12     1     1    53    43    12
               2     2     4   736    71    41    19     9    20    88     0
               3     0     0    35   671     0   210     2    39    67     6
               4    15   102     9    10   745     0     9     7    29    57
               5    13     2     3    29     4   609   124    19    80    32
               6    29    63     7     9    39     1   788     0    29     2
               7    15     0    64    79    52     7     2   829     2    40
               8     8    18    48    55     4     7    28    38   655   148
               9    86    17    46   116    21     6    27    89    35   518

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
25 | 0.8632 | 0.7298
26 | 0.8608 | 0.7342
27 | 0.8714 | 0.7309

At most 23 steps left. The run stops early, after any step, if validation accuracy has not improved by at least 0.5 percentage points over the previous 5 steps. The network from the last step that runs is scored on the test set. Reply with the complete build_weights() for step 28 in one Python code block.
