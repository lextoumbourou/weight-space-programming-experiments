Step 19 of 50: training loss 0.8330, accuracy 0.7360.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   811    22    84    13     0    21    30     0     8     2
               1     0  1006    18     0     0     2     0     5    33     0
               2     9    41   802    10     6     5    15    18    81     3
               3     2     4    32   651     5   110    11    89    97    29
               4     2   142    14     0   667     0    15     9    94    40
               5     2     8     5   119     2   516   132    27    97     7
               6    28    20     3     2     3    23   862     0    26     0
               7     4    25    40    19    12     4     0   846    40   100
               8    12    27    54    28     9    23    39    55   684    78
               9    20    19    29    20    63    13    16   167    99   515

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

At most 31 steps left. Reply with the complete build_weights() for step 20 in one Python code block.


Here are 16 training images your step 19 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 8, predicted 3 (top 3: 3 0.44, 5 0.21, 6 0.13)
2. true 5, predicted 3 (top 3: 3 0.50, 5 0.48, 9 0.01)
3. true 9, predicted 4 (top 3: 4 0.39, 9 0.33, 8 0.10)
4. true 3, predicted 5 (top 3: 5 0.63, 3 0.36, 4 0.01)
5. true 3, predicted 8 (top 3: 8 0.37, 6 0.13, 2 0.13)
6. true 2, predicted 7 (top 3: 7 0.44, 2 0.44, 0 0.05)
7. true 3, predicted 1 (top 3: 1 0.29, 8 0.23, 5 0.09)
8. true 8, predicted 5 (top 3: 5 0.31, 3 0.30, 0 0.22)
9. true 3, predicted 8 (top 3: 8 0.70, 9 0.10, 6 0.07)
10. true 3, predicted 4 (top 3: 4 0.68, 3 0.08, 8 0.07)
11. true 5, predicted 8 (top 3: 8 0.31, 2 0.29, 6 0.19)
12. true 4, predicted 1 (top 3: 1 0.50, 9 0.34, 4 0.10)
13. true 4, predicted 8 (top 3: 8 0.59, 1 0.21, 6 0.06)
14. true 4, predicted 1 (top 3: 1 0.48, 8 0.25, 4 0.11)
15. true 8, predicted 6 (top 3: 6 0.43, 8 0.22, 2 0.11)
16. true 5, predicted 6 (top 3: 6 0.31, 8 0.23, 3 0.17)

[image: mistakes.png]
