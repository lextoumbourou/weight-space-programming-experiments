Step 6 of 50: training loss 1.1142, accuracy 0.6913.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   893    14    38     5     1     8    31     0     1     0
               1     4  1009    38     0     0     4     0     6     0     3
               2    25    18   613   210    39     6    15    25    17    22
               3    10     1    12   778     1   145     8    21    40    14
               4     6   108    31    13   622     4    44     5    13   137
               5    13     5    13   126     6   595    95    12    48     2
               6   117    33     9     7   104    82   591     0    24     0
               7    43    11    60    88     1     6     0   686     4   191
               8    25    74    94    17     4    14    66    80   491   144
               9    45    31    39    73    21    31    17    65     4   635

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.6349 | 0.3786
2 | 1.6757 | 0.5669
3 | 1.4210 | 0.5906
4 | 1.3284 | 0.6249
5 | 1.1885 | 0.6594
6 | 1.1142 | 0.6913

At most 44 steps left. Reply with the complete build_weights() for step 7 in one Python code block.


Here are 16 training images your step 6 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 5, predicted 8 (top 3: 8 0.57, 6 0.36, 5 0.05)
2. true 2, predicted 3 (top 3: 3 0.90, 2 0.10, 9 0.00)
3. true 6, predicted 2 (top 3: 2 0.54, 6 0.16, 4 0.15)
4. true 2, predicted 3 (top 3: 3 0.62, 2 0.35, 4 0.03)
5. true 8, predicted 1 (top 3: 1 0.70, 8 0.16, 9 0.08)
6. true 8, predicted 6 (top 3: 6 0.85, 8 0.14, 0 0.00)
7. true 8, predicted 9 (top 3: 9 0.88, 8 0.12, 7 0.00)
8. true 4, predicted 1 (top 3: 1 0.38, 7 0.20, 6 0.17)
9. true 7, predicted 9 (top 3: 9 0.92, 7 0.03, 3 0.03)
10. true 8, predicted 9 (top 3: 9 0.47, 7 0.20, 8 0.16)
11. true 9, predicted 8 (top 3: 8 0.52, 1 0.16, 6 0.11)
12. true 2, predicted 3 (top 3: 3 0.90, 4 0.05, 2 0.04)
13. true 9, predicted 5 (top 3: 5 0.70, 9 0.24, 3 0.05)
14. true 8, predicted 2 (top 3: 2 0.54, 7 0.29, 8 0.09)
15. true 6, predicted 0 (top 3: 0 0.99, 6 0.01, 8 0.00)
16. true 1, predicted 2 (top 3: 2 0.97, 8 0.01, 7 0.01)

[image: mistakes.png]
