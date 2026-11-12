Step 17 of 50: training loss 1.3253, accuracy 0.6170.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   699     6     3     0     0     0     5     0   270     8
               1     0   969    68    14     0     3     3     3     3     1
               2    22    12   596    76     1     0    27     5   223    28
               3     2     6    36   598     0    52     3     6   313    14
               4     6    21     3     1   312     1     4     0   145   490
               5     3    12    13    63     0   218    22     2   574     8
               6    20    46     1    20    27     0   694     0   115    44
               7    10    14    36    16     3     4     0   677    44   286
               8     3    76   104    86     0     2     3     4   627   104
               9    16    27     0    13     5     1     1    26    92   780

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

At most 33 steps left. Reply with the complete build_weights() for step 18 in one Python code block.


Here are 16 training images your step 17 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 2, predicted 6 (top 3: 6 0.31, 3 0.26, 8 0.22)
2. true 5, predicted 8 (top 3: 8 0.82, 6 0.10, 5 0.04)
3. true 3, predicted 9 (top 3: 9 0.53, 3 0.35, 7 0.06)
4. true 9, predicted 8 (top 3: 8 0.70, 2 0.16, 9 0.10)
5. true 8, predicted 1 (top 3: 1 0.27, 3 0.25, 8 0.18)
6. true 5, predicted 1 (top 3: 1 0.69, 8 0.24, 6 0.05)
7. true 4, predicted 9 (top 3: 9 0.55, 4 0.34, 8 0.09)
8. true 7, predicted 3 (top 3: 3 0.47, 9 0.22, 1 0.20)
9. true 7, predicted 9 (top 3: 9 0.85, 7 0.05, 8 0.05)
10. true 5, predicted 8 (top 3: 8 0.46, 2 0.40, 0 0.08)
11. true 0, predicted 8 (top 3: 8 0.47, 9 0.22, 6 0.21)
12. true 5, predicted 8 (top 3: 8 0.87, 5 0.04, 3 0.04)
13. true 2, predicted 8 (top 3: 8 0.82, 2 0.10, 9 0.05)
14. true 4, predicted 9 (top 3: 9 0.64, 8 0.25, 4 0.07)
15. true 9, predicted 1 (top 3: 1 0.25, 9 0.24, 8 0.24)
16. true 3, predicted 2 (top 3: 2 0.96, 3 0.02, 8 0.01)

[image: mistakes.png]
