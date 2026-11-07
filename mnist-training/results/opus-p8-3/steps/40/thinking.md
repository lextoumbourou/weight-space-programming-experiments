I'm at about 86% accuracy with 11 steps left, so I'll probe three more features and then build. The biggest remaining confusions are 7 vs 9, then 6 vs 0. For 6 vs 0 I'm checking which features separate them: 0 has a much higher upper-right value (73% vs 21%), and its right-middle V is 74 against 12.

I'm now testing whether the top-right ink at row 1, column 3 separates 6 from 0, since 0 has its right side there and 6 doesn't. I'm also checking bottom-left ink at row 3 as a way to split 9 from 0.

I'm settling on a feature that checks for ink in the bottom-left corner, a threshold of 0.8 there to split 9 from 0. I'm also considering a top-left ink feature at threshold 0.4, which might separate 7's bar end from 9 and 5, and I'm confirming that a single-cell threshold of 0.4 works given how strong the blurred stroke signal is.
