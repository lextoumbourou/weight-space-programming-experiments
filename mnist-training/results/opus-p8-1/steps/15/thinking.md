I'm decoding the three bits from cells (0,0), (0,1) and (0,2). For class 0 the probabilities of bit1 and bit2 come out to roughly 0.33 and 0.61, while bit0 is only about 0.04.

I'm working through the per-class tallies now: class 2 comes out to about 0.11 for bit0, 0.49 for bit1 and 0.41 for bit2. Class 3 and class 5 show strong bit1 and bit2 values, while class 6 has essentially nothing.

I'm weighing whether to keep going with the remaining tests one at a time, which would take about 21 more steps, or to see if a fourth test could be folded in alongside the others.

I'm ruling out a fourth test: with only two spare categories, adding it would blur the marginals I already have, so I'll skip it. Next I'll move on to the cells at (0,3), (0,4) and (0,5).
