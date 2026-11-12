Step 36 of 50: training loss 0.8409, accuracy 0.7319.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   798    15    34     0    13     3    93     0    30     5
               1     0   971    14     0    66     3     0    10     0     0
               2    35    13   573    91   124     4     7    16   121     6
               3     6     3    16   707     1   165     0    11   117     4
               4     5    25     4     0   892     2     6     1    19    29
               5     3    13     3    69    13   500    50     8   256     0
               6    30    28     0     1    98    14   765     0    31     0
               7     8     8    20     7    61    16     0   884     9    77
               8     7    86    63    10    20    37    15     9   723    39
               9    21    14     1     3   286    35     8    28    59   506

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

At most 14 steps left. Reply with the complete build_weights() for step 37 in one Python code block.


Here are 16 training images your step 36 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 2, predicted 3 (top 3: 3 0.33, 0 0.25, 2 0.20)
2. true 9, predicted 4 (top 3: 4 0.61, 9 0.27, 5 0.05)
3. true 9, predicted 4 (top 3: 4 0.74, 9 0.14, 8 0.06)
4. true 2, predicted 4 (top 3: 4 0.41, 3 0.29, 8 0.10)
5. true 9, predicted 8 (top 3: 8 0.45, 9 0.43, 4 0.05)
6. true 2, predicted 4 (top 3: 4 0.61, 6 0.10, 8 0.10)
7. true 9, predicted 4 (top 3: 4 0.50, 7 0.28, 9 0.12)
8. true 1, predicted 4 (top 3: 4 0.56, 5 0.11, 9 0.09)
9. true 1, predicted 2 (top 3: 2 0.65, 1 0.34, 8 0.01)
10. true 8, predicted 1 (top 3: 1 0.63, 2 0.13, 8 0.09)
11. true 9, predicted 4 (top 3: 4 0.36, 5 0.34, 8 0.15)
12. true 2, predicted 7 (top 3: 7 0.41, 2 0.28, 4 0.09)
13. true 3, predicted 7 (top 3: 7 0.32, 9 0.24, 3 0.13)
14. true 3, predicted 5 (top 3: 5 0.75, 3 0.13, 8 0.08)
15. true 6, predicted 4 (top 3: 4 0.49, 0 0.22, 9 0.16)
16. true 8, predicted 4 (top 3: 4 0.32, 8 0.20, 6 0.16)

[image: mistakes.png]
