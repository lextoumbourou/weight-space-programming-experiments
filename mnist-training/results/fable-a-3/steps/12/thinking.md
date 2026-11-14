I'm decoding the V column by working out each bit as a sum of specific output positions. For class 0, I'm tallying the selected values from that list of ten, starting with b0, which comes to 324 and about 32.7%, and I'm moving on to the b1 sum.

Now I'm working through the class 4 bit sums, starting with the b0 total.

Now I'm checking the class 4 sums for b0 through b3, which come to 79.3%, 92.1%, 92.6%, and 89.4%. Next I'm moving on to class 5, where the per-bit totals are much lower for b0 and b1 but higher for b2 and b3.

Now I'm running the class 8 sums, starting from the opening value of 37.

I'm tallying the class 9 bit sums, working through b0 to b2 and starting on b3.

I'm checking the bit-sum totals for V col 2 against the table, which matches the per-bit percentages I just worked out. Next I'm starting on V col 3.

I'm working out which pattern to drop for V col 3, weighing whether top-only or bottom-only runs are more common given how the slant pushes tops rightward, and I'm leaning toward dropping 0001. Then I'm setting up the step 9 decode, with o0 as 0000 and o1 as 1000, and continuing through the rest of the mapping.

Still working out the step 9 pattern mapping for the remaining outputs.
