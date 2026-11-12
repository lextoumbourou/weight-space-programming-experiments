Step 7 of 50: training loss 1.5617, accuracy 0.6031.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   855    16    33    10    15    17    44     0     1     0
               1     4  1019    27     0     0     5     0     8     0     1
               2    14    28   485   313    85     6    11    39     2     7
               3     4     7    13   800    20   151    10    15     8     2
               4     4   126    17     6   774     5    23     0     1    27
               5     7    10     9   224    23   553    61    14    12     2
               6    57    77    11    18   330   176   298     0     0     0
               7    26    54    55   108    29    12     1   729     0    76
               8     3   179   165    79    47    42    68   128   240    58
               9    24    76    42   128   307    31    16    58     1   278

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

At most 43 steps left. Reply with the complete build_weights() for step 8 in one Python code block.


Here are 16 training images your step 7 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 7, predicted 2 (top 3: 2 0.73, 3 0.26, 7 0.00)
2. true 6, predicted 4 (top 3: 4 0.98, 5 0.02, 8 0.00)
3. true 7, predicted 2 (top 3: 2 0.89, 7 0.10, 3 0.01)
4. true 6, predicted 1 (top 3: 1 0.77, 6 0.13, 8 0.03)
5. true 8, predicted 4 (top 3: 4 0.38, 2 0.36, 3 0.26)
6. true 5, predicted 7 (top 3: 7 0.49, 8 0.23, 2 0.15)
7. true 8, predicted 1 (top 3: 1 0.92, 6 0.03, 2 0.02)
8. true 7, predicted 2 (top 3: 2 0.71, 7 0.21, 3 0.08)
9. true 6, predicted 1 (top 3: 1 0.49, 8 0.17, 4 0.10)
10. true 0, predicted 6 (top 3: 6 0.88, 2 0.06, 4 0.05)
11. true 4, predicted 8 (top 3: 8 0.39, 1 0.33, 6 0.11)
12. true 2, predicted 4 (top 3: 4 0.80, 3 0.15, 2 0.05)
13. true 9, predicted 7 (top 3: 7 0.40, 9 0.35, 8 0.07)
14. true 8, predicted 1 (top 3: 1 0.99, 9 0.00, 7 0.00)
15. true 9, predicted 3 (top 3: 3 0.86, 5 0.13, 4 0.01)
16. true 6, predicted 5 (top 3: 5 0.55, 6 0.42, 4 0.01)

[image: mistakes.png]
