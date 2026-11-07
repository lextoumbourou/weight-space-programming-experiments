Now I'm tallying the predicted counts for each digit, with 8 the highest at 1161. The strongest remaining transitions are 8→2 and 2→8 at around 230 each, followed by the 3↔5, 7↔9, and 9↔4 pairs.

Now I'm weighing a small bias change for the step, with a structural tweak to the "1" classification to curb the 1→2 confusions, and I'm leaving the 3 and 5 biases where they are.

Now I'm weighing a bigger penalty for missing strokes, which I expect to help separate the dense digits from the partial matches, and I'm adding small compensating boosts to 8, 9, 0 and 6 so they don't lose ground to the others.

Now I'm running the same test with a stronger penalty for missing strokes, adding offsetting boosts so the dense digits don't fall behind the sparse ones.

Now I'm settling on a moderate-risk step: a stronger penalty for missing strokes, offset by small boosts to the dense digits so they don't lose out to the sparse ones.
