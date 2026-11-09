I'm decoding the bit pattern so that k equals top plus twice mid plus four times bot, and listing what each value of k means. For digit 0 with N=991, most of the weight sits at k=4 and k=5, and I'm estimating the top-bit probability from those counts.

I'm working through the remaining digits' bit-probabilities: for digit 1 the top-bit chance comes out around .028, and the mid and bot chances are about .004 and .054. Digits 2 through 5 are next, where I'm comparing the top, mid and bot shares across each digit's counts.

Now I'm checking the top, mid and bot shares for digit 8, with N=1009, and the top-bit share comes out to .942.

I'm finishing the digit 9 shares, where the top-bit chance is about .974 and the mid-bit chance about .903, then collecting all ten digits' top, mid and bot values into one list. The features look clean, with the top share sitting high for 3, 8 and 9 and low for 1, 4 and 6.

I'm checking the top-bit, mid-bit and bot-bit shares for each digit against the three-feature groups, and the lists for 0, 1, 2 and 3 are coming out fairly distinct from one another.

I'm checking which vertical segments separate the remaining digits in the group {0, 2, 3, 5, 8}, since the three main features can't tell them apart. The upper-left, upper-right, lower-left and lower-right segments look like the useful splits there, with 0 having all four and 2 lacking the lower-right.

I'm checking which vertical segments can separate the remaining digits in {0, 2, 3, 5, 8}: the upper-left and upper-right ones distinguish 3 from 5, the lower-right and lower-left ones distinguish 2 from 3, and a centre diagonal separates 0 from 8. Next I'll probe the upper-left, upper-right and lower-right segments, then the lower-left and centre pieces.

I'm weighing whether a classifier after this probe would be enough, or whether I need one more segment test first. Estimating the three horizontal features plus the upper-left, upper-right and lower-right verticals suggests roughly 85% accuracy, with 0, 2 and 8 still the hardest to tell apart.

I'm defining the first vertical-segment feature over a set of sample cells in the upper-left region, and expecting it to separate 3 from 5, which should lift the overall accuracy toward the 80–85% range.

I'm settling on the vertical-segment probes now: the upper-left and upper-right ones should separate 3 from 5, since 5 lacks the upper-right stroke. The right-side columns look like they'll pick up the arc tip of 3 and the top of 1 at the edges, which I'll measure rather than assume.

I'm weighing whether the upper-left and lower-right vertical segments are worth probing before llV or urV, since they split {0, 2, 8} and {2, 3, 5, 8} more cleanly.

I'm weighing whether the upper-right and lower-left segments can split 5 from 8, and I'll also need a centre diagonal to separate 0 from 8.

I'm weighing a third probe alongside the upper-right and lower-right segments, with the lower-left and a centre diagonal as the remaining candidates. The plan is to spend steps 10 and 11 on probes and leave the rest for classification, possibly with the classifier starting at step 11.

Next I'm writing the probe for the upper-right and lower-right vertical segments, and I'll pick up the planned step-11 probe for the lower-left and centre diagonal afterward.
