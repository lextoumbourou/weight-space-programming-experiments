Step 41 of 50: training loss 0.7935, accuracy 0.7540.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   803    13    68     0    16     7    52     0    24     8
               1     0   985    22     2    43     5     0     7     0     0
               2    48    11   639   130    41    19     5    27    52    18
               3     5     1    50   792     0   110     0     9    52    11
               4    12    24     9     0   839     4    10     1    15    69
               5     1    14     4    61     6   560    46     6   216     1
               6    40    44     2     0    71    33   751     0    22     4
               7     6     2    23    25    13    15     0   892     6   108
               8    12    47   188    17    12    62    18     9   580    64
               9    26    13     7     3    70    59     9    25    50   699

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

At most 9 steps left. Reply with the complete build_weights() for step 42 in one Python code block.


Here are 16 training images your step 41 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 4, predicted 8 (top 3: 8 0.39, 4 0.25, 9 0.22)
2. true 5, predicted 8 (top 3: 8 0.54, 3 0.21, 6 0.14)
3. true 2, predicted 8 (top 3: 8 0.59, 3 0.26, 2 0.10)
4. true 0, predicted 6 (top 3: 6 0.38, 2 0.24, 8 0.14)
5. true 5, predicted 8 (top 3: 8 0.69, 6 0.20, 5 0.05)
6. true 7, predicted 9 (top 3: 9 0.67, 8 0.14, 7 0.12)
7. true 5, predicted 8 (top 3: 8 0.73, 4 0.10, 3 0.10)
8. true 3, predicted 5 (top 3: 5 0.49, 3 0.45, 8 0.03)
9. true 9, predicted 2 (top 3: 2 0.28, 3 0.27, 9 0.20)
10. true 8, predicted 9 (top 3: 9 0.33, 8 0.30, 3 0.26)
11. true 5, predicted 8 (top 3: 8 0.46, 6 0.31, 5 0.10)
12. true 5, predicted 8 (top 3: 8 0.45, 6 0.14, 3 0.13)
13. true 5, predicted 8 (top 3: 8 0.41, 3 0.36, 6 0.07)
14. true 5, predicted 3 (top 3: 3 0.52, 8 0.37, 2 0.04)
15. true 9, predicted 8 (top 3: 8 0.72, 9 0.16, 6 0.10)
16. true 0, predicted 8 (top 3: 8 0.35, 6 0.21, 0 0.18)

[image: mistakes.png]
