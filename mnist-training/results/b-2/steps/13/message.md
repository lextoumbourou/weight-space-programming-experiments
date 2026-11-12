Step 12 of 50: training loss 1107.3885, accuracy 0.0831.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0    32    35    54     7   104   244     4    24   487     0
               1   945    50     0    39    27     2     0     0     1     0
               2    40    25     4   161   130    32   342   216    40     0
               3    54   163   325    28   127   225     8    39    61     0
               4   130   142    19    69   185    31    33   286    88     0
               5    76   125   179    59   123   224    21    46    62     0
               6   170    36    21   361    83    81   138    45    32     0
               7    98   207   105   139   315    40    22   142    22     0
               8   335   151    57   154   111    48    67    58    28     0
               9   189   257    36    90   120    15    49   173    32     0

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

At most 38 steps left. Reply with the complete build_weights() for step 13 in one Python code block.


Here are 16 training images your step 12 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 2, predicted 1 (top 3: 1 0.98, 4 0.02, 2 0.00)
2. true 9, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
3. true 6, predicted 8 (top 3: 8 0.97, 5 0.03, 7 0.00)
4. true 8, predicted 1 (top 3: 1 0.97, 4 0.02, 0 0.01)
5. true 6, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
6. true 8, predicted 3 (top 3: 3 0.98, 4 0.02, 0 0.00)
7. true 5, predicted 4 (top 3: 4 0.67, 5 0.33, 7 0.00)
8. true 5, predicted 3 (top 3: 3 0.98, 4 0.02, 0 0.00)
9. true 0, predicted 8 (top 3: 8 1.00, 5 0.00, 2 0.00)
10. true 9, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
11. true 2, predicted 6 (top 3: 6 0.80, 3 0.18, 7 0.01)
12. true 7, predicted 1 (top 3: 1 0.98, 4 0.02, 0 0.00)
13. true 0, predicted 4 (top 3: 4 0.99, 1 0.01, 3 0.00)
14. true 9, predicted 2 (top 3: 2 0.98, 5 0.02, 1 0.00)
15. true 8, predicted 0 (top 3: 0 0.96, 1 0.02, 3 0.02)
16. true 0, predicted 2 (top 3: 2 0.98, 5 0.02, 8 0.00)

[image: mistakes.png]
