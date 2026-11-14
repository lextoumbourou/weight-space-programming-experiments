I'm decoding the three bits from the voltage thresholds: b1 comes from V(r0,L), b2 from V(r0,R), and b3 from V(r3,C), each compared against 0.6. For input 0 with value 991, I'm summing the relevant readings for each bit and dividing by 991, getting about 0.393 for b1, 0.687 for b2, and 0.253 for b3.

Now I'm working through the remaining inputs, checking b1, b2 and b3 against the 0.6 threshold for each one.

Now I'm checking the remaining readings for inputs 8 and 9 against the 0.6 threshold, and pulling out the V(r0,L) values that sit above it.

I'm checking the remaining voltage readings for each input against the 0.6 threshold, looking for the sharpest separations. On the left side, input 4 stands out against input 9, and on the right side input 5 is far below input 3. For the center reading, most values clearly fall on one side of the threshold, though input 8 sits unusually high and I'm double-checking it.

Now I'm working out the voltage-weighted means for each reading, checking them against the threshold values for the left, right and center taps.

I'm working out the per-digit means for the remaining voltage readings, comparing each against the 0.6 threshold. Then I want to pick a probe input that separates the most common confusions, like 7 versus 9 and 3 versus 5.

I'm now testing which stroke features separate the confusable digits: the lower-left arc should distinguish 0 from 2, and the upper-right arc should split 0 and 2 while separating 3 from 5. For 7 versus 9, the upper-right corner doesn't help, so I'm looking at the left-side bar instead.

I'm considering which stroke features to test next: one arc on the right side at the middle row, another on the left side at the lower row, and a horizontal bar across the top-right, since that bar would separate 5 and 7 from the others.
