Step 11 of 50: training loss 0.9275, accuracy 0.7032.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   888    13    37     4     1    10    36     0     2     0
               1     4  1002    40     0     0     4     0     6     3     5
               2    24    14   619   187    45     7    15    25    36    18
               3     7     0    15   744     1   162     8    24    56    13
               4     4    92    28    11   642     4    43     4    26   129
               5    11     3    11   108     7   602    90    11    70     2
               6    92    20     9     5   113    78   613     0    37     0
               7    38     7    59    76     3     9     0   701     8   189
               8    23    38    75    16     6    12    62    60   596   121
               9    42    25    40    65    28    35    20    67    14   625

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

At most 39 steps left. Reply with the complete build_weights() for step 12 in one Python code block.


Here are 16 training images your step 11 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 8, predicted 2 (top 3: 2 0.46, 8 0.25, 7 0.13)
2. true 5, predicted 9 (top 3: 9 0.59, 5 0.15, 8 0.08)
3. true 2, predicted 3 (top 3: 3 0.44, 2 0.32, 9 0.07)
4. true 5, predicted 2 (top 3: 2 0.25, 8 0.22, 7 0.17)
5. true 8, predicted 1 (top 3: 1 0.29, 8 0.27, 7 0.24)
6. true 4, predicted 9 (top 3: 9 0.38, 4 0.33, 8 0.10)
7. true 3, predicted 5 (top 3: 5 0.66, 3 0.34, 6 0.00)
8. true 4, predicted 1 (top 3: 1 0.66, 8 0.13, 6 0.07)
9. true 2, predicted 1 (top 3: 1 0.40, 8 0.23, 4 0.11)
10. true 8, predicted 1 (top 3: 1 0.50, 8 0.38, 7 0.04)
11. true 4, predicted 9 (top 3: 9 0.65, 8 0.21, 4 0.09)
12. true 7, predicted 9 (top 3: 9 0.58, 7 0.24, 3 0.13)
13. true 5, predicted 3 (top 3: 3 0.47, 5 0.38, 8 0.06)
14. true 4, predicted 9 (top 3: 9 0.69, 1 0.16, 4 0.07)
15. true 9, predicted 7 (top 3: 7 0.30, 2 0.24, 8 0.21)
16. true 4, predicted 9 (top 3: 9 0.78, 4 0.08, 5 0.06)

[image: mistakes.png]
