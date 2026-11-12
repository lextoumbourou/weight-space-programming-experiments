Step 15 of 50: training loss 1077.1201, accuracy 0.0622.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0    51    92   417    68    76   253     2     3    29     0
               1    67    26     2    49   457   116     1   102   244     0
               2   194   139    19   180   173    83    95    60    47     0
               3   319   198    23   278   120    13    64    13     2     0
               4    62    12     1   172    63     3   491   155    24     0
               5   393   129    12   189   151    17     9     9     6     0
               6   138    50     1   223   164    34   153   161    43     0
               7   298   453    36    93   137    38    19    15     1     0
               8   282   182     6   159   320     5    28    27     0     0
               9   433   237    13    97   148    15     6     9     3     0

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

At most 35 steps left. Reply with the complete build_weights() for step 16 in one Python code block.


Here are 16 training images your step 15 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 4, predicted 7 (top 3: 7 1.00, 6 0.00, 4 0.00)
2. true 0, predicted 8 (top 3: 8 1.00, 7 0.00, 5 0.00)
3. true 8, predicted 1 (top 3: 1 0.92, 4 0.08, 0 0.00)
4. true 4, predicted 3 (top 3: 3 0.96, 6 0.02, 4 0.02)
5. true 2, predicted 4 (top 3: 4 1.00, 1 0.00, 3 0.00)
6. true 1, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
7. true 2, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
8. true 8, predicted 1 (top 3: 1 0.98, 4 0.02, 2 0.00)
9. true 5, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
10. true 0, predicted 2 (top 3: 2 0.98, 5 0.02, 8 0.00)
11. true 5, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
12. true 0, predicted 5 (top 3: 5 1.00, 2 0.00, 8 0.00)
13. true 6, predicted 8 (top 3: 8 1.00, 5 0.00, 7 0.00)
14. true 7, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
15. true 5, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
16. true 1, predicted 4 (top 3: 4 1.00, 7 0.00, 3 0.00)

[image: mistakes.png]
