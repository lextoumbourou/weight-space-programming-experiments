I've got a best score of 0.7774 with 13 left, so I'm sticking with small steps. For the 3→8 pair, which still has 117 remaining, I'm going to make the negative weight for 8 stronger, moving it from 0.4 to 0.8, since 8 should be penalized when left-open cavities are present. For 3→5 at 103, 5 shares a left-open lower cavity and has an upper right-open one, while 3 has no right-open cavity, so I'm adding a negative for 3 on right-open cavities.

Next I'm adding a negative for 5 on left-open cavities at the upper region near (12, 8.5), since its upper cavity is right-open where 3's is left-open. For 2 against 3, I'll add a generic negative on left-open cavities at -0.3, since I can't clearly place a left-open region for 2. Then I'm recalculating the bias from the step 37 column sums.

Now I'm working through the bias recalculation, pulling the column totals into a rough sum for each row.

Now I'm applying the correction terms to each row, with a series of small numbers at the end pushing the bias values toward their final adjustments.
