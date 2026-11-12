Step 21 of 50: training loss 1244.8506, accuracy 0.0423.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0    17    16     0     8   332   144     0    52   422     0
               1   801    13     1   165    55     1     1    20     7     0
               2     1     8     0     0    77   131     0   111   662     0
               3     5     2     0     2   211    78     0   260   472     0
               4    11     4     0    50   225    28     6   455   204     0
               5     6     1     0    31   162    29    19   300   367     0
               6     3    13     2     4   178   459     0    13   295     0
               7   469    64     0   135   309    41     0    38    34     0
               8    94    37     0    40   546    88     2   103    99     0
               9    39     4     0   161   334     3    11   351    58     0

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

At most 29 steps left. Reply with the complete build_weights() for step 22 in one Python code block.


Here are 16 training images your step 21 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 6, predicted 5 (top 3: 5 1.00, 4 0.00, 2 0.00)
2. true 7, predicted 4 (top 3: 4 1.00, 3 0.00, 7 0.00)
3. true 2, predicted 5 (top 3: 5 1.00, 8 0.00, 4 0.00)
4. true 0, predicted 5 (top 3: 5 1.00, 4 0.00, 8 0.00)
5. true 1, predicted 0 (top 3: 0 1.00, 1 0.00, 3 0.00)
6. true 8, predicted 4 (top 3: 4 1.00, 3 0.00, 1 0.00)
7. true 8, predicted 5 (top 3: 5 1.00, 2 0.00, 8 0.00)
8. true 3, predicted 8 (top 3: 8 1.00, 7 0.00, 5 0.00)
9. true 5, predicted 4 (top 3: 4 0.61, 7 0.39, 3 0.00)
10. true 7, predicted 3 (top 3: 3 1.00, 0 0.00, 4 0.00)
11. true 6, predicted 8 (top 3: 8 1.00, 7 0.00, 5 0.00)
12. true 5, predicted 8 (top 3: 8 1.00, 7 0.00, 5 0.00)
13. true 0, predicted 7 (top 3: 7 1.00, 8 0.00, 4 0.00)
14. true 7, predicted 0 (top 3: 0 1.00, 3 0.00, 1 0.00)
15. true 4, predicted 8 (top 3: 8 1.00, 7 0.00, 5 0.00)
16. true 3, predicted 7 (top 3: 7 1.00, 8 0.00, 6 0.00)

[image: mistakes.png]
