I'm working out a decoding of column 2, matching each of the ten patterns o0 through o9 to its bit string, then summing the patterns that set each bit b0 through b3. The last line is still starting to form the class.

Now I'm working out the per-class bit rates, summing the pattern counts that set each bit for classes 0 through 3. Class 1 comes out high on b1 at about 76%, and class 3 stays near zero on most bits.

Now I'm tallying the bit rates for classes 4 and 5, where class 4 has b1 around 41% and b3 at about a third. Class 5 stays low across most bits, and I'm starting the tally for class 6.

Now I'm tallying class 7's bit rates, where b2 and b3 come out highest at about 48% and 43%. Class 8 is next.

Now I'm tallying class 8's bit rates, with b3 at about 17.6%. Class 9 comes next, where b3 jumps to about 49.6% and b2 sits near 41.7%.

Now I'm reading off the per-pattern counts for the remaining column-2 rows, which give the bit rates for the (0,2), (1,2) and (2,2) cells.

Now I'm checking the per-bit rates for the (3,2) row, where class 9 and class 7 come out highest and class 4 follows. The stem threshold may need to drop a little, since the rates sit closer to 45% than I'd like.

Now I'm planning the next checks: the bottom strokes of 1, 6, 4, 7 and 9 on the vertical side, and the arcs on the top and bottom rows to tell 7 and 5 apart from 9, 3, 2 and 8.

Now I'm weighing which of the remaining checks are worth running, since I have room for only four of the six before the classifier. I'll drop the less useful column-0 and row-1/2 scans and take the row-0 and row-3 scans alongside the column-1 and column-3 ones. Step 29 starts with the row-0 run patterns, skipping 1000.
