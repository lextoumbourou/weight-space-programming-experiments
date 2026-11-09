Step 7 of 15: validation loss 0.8792, accuracy 0.7403.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   708     0    34     0     0    13    27     0   207     2
               1     0   834   154     1     0     6     2    33    27     7
               2    30     2   614    76     2     3     3     9   242     9
               3     3     0     7   718     0   104     0     1   195     2
               4    13    13    14     2   503    14    48     2   178   196
               5     3     1     4    10     0   779    34    11    72     1
               6    37     2     8     0     3     5   886     0    25     1
               7    18     0    25    44     5   100     0   658    63   177
               8     0     1     9     4     1     2    10     3   968    11
               9    28     0     5    29     0    53    20     8    83   735

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 0.9176 | 0.7428
2 | 0.8203 | 0.7656
3 | 0.8671 | 0.7260
4 | 1.3566 | 0.5882
5 | 0.8736 | 0.7192
6 | 0.9409 | 0.7196
7 | 0.8792 | 0.7403

8 steps left. Reply with the complete build_weights() for step 8 in one Python code block.
