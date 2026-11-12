Step 5 of 50: training loss 1.3466, accuracy 0.5185.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   815     8    92     0    47    24     0     4     0     1
               1     0   790    70     0    77     0     0   127     0     0
               2     8     3   516     9   405    12     2    11     0    24
               3     2     1    64   511   102   331     1    17     0     1
               4     0    12    28     0   913     0     1    29     0     0
               5     2     3    22    63    72   734    13     6     0     0
               6    31    12    21    14   576    47   261     5     0     0
               7     4    12    78     1   191    14     0   599     0   191
               8    17    44   275    56   237    83    84   129    15    69
               9     9    11    52     0   758    38     1    61     0    31

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.5011 | 0.5277
2 | 1.1869 | 0.6212
3 | 2.0915 | 0.5810
4 | 2.1250 | 0.3982
5 | 1.3466 | 0.5185

At most 45 steps left. Reply with the complete build_weights() for step 6 in one Python code block.


Here are 16 training images your step 5 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 9, predicted 5 (top 3: 5 0.35, 0 0.28, 2 0.13)
2. true 4, predicted 2 (top 3: 2 0.29, 4 0.29, 7 0.26)
3. true 9, predicted 4 (top 3: 4 0.82, 5 0.07, 9 0.04)
4. true 2, predicted 4 (top 3: 4 0.34, 9 0.24, 2 0.18)
5. true 2, predicted 4 (top 3: 4 0.41, 2 0.39, 6 0.12)
6. true 6, predicted 4 (top 3: 4 0.30, 6 0.18, 5 0.15)
7. true 9, predicted 4 (top 3: 4 0.47, 7 0.21, 5 0.10)
8. true 6, predicted 2 (top 3: 2 0.34, 7 0.29, 6 0.14)
9. true 4, predicted 1 (top 3: 1 0.45, 4 0.38, 9 0.10)
10. true 7, predicted 9 (top 3: 9 0.63, 7 0.14, 3 0.09)
11. true 5, predicted 3 (top 3: 3 0.42, 5 0.36, 4 0.12)
12. true 6, predicted 4 (top 3: 4 0.35, 6 0.35, 1 0.08)
13. true 1, predicted 4 (top 3: 4 0.39, 1 0.25, 7 0.08)
14. true 6, predicted 1 (top 3: 1 0.46, 7 0.18, 4 0.18)
15. true 8, predicted 2 (top 3: 2 0.28, 8 0.15, 5 0.15)
16. true 2, predicted 4 (top 3: 4 0.91, 2 0.02, 9 0.01)

[image: mistakes.png]
