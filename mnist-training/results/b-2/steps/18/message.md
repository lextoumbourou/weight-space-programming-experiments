Step 17 of 50: training loss 1047.6190, accuracy 0.1387.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   210   156   205     8    70   235     0    12    95     0
               1    79    88     1    22   729    79     1    42    23     0
               2    66   165    72   134   227   107   102    82    35     0
               3   106   182    88   117   275   147    26    49    40     0
               4   136   424    73    41   186    47    15    47    14     0
               5    29    48    34    71   154   116   109   212   142     0
               6    25     6     0   225    56     6   548    83    18     0
               7   211   414    25    59   300    32     3    31    15     0
               8   126   364   117    56   218    57    17    35    19     0
               9   172   399    21    92   213    14    16    26     8     0

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

At most 33 steps left. Reply with the complete build_weights() for step 18 in one Python code block.


Here are 16 training images your step 17 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 7, predicted 0 (top 3: 0 0.64, 1 0.34, 3 0.01)
2. true 7, predicted 1 (top 3: 1 0.98, 4 0.02, 2 0.00)
3. true 5, predicted 4 (top 3: 4 0.93, 1 0.07, 5 0.00)
4. true 7, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
5. true 8, predicted 5 (top 3: 5 1.00, 4 0.00, 2 0.00)
6. true 9, predicted 1 (top 3: 1 0.98, 4 0.02, 0 0.00)
7. true 2, predicted 4 (top 3: 4 1.00, 5 0.00, 7 0.00)
8. true 1, predicted 4 (top 3: 4 1.00, 7 0.00, 3 0.00)
9. true 8, predicted 1 (top 3: 1 0.98, 4 0.02, 0 0.00)
10. true 8, predicted 1 (top 3: 1 0.98, 4 0.02, 0 0.00)
11. true 2, predicted 4 (top 3: 4 1.00, 7 0.00, 3 0.00)
12. true 7, predicted 0 (top 3: 0 0.95, 3 0.03, 1 0.02)
13. true 2, predicted 5 (top 3: 5 0.77, 4 0.23, 8 0.00)
14. true 1, predicted 4 (top 3: 4 1.00, 1 0.00, 3 0.00)
15. true 5, predicted 7 (top 3: 7 1.00, 4 0.00, 6 0.00)
16. true 4, predicted 1 (top 3: 1 0.98, 4 0.02, 0 0.00)

[image: mistakes.png]
