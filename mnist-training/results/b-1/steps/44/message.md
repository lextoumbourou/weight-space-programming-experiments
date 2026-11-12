Step 43 of 50: training loss 0.7773, accuracy 0.7617.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   811    13    64     0     6     6    62     1    21     7
               1     0   981    24     2    39     5     0    13     0     0
               2    43     9   660   120    31    17     7    21    63    19
               3     6     1    35   776     0   134     0    14    53    11
               4    11    23    10     2   813     5    13     3    18    85
               5     4    11     3    77     4   561    55     9   191     0
               6    44    31     2     2    49    25   793     0    18     3
               7     6     2    20    17    12    17     0   926     6    84
               8    11    49   170    17     8    65    21    10   598    60
               9    25    12     4     6    68    69    11    31    37   698

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
32 | 0.8597 | 0.7340
33 | 0.8500 | 0.7380
34 | 0.8805 | 0.7238
35 | 0.8682 | 0.7310
36 | 0.8409 | 0.7319
37 | 0.8217 | 0.7448
38 | 0.8056 | 0.7534
39 | 0.7984 | 0.7570
40 | 0.7887 | 0.7604
41 | 0.7935 | 0.7540
42 | 0.7842 | 0.7616
43 | 0.7773 | 0.7617

At most 7 steps left. Reply with the complete build_weights() for step 44 in one Python code block.


Here are 16 training images your step 43 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 9, predicted 0 (top 3: 0 0.60, 6 0.24, 9 0.08)
2. true 8, predicted 2 (top 3: 2 0.68, 1 0.23, 8 0.04)
3. true 9, predicted 4 (top 3: 4 0.67, 9 0.23, 1 0.03)
4. true 8, predicted 2 (top 3: 2 0.78, 8 0.10, 6 0.04)
5. true 8, predicted 1 (top 3: 1 0.53, 2 0.36, 8 0.05)
6. true 8, predicted 2 (top 3: 2 0.42, 8 0.27, 7 0.10)
7. true 4, predicted 9 (top 3: 9 0.30, 6 0.27, 8 0.20)
8. true 5, predicted 8 (top 3: 8 0.50, 6 0.35, 5 0.06)
9. true 1, predicted 4 (top 3: 4 0.45, 5 0.24, 6 0.07)
10. true 3, predicted 8 (top 3: 8 0.47, 3 0.27, 2 0.11)
11. true 5, predicted 8 (top 3: 8 0.52, 3 0.35, 6 0.08)
12. true 7, predicted 3 (top 3: 3 0.29, 4 0.27, 9 0.16)
13. true 2, predicted 6 (top 3: 6 0.41, 4 0.32, 8 0.09)
14. true 8, predicted 2 (top 3: 2 0.77, 8 0.19, 1 0.02)
15. true 5, predicted 8 (top 3: 8 0.60, 6 0.16, 7 0.08)
16. true 6, predicted 8 (top 3: 8 0.47, 6 0.25, 9 0.12)

[image: mistakes.png]
