Step 10 of 50: training loss 0.9695, accuracy 0.6913.

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
7 | 1.5617 | 0.6031
8 | 1.1344 | 0.6834
9 | 1.9282 | 0.6363
10 | 0.9695 | 0.6913

At most 40 steps left. Reply with the complete build_weights() for step 11 in one Python code block.


Here are 16 training images your step 10 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 7, predicted 0 (top 3: 0 0.57, 9 0.24, 7 0.17)
2. true 8, predicted 6 (top 3: 6 0.32, 2 0.26, 8 0.17)
3. true 2, predicted 3 (top 3: 3 0.98, 2 0.01, 9 0.01)
4. true 6, predicted 1 (top 3: 1 0.79, 8 0.10, 6 0.10)
5. true 6, predicted 4 (top 3: 4 0.80, 5 0.20, 3 0.00)
6. true 4, predicted 3 (top 3: 3 0.34, 4 0.18, 9 0.16)
7. true 5, predicted 3 (top 3: 3 0.64, 2 0.15, 5 0.15)
8. true 5, predicted 6 (top 3: 6 0.67, 8 0.14, 5 0.05)
9. true 5, predicted 7 (top 3: 7 0.59, 1 0.20, 8 0.12)
10. true 2, predicted 7 (top 3: 7 0.21, 8 0.18, 5 0.17)
11. true 2, predicted 3 (top 3: 3 0.76, 2 0.13, 8 0.05)
12. true 0, predicted 6 (top 3: 6 0.84, 0 0.09, 8 0.07)
13. true 8, predicted 7 (top 3: 7 0.40, 8 0.30, 1 0.15)
14. true 9, predicted 7 (top 3: 7 0.39, 9 0.21, 1 0.14)
15. true 7, predicted 3 (top 3: 3 0.48, 7 0.27, 9 0.11)
16. true 8, predicted 7 (top 3: 7 0.52, 9 0.16, 2 0.15)

[image: mistakes.png]
