I'm checking the results so far: digits 0, 4 and 7 are now classified correctly, but 1 is mostly being predicted as 6, and 6 is over-predicted overall. The bias changes on the 1 and 6 rows were too large, so I'm lowering the bias for 6 from 0.8 to -0.2.

I'm lowering the bias for 4 and raising it for 1, 8, 9 and 0, since those are the classes being under-predicted. The column sums show 6 and 4 well over the roughly 1000 target, while 1, 8 and 9 sit far below it. I'll adjust them step by step until the predicted counts level out.

I'm estimating the bias corrections as a log of target over predicted count, scaled by about 0.8, which gives a shift of roughly +1.4 for class 1 and -0.76 for class 6. Applying those shifts to the current biases yields new values of about 1.06 for 0, 1.1 for 1, 0.56 for 3 and 0.03 for 4.

Now I'm settling the final bias values for classes 3 through 9, and I'll also consider whether the features need a small improvement. For this step I'm sticking to bias tuning alone to see its effect.
