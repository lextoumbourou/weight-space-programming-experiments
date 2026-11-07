I'm decoding the three features from the first row, then running the same calculation on the second row.

I'm working through the remaining rows, checking each feature's sum and comparing the scores across digits. Digit 7 scores highest on F1 and 9 scores low, which separates them clearly. For F2, digit 5 stands out well above 3.

I'm nudging the bias for digit 7 up by 0.2 to 0.4, since adding F1 will already push its predictions higher. For these single-cell features, I'm setting the threshold at 0.4, which gives m=0.8, with λ at 0.4.
