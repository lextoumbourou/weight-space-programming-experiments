Step 45 of 50: training loss 0.7950, accuracy 0.7551.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   807    13    53     0     6     6    61     1    37     7
               1     0   981    24     2    39     5     0    13     0     0
               2    44     9   651   110    31    18     8    21    80    18
               3     6     1    34   772     0   141     0    14    48    14
               4    11    23    10     0   810     5    12     3    29    80
               5     4    11     2    25     3   544    43     6   277     0
               6    44    30     2     2    49    25   788     0    23     4
               7     6     2    20    18    12    17     0   926     5    84
               8    13    44   136    36     8    87    19    10   578    78
               9    25    12     4     7    68    70    10    31    40   694

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
44 | 0.7768 | 0.7617
45 | 0.7950 | 0.7551

At most 5 steps left. Reply with the complete build_weights() for step 46 in one Python code block.


Here are 16 training images your step 45 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 3, predicted 2 (top 3: 2 0.51, 3 0.26, 8 0.16)
2. true 7, predicted 9 (top 3: 9 0.53, 7 0.25, 5 0.11)
3. true 6, predicted 4 (top 3: 4 0.55, 6 0.41, 5 0.02)
4. true 8, predicted 5 (top 3: 5 0.56, 8 0.36, 3 0.06)
5. true 5, predicted 8 (top 3: 8 0.73, 6 0.09, 3 0.09)
6. true 0, predicted 5 (top 3: 5 0.32, 0 0.25, 6 0.24)
7. true 5, predicted 8 (top 3: 8 0.86, 6 0.05, 3 0.03)
8. true 4, predicted 9 (top 3: 9 0.53, 2 0.12, 8 0.11)
9. true 8, predicted 3 (top 3: 3 0.31, 9 0.29, 5 0.22)
10. true 2, predicted 8 (top 3: 8 0.72, 3 0.10, 2 0.08)
11. true 3, predicted 8 (top 3: 8 0.51, 3 0.29, 7 0.14)
12. true 7, predicted 9 (top 3: 9 0.85, 7 0.08, 8 0.04)
13. true 9, predicted 7 (top 3: 7 0.40, 9 0.24, 8 0.18)
14. true 3, predicted 5 (top 3: 5 0.38, 3 0.34, 0 0.17)
15. true 1, predicted 7 (top 3: 7 0.79, 3 0.07, 1 0.06)
16. true 0, predicted 6 (top 3: 6 0.67, 8 0.14, 2 0.13)

[image: mistakes.png]
