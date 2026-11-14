I'm decoding column 3 of V from the step-9 patterns, mapping each output o0 through o9 to its bit string. Then I'm summing those patterns to get the four bits b0 through b3, with b0 taking o1, o4, o7 and o9.

I'm tallying each class's bit rates from the counts: class 0 comes out at roughly 71%, 97%, 94% and 44% for b0 through b3, and class 1 is much lower on most bits.

I'm working through the bit rates for classes 4 and 5: class 4 comes out around 89%, 92%, 70% and 46%, and class 5 is very low on the first bits, at roughly 1%, 13% and so on.

I'm working through class 6's bit rates: b0 comes to about 3%, b1 about 29%, b2 about 80% and b3 about 36%. Then I'm starting on class 7, with b0 at roughly 59% and b1 still being summed.

I'm working out class 8's bit rates from its counts, landing at about 59%, 53%, 55% and 50%. Then I'm moving on to class 9 and starting to sum its first bit.

I'm finishing the b3 sum for class 9 at about 51%, then writing out the full V column 3 table with all ten classes' bit rates.

I've now got 31 features measured across H and V, with only one H cell still missing. Next I'm planning a pure naive Bayes classifier on those 31 features to see how accurate it is, and I'm setting up the log-odds weights with the probabilities clipped to a safe range.

I'm settling on a scale factor of about 0.4 for the log-odds, since naive Bayes overcounts correlated evidence and would otherwise be overconfident. At that scale, typical correct margins stay small in loss, while the occasional wrong call costs only a few units.

I'm settling the log-odds scale at 0.3, since naive Bayes overcounts correlated features and needs tempering. I'm also adding log class priors from the row counts, which have only a tiny effect. I'm leaving the diagonal templates out for now so this checkpoint measures the naive Bayes classifier on H and V alone.

Now I'm filling in the per-class row values for the H grid, starting with class 0, and leaving out the one cell I haven't measured yet.

Filling in the H grid row values for classes 1 through 3, with the per-row counts continuing from where the last pass left off.

I'm filling in the H grid's remaining class 6 values, then moving on to classes 7 through 9, and I'm leaving the one unmeasured cell out.

Now I'm filling in the H grid's rows for classes 7 through 9, with the class 9 row 2 values still to come.

Now I'm converting the V column tables into row-by-column grids for class 0, taking each column's four values and arranging them by row.

Now I'm writing out the V column grids for classes 1 and 2, arranging each column's four values by row and working through class 2's first column.

Writing the V column grids for class 3, arranging each column's values by row.

Now I'm arranging the class 4 V values into rows, with the first two rows of the grid filled in and the third still in progress.

Still filling in the class 6 column grid...

Still converting the class 7 column grid...

Still converting the class 8 column grid...

Still converting the class 9 column grid...

Setting up the checkpoint: I'm deciding to test the naive Bayes classifier now, before adding more probes, to confirm the approach works. I'm storing the H and V probability tables as percentages, with the unmeasured H cell left out, and converting each into log-odds weights scaled by 0.3 and clipped to a safe range.
