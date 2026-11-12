Step 7 of 50: training loss 1.3141, accuracy 0.6005.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   953     4     6     0     0     0     3     1    24     0
               1     0   948    92     0     0    15     7     1     1     0
               2    60     6   567     6     2    14    68     2   265     0
               3     6     4    19   382     0   307     1     5   306     0
               4     9    25     6     0   693     4    38     0   207     1
               5    12     7     6     7     0   511    69     0   303     0
               6    96    12     1     0    37     7   735     0    79     0
               7    49    24    42     7    14    95     0   363   130   366
               8    12    56    66     0     3    26    32     3   808     3
               9    71    37     0     0   224    80     9     5   490    45

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

At most 43 steps left. Reply with the complete build_weights() for step 8 in one Python code block.


Here are 16 training images your step 7 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 2, predicted 8 (top 3: 8 0.87, 4 0.08, 0 0.03)
2. true 4, predicted 6 (top 3: 6 0.33, 4 0.30, 5 0.23)
3. true 7, predicted 2 (top 3: 2 0.65, 7 0.30, 8 0.03)
4. true 2, predicted 1 (top 3: 1 0.74, 2 0.21, 6 0.02)
5. true 7, predicted 9 (top 3: 9 0.90, 7 0.04, 5 0.04)
6. true 7, predicted 9 (top 3: 9 0.50, 7 0.35, 5 0.07)
7. true 4, predicted 8 (top 3: 8 0.55, 4 0.38, 9 0.03)
8. true 6, predicted 8 (top 3: 8 0.36, 5 0.31, 0 0.19)
9. true 9, predicted 8 (top 3: 8 0.38, 4 0.25, 5 0.20)
10. true 9, predicted 8 (top 3: 8 0.28, 4 0.27, 5 0.25)
11. true 9, predicted 4 (top 3: 4 0.46, 9 0.36, 8 0.12)
12. true 9, predicted 8 (top 3: 8 0.38, 5 0.33, 9 0.19)
13. true 9, predicted 8 (top 3: 8 0.62, 4 0.11, 9 0.10)
14. true 2, predicted 8 (top 3: 8 0.83, 2 0.09, 4 0.03)
15. true 9, predicted 8 (top 3: 8 0.87, 9 0.05, 5 0.05)
16. true 7, predicted 5 (top 3: 5 0.51, 9 0.19, 8 0.13)

[image: mistakes.png]
