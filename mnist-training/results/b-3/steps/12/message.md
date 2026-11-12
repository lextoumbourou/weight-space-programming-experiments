Step 11 of 50: training loss 4.5635, accuracy 0.4265.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   811   102    61     3     0     0     0    14     0     0
               1     0  1062     1     0     0     0     0     1     0     0
               2     4   301   542    22     0     0     0   121     0     0
               3     2   310    66   338     0     5     7   300     0     2
               4     4   633    16     2    45     0     0    75     0   208
               5    13   438    56   138     0   107    38   104     0    21
               6    48   471    94    12    16     1   323     2     0     0
               7     3   179     3     0     1     0     0   897     0     7
               8    31   607   129    15     0     0    15   210     0     2
               9    11   452    14     3     0     1     0   340     0   140

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5011 | 0.5277
2 | 1.1869 | 0.6212
3 | 2.0915 | 0.5810
4 | 2.1250 | 0.3982
5 | 1.3466 | 0.5185
6 | 1.1621 | 0.6170
7 | 1.3141 | 0.6005
8 | 1.1417 | 0.6499
9 | 3.4269 | 0.4356
10 | 1.5914 | 0.6284
11 | 4.5635 | 0.4265

At most 39 steps left. Reply with the complete build_weights() for step 12 in one Python code block.


Here are 16 training images your step 11 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 2, predicted 1 (top 3: 1 0.58, 7 0.35, 2 0.07)
2. true 9, predicted 7 (top 3: 7 0.87, 9 0.11, 1 0.02)
3. true 4, predicted 7 (top 3: 7 0.72, 1 0.28, 2 0.00)
4. true 2, predicted 1 (top 3: 1 0.97, 7 0.03, 2 0.00)
5. true 4, predicted 1 (top 3: 1 1.00, 7 0.00, 4 0.00)
6. true 6, predicted 1 (top 3: 1 0.67, 6 0.16, 0 0.12)
7. true 8, predicted 1 (top 3: 1 0.53, 7 0.28, 2 0.09)
8. true 4, predicted 1 (top 3: 1 1.00, 7 0.00, 2 0.00)
9. true 6, predicted 1 (top 3: 1 0.60, 7 0.24, 2 0.12)
10. true 5, predicted 1 (top 3: 1 0.99, 7 0.01, 2 0.00)
11. true 3, predicted 7 (top 3: 7 0.95, 1 0.04, 2 0.00)
12. true 9, predicted 1 (top 3: 1 0.67, 7 0.33, 9 0.00)
13. true 5, predicted 3 (top 3: 3 0.57, 2 0.22, 5 0.11)
14. true 8, predicted 1 (top 3: 1 0.91, 7 0.09, 2 0.00)
15. true 4, predicted 1 (top 3: 1 1.00, 4 0.00, 7 0.00)
16. true 8, predicted 3 (top 3: 3 0.66, 5 0.14, 2 0.13)

[image: mistakes.png]
