Step 2 of 50: validation loss 1.2629, accuracy 0.5742.

Confusion matrix (rows: true digit, columns: predicted digit):

true \ predicted     0     1     2     3     4     5     6     7     8     9
               0   751    10   160    17     0     2    48     2     0     1
               1     1   895     6     0     6     6    35   112     3     0
               2    11    45   648    65    34     0    35    52    61    39
               3     2     4    89   656     0   154    33    59    27     6
               4     4   103    30     0   350     2    54    84    39   317
               5     6     9    38    83     0   629    84     8    57     1
               6   242    57    28    13    44   111   413     0    43    16
               7     8    43    47    29     8    10     3   714     3   225
               8    15    89   265    37     3    25   159   165   148   103
               9    61    47    79    23    13    30    26   116    28   538

History (validation set, 10,000 images):

step | loss | accuracy
---- | ---- | --------
1 | 2.9468 | 0.2540
2 | 1.2629 | 0.5742

48 steps left. Reply with the complete build_weights() for step 3 in one Python code block.
