Step 8 of 50: training loss 1.1417, accuracy 0.6499.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   956     4    16     0     0     0     4     1    10     0
               1     0   939    96     1     0    15     7     6     0     0
               2    58     5   636    19     5    10    75     2   179     1
               3     5     4    14   621     1   271     2     6   104     2
               4     7    28    14     0   771     3    47     3   103     7
               5    11     7     8    44     1   568    99     2   175     0
               6    95    11     1     0    43    14   770     0    33     0
               7    36    17    37    25    24    41     1   422    59   428
               8    23    60   116     3     4    36    61    15   677    14
               9    74    35     2     2   280    89    25    20   295   139

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

At most 42 steps left. Reply with the complete build_weights() for step 9 in one Python code block.


Here are 16 training images your step 8 network got wrong, chosen at random from its mistakes, numbered left
to right and top to bottom, shown 4x enlarged with ink in white:

1. true 3, predicted 5 (top 3: 5 0.48, 8 0.37, 3 0.10)
2. true 6, predicted 4 (top 3: 4 0.41, 6 0.34, 8 0.14)
3. true 2, predicted 8 (top 3: 8 0.65, 4 0.23, 6 0.08)
4. true 8, predicted 1 (top 3: 1 0.42, 6 0.35, 8 0.09)
5. true 9, predicted 4 (top 3: 4 0.40, 5 0.32, 9 0.21)
6. true 4, predicted 8 (top 3: 8 0.44, 4 0.40, 3 0.07)
7. true 2, predicted 8 (top 3: 8 0.41, 0 0.27, 4 0.14)
8. true 7, predicted 8 (top 3: 8 0.66, 2 0.13, 4 0.08)
9. true 9, predicted 5 (top 3: 5 0.45, 9 0.16, 8 0.12)
10. true 2, predicted 6 (top 3: 6 0.76, 2 0.14, 8 0.05)
11. true 7, predicted 9 (top 3: 9 0.91, 3 0.03, 7 0.03)
12. true 2, predicted 6 (top 3: 6 0.98, 8 0.01, 4 0.01)
13. true 4, predicted 1 (top 3: 1 0.99, 8 0.00, 7 0.00)
14. true 9, predicted 0 (top 3: 0 0.46, 5 0.45, 8 0.05)
15. true 9, predicted 5 (top 3: 5 0.28, 8 0.20, 6 0.16)
16. true 4, predicted 8 (top 3: 8 0.46, 4 0.34, 6 0.15)

[image: mistakes.png]
