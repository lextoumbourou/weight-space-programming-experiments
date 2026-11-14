I'm working out the decoding rule: the output value is built from three bits, with b1 covering the odd-numbered outputs, b2 the 2-3-6-7 group, and b3 the 4-5-6-7 group. I'm also noting that outputs 8 and 9 are always absent, and starting to tally the class 0 counts for 991.

I'm tallying the class 4 counts now, starting with the first few entries of its distribution.

I'm now working through the class 5 and class 6 tallies, checking how the bit counts come out for each group.

I'm now tallying the class 8 counts, checking how the bit groups come out for that class's distribution.

I'm tallying the class 8 and class 9 counts, working out the three bit groups for each. Class 8 comes out strongly on b1, b2 and b3, while class 9 sits around two-thirds to three-quarters on each group.

I'm comparing the "\" stroke strength across the digit classes: class 8 and class 3 are the strongest on the (1,2) position, while classes 0 and 1 stay low on the same position.

I'm working through the conditional probabilities for the remaining stroke positions, checking the rare cases for digits 2, 4, 6 and 7. Next I'm planning the extra corner strokes for the last set of tests.

I'm now setting up the next set of extra stroke checks, starting from the bottom-left "\" position and looking at how its conditional rates looked earlier. Since those earlier strata were small, I want to see how often it shows up once the top-left "\", the center "/" and the "/" at (1,2) are all absent.

I'm settling on the extra checks for this round: the bottom-left "\" at (3,0) and the "/" at (0,0), since the conditional rates for the earlier bottom-left stroke were based on small strata.
