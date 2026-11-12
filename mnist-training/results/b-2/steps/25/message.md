Step 24 of 50: training loss 1199.8983, accuracy 0.1023.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0    11    39     1    58   649    90     2   108    33     0
               1     1   221   145     2   424   264     0     7     0     0
               2    16   463   203     5   186   116     0     1     0     0
               3    55   645    12    16   288    13     0     1     0     0
               4     6    87     1     3   469   222     2    84   109     0
               5   145    19     1   552   168     3    24     3     0     0
               6    10    18     0   141   523     0    95   180     0     0
               7    50   677    41     5   305    10     0     2     0     0
               8    26    43     0   110   784    15     4    24     3     0
               9    23   117     1    37   729    40     0     9     5     0

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.6349 | 0.3786
2 | 1.6757 | 0.5669
3 | 1.4210 | 0.5906
4 | 1.3284 | 0.6249
5 | 1.1885 | 0.6594
6 | 1.1142 | 0.6913
7 | 1.5617 | 0.6031
8 | 1.1344 | 0.6834
9 | 1.9282 | 0.6363
10 | 0.9695 | 0.6913
11 | 0.9275 | 0.7032
12 | 1107.3885 | 0.0831
13 | 1134.8277 | 0.0887
14 | 0.8973 | 0.7265
15 | 1077.1201 | 0.0622
16 | 1075.4426 | 0.0644
17 | 1047.6190 | 0.1387
18 | 1036.4964 | 0.0562
19 | 0.8330 | 0.7360
20 | 1254.7789 | 0.1760
21 | 1244.8506 | 0.0423
22 | 1295.6073 | 0.0936
23 | 1239.2741 | 0.0950
24 | 1199.8983 | 0.1023

At most 26 steps left. Reply with the complete build_weights() for step 25 in one Python code block.


Here are 16 training images your step 24 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 4, predicted 5 (top 3: 5 1.00, 2 0.00, 4 0.00)
2. true 6, predicted 4 (top 3: 4 1.00, 7 0.00, 3 0.00)
3. true 0, predicted 7 (top 3: 7 1.00, 4 0.00, 8 0.00)
4. true 3, predicted 1 (top 3: 1 1.00, 4 0.00, 0 0.00)
5. true 7, predicted 4 (top 3: 4 1.00, 1 0.00, 5 0.00)
6. true 9, predicted 5 (top 3: 5 0.98, 4 0.02, 2 0.00)
7. true 9, predicted 1 (top 3: 1 1.00, 0 0.00, 4 0.00)
8. true 6, predicted 4 (top 3: 4 1.00, 3 0.00, 7 0.00)
9. true 7, predicted 1 (top 3: 1 1.00, 4 0.00, 2 0.00)
10. true 9, predicted 4 (top 3: 4 1.00, 5 0.00, 1 0.00)
11. true 7, predicted 4 (top 3: 4 1.00, 5 0.00, 1 0.00)
12. true 0, predicted 4 (top 3: 4 1.00, 3 0.00, 7 0.00)
13. true 5, predicted 0 (top 3: 0 0.99, 3 0.01, 1 0.00)
14. true 3, predicted 0 (top 3: 0 1.00, 1 0.00, 3 0.00)
15. true 4, predicted 5 (top 3: 5 1.00, 4 0.00, 2 0.00)
16. true 5, predicted 3 (top 3: 3 1.00, 4 0.00, 0 0.00)

[image: mistakes.png]
