Step 14 of 50: training loss 0.8973, accuracy 0.7265.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   873    18    47     8     0    16    29     0     0     0
               1     0  1028    14     0     1     1     0     6    12     2
               2    25    28   803    10    24     4    23    16    51     6
               3    12     3    39   580    20   125    13   124    83    31
               4     3   123     4     0   735     0    35     3    19    61
               5     9     6     4    96     4   552   137    32    69     6
               6    54    33     0     0    81    72   715     0    12     0
               7    24    32    42    18    10     9     1   792    22   140
               8    42    52    52    16    11    32    73    53   607    71
               9    44    39    23    17    55    14    33   114    42   580

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

At most 36 steps left. Reply with the complete build_weights() for step 15 in one Python code block.


Here are 16 training images your step 14 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 2, predicted 1 (top 3: 1 0.28, 7 0.19, 2 0.17)
2. true 6, predicted 5 (top 3: 5 0.59, 6 0.32, 4 0.03)
3. true 4, predicted 9 (top 3: 9 0.50, 1 0.26, 8 0.08)
4. true 8, predicted 2 (top 3: 2 0.53, 7 0.22, 8 0.11)
5. true 9, predicted 0 (top 3: 0 0.98, 7 0.01, 2 0.01)
6. true 5, predicted 9 (top 3: 9 0.37, 5 0.16, 7 0.15)
7. true 3, predicted 5 (top 3: 5 0.34, 0 0.27, 3 0.22)
8. true 5, predicted 9 (top 3: 9 0.42, 5 0.40, 3 0.06)
9. true 8, predicted 2 (top 3: 2 0.24, 6 0.21, 4 0.20)
10. true 3, predicted 7 (top 3: 7 0.65, 8 0.10, 3 0.10)
11. true 5, predicted 3 (top 3: 3 0.54, 5 0.42, 4 0.02)
12. true 8, predicted 7 (top 3: 7 0.36, 8 0.15, 5 0.15)
13. true 8, predicted 9 (top 3: 9 0.49, 8 0.26, 5 0.09)
14. true 9, predicted 7 (top 3: 7 0.57, 9 0.22, 4 0.05)
15. true 2, predicted 0 (top 3: 0 0.85, 2 0.13, 7 0.02)
16. true 9, predicted 2 (top 3: 2 0.52, 0 0.23, 4 0.13)

[image: mistakes.png]
