I'm decoding the output column V1 by mapping each pattern o0 through o9 to its bit string, then expressing the four output bits b0 to b3 as sums over the patterns that set each bit. This is the start of the class-0 case.

I'm working through the per-class tallies now, summing the counts that set each output bit for classes 1 through 3 and converting them to percentages.

I'm tallying the bit counts for class 4 and class 5, converting each output bit to a percentage of that class's total.

I'm tallying the remaining bit counts for classes 6 through 8, with class 6 coming out around 73%, 87%, 92%, and 67% across the four outputs, and class 7 at roughly 12%, 25%, 43%, and 71%.

I'm finishing the bit-percentage tallies for class 8 and class 9, then writing out the first few rows of the V column 1 table.

I'm filling in the rest of the V column 1 table, with the class 9 percentages and the bit ratios for classes 3 through 8. One result stands out to me: class 8 looks notably high on the last output bits.

I'm checking whether the V column 2 pattern should drop the bottom bit, since the stem counts for column 1 showed that bit mattered a lot.

I'm checking whether a bottom-only pattern makes sense for column 2, since the top-only and bottom-only options both look like they'd mostly show up as longer runs instead.

I'm weighing whether column 2 should also drop the top-only pattern, since the stroke ends up in the top rows there and the bottom-only pattern still shows up for the 7s. I'm going to keep the same choice as column 1, dropping 1000 and keeping 0001, because the earlier counts show 1000 is rare.

I'm considering whether column 3 should drop the bottom-only pattern instead, since the top-right corners of the 2s and 7s might make the top-only pattern more common there. I'll decide that at the next step, and for now I'm setting up column 2 with the same patterns as before.
