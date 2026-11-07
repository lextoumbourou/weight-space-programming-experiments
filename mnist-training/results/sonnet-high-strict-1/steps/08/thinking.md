I'm trying a few weight changes on the narrow channels, cutting the broad ones to about half, since the broad blur may just be adding noise. The confusions I'm still seeing are 2 to 4, 7 to 9, 5 to 6, and 1 to 7, and 8 is scattered. For 7 versus 9, I'm looking at the loop at the top of the 9 as the distinguishing feature.

Next I'm lowering the bias on 9 by about 0.15 and raising 7 by 0.1, since the loop-side stroke on 9 is what separates it from 7. For 2 versus 4, I'm checking the bottom bar and the column totals, and trying a small drop on the 4 bias.

I'm working through the digit-6 and digit-1 biases now, dropping 6 by about 0.2 and 1 by a similar amount. I'm also weighing whether to scale the narrow channels up around 1.3 and leave the broad ones at 1.0, which would shift the logit scale a bit, though I'll keep the bias adjustments modest.

Ah, that fragment is just the tail of a word, so there's nothing new to add; I'm still weighing the bias changes for 6 and 1 and whether scaling the narrow channels up is worth the shift in logit scale.
