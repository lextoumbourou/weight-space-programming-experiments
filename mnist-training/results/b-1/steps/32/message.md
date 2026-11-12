Step 31 of 50: training loss 0.8709, accuracy 0.7170.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   838    16    17     0     3     4    85     0    19     9
               1     0  1006    17     0    25     6     2     8     0     0
               2    42    25   552    97    72    22    23    17   121    19
               3     6     2    11   646     0   271     0     8    77     9
               4     1    24     3     0   827     0    18     2    14    94
               5     4    14     3    67     4   610    50     6   157     0
               6    39    27     0     0   102    42   738     0    16     3
               7     9     4     9     6    68    31     0   860     2   101
               8     5    97    74    33    14    83    22    17   539   125
               9    17    13     2     1   255    67    11    26    15   554

History (training set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 1.4479 | 0.5465
2 | 1.4511 | 0.5327
3 | 1.6403 | 0.4871
4 | 1.6386 | 0.5078
5 | 2.7367 | 0.4958
6 | 2.3875 | 0.4751
7 | 5.6237 | 0.2327
8 | 1.8055 | 0.4696
9 | 1.9854 | 0.4561
10 | 1.5771 | 0.5330
11 | 1.8457 | 0.4671
12 | 2.1344 | 0.4372
13 | 1.9350 | 0.5070
14 | 4.0279 | 0.4305
15 | 1.3307 | 0.6072
16 | 1.1902 | 0.6406
17 | 1.3253 | 0.6170
18 | 1.0953 | 0.6732
19 | 1.0859 | 0.6762
20 | 1.0582 | 0.6870
21 | 1.0690 | 0.7032
22 | 1.0120 | 0.7094
23 | 0.9694 | 0.7188
24 | 0.9191 | 0.7269
25 | 0.9104 | 0.7289
26 | 0.9694 | 0.7285
27 | 0.8722 | 0.7285
28 | 0.8638 | 0.7285
29 | 0.8738 | 0.7332
30 | 0.8570 | 0.7372
31 | 0.8709 | 0.7170

At most 19 steps left. Reply with the complete build_weights() for step 32 in one Python code block.


Here are 16 training images your step 31 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 9, predicted 4 (top 3: 4 0.72, 5 0.12, 9 0.09)
2. true 2, predicted 0 (top 3: 0 0.61, 2 0.36, 3 0.01)
3. true 8, predicted 9 (top 3: 9 0.49, 8 0.21, 3 0.15)
4. true 8, predicted 5 (top 3: 5 0.28, 9 0.27, 3 0.25)
5. true 3, predicted 5 (top 3: 5 0.77, 3 0.15, 8 0.07)
6. true 8, predicted 1 (top 3: 1 0.46, 2 0.29, 8 0.12)
7. true 6, predicted 4 (top 3: 4 0.59, 9 0.18, 0 0.08)
8. true 3, predicted 8 (top 3: 8 0.42, 5 0.26, 9 0.16)
9. true 2, predicted 9 (top 3: 9 0.33, 4 0.21, 5 0.14)
10. true 6, predicted 8 (top 3: 8 0.61, 6 0.36, 0 0.03)
11. true 8, predicted 5 (top 3: 5 0.38, 8 0.24, 3 0.12)
12. true 8, predicted 3 (top 3: 3 0.33, 5 0.29, 8 0.24)
13. true 6, predicted 4 (top 3: 4 0.61, 6 0.15, 5 0.14)
14. true 2, predicted 5 (top 3: 5 0.33, 6 0.28, 3 0.16)
15. true 2, predicted 3 (top 3: 3 0.40, 8 0.22, 4 0.13)
16. true 2, predicted 8 (top 3: 8 0.58, 9 0.15, 3 0.12)

[image: mistakes.png]
