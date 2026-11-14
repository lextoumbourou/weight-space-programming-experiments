I'm working out the parity equations for row 0 of the H matrix, with each check bit as a sum of the data bits it covers. For class 0, I'm tallying the counts and checking the first few bit totals against the 3.4% figure.

I'm tallying the remaining classes, checking each bit's share against the percentages I've already computed, and noting which classes come out near zero.

Now I'm tallying classes 7 and 8, working out each bit's share from the counts in their rows.

Now I'm finishing the tallies for class 9, where bit 0 comes out to zero and bit 1 is around 10%, bit 2 about 24%, and bit 3 under 1%.

Now I'm tallying the per-bit shares for row 0 across classes 0 through 9. Class 5 stands out, with bit 3 near 40% while bit 3 is barely present in the others, and bit 8 is only around 5.6% in that same class.

Now I'm moving on to the next row of the H matrix, checking the remaining columns against the bit shares I've already worked out.
