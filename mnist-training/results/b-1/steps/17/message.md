Step 16 of 50: training loss 1.1902, accuracy 0.6406.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   758     9    20     2     0    29   160     2    10     1
               1     0   980    58    11     0     6     2     7     0     0
               2    30    10   645   106    55    44    73    17     9     1
               3     5     7    42   603     4   338     2    19     7     3
               4     3    34     6     8   799     2    89     7     6    29
               5     3    24    26   146     2   528   129     5    52     0
               6    18    52     2    13    69    23   789     0     1     0
               7     7    12    27    27    40    72     1   873     4    27
               8     3   105   232   244     3   225    57    34    87    19
               9    20    34     3    39   252   115    36   113     5   344

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

At most 34 steps left. Reply with the complete build_weights() for step 17 in one Python code block.


Here are 16 training images your step 16 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 6, predicted 1 (top 3: 1 0.46, 6 0.26, 3 0.21)
2. true 7, predicted 4 (top 3: 4 0.29, 3 0.26, 7 0.23)
3. true 2, predicted 0 (top 3: 0 0.92, 2 0.06, 4 0.02)
4. true 7, predicted 4 (top 3: 4 0.43, 5 0.21, 3 0.17)
5. true 7, predicted 4 (top 3: 4 0.81, 5 0.11, 9 0.07)
6. true 3, predicted 5 (top 3: 5 0.78, 3 0.22, 8 0.00)
7. true 0, predicted 2 (top 3: 2 0.41, 1 0.24, 3 0.17)
8. true 8, predicted 3 (top 3: 3 0.49, 6 0.18, 2 0.14)
9. true 0, predicted 6 (top 3: 6 0.59, 0 0.22, 5 0.10)
10. true 8, predicted 3 (top 3: 3 0.54, 2 0.18, 5 0.13)
11. true 8, predicted 5 (top 3: 5 0.67, 3 0.15, 8 0.06)
12. true 9, predicted 7 (top 3: 7 0.61, 3 0.23, 9 0.06)
13. true 3, predicted 5 (top 3: 5 0.59, 3 0.27, 7 0.07)
14. true 3, predicted 5 (top 3: 5 0.55, 3 0.41, 8 0.02)
15. true 5, predicted 6 (top 3: 6 0.35, 8 0.25, 5 0.18)
16. true 5, predicted 6 (top 3: 6 0.37, 5 0.25, 8 0.18)

[image: mistakes.png]
