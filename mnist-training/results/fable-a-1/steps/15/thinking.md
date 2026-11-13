I'm decoding the three bits: bit0 is TR-lower (D), bit1 is BL-upper (E), and bit2 is BL-lower (F), so I'm mapping each outcome from 0 to 7 to its combination of D, E, and F. Then I'm writing out the sums for D, E, and F in terms of those outcomes, and starting to sort the outcomes into classes.

Now I'm tallying the per-class sums for D, E, and F, and checking the ratios as I go through classes 1 to 5.

Now I'm working through the per-class counts for classes 4 through 8, computing the D, E, and F shares for each. Class 8 comes out high on all three, around 92%, 92%, and 88%, and I'm moving on to class 9.

Now I'm tallying the per-class ratios for the BL-lower outcomes, and class 9 comes out at about 95% on TR-lower and 74.5% on BL-upper.

Now I'm checking the remaining zones, BR-upper and BR-lower, and weighing whether a third feature would help separate the pairs the corner zones still confuse, like 0 and 6.

I'm comparing the corner readings for the pairs that are still close, checking 0 against 6 on the top-right zones, and 2 against 8 on the bottom-left upper zone. For 2 against 3 and 9 against 7, the top-left lower, bottom-left upper, and top-right lower zones each give a clear gap.

I'm now comparing the remaining close pairs using the corner zones: for 5 versus 3, the top-right upper zone separates them sharply, and for 4 versus 9 the top-right and top-left upper zones do the same. I'm also checking 5 against 6, 8 against 9, 7 against 2, and 0 against 2, where the top-left and bottom-left zones each give a clear gap.

I'm checking 4 against 6 next, since their corner readings overlap and the bottom-right zones should help separate them. Then I'm looking at 3 against 8, 5 against 9, and 5 against 3, where the top-left lower and top-right upper zones each give a clear gap. I'm planning to add a third feature, maybe a hole or orientation template, to handle the cases the corner zones leave open.

I'm weighing a third feature to resolve the remaining close pairs, and I'm leaning toward a hole measure, which would need recalibrating with the four sizes. I'm considering a binary threshold on a lower or upper hole reading, and may combine it with the bottom-right zones.

I'm settling on the third feature: a binary test on the lower hole reading, H_lo above 0.05, which I'll wire into a general feature list that takes channels, rows, and a threshold.
