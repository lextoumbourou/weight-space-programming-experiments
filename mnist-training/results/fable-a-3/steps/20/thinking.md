Now I'm working through the decoding constraints, mapping each parity bit to its set of outputs, and then starting on the class counts.

Now I'm tallying the class-by-class counts, working out each parity bit's share, and tracking the stratum A and B totals.

Now I'm checking the class 6 counts against the stratum totals.

Now I'm tallying the class 6 and class 7 counts, working out their parity shares and stratum A and B totals.

Now I'm checking the class 9 counts, working out the parity shares for b1, b2 and b3, and starting on the stratum A total.

Now I'm tallying the per-parity-bit shares for classes 8 and 9, and the stratum A and B figures.

Now I'm working out the conditional shares for the "/"(3,3) check, using the stratum figures and the step 5 data for classes 0, 1, 4 and 6, and putting together a rough combined estimate.

Now I'm running the rough per-class estimates for the "/"(3,3) and "/"(0,2) checks, and the low-information classes for (0,2) look like they'll just need a coarse guess.

Now I'm writing out the full k=3 table row by row, with each class's values across the four column positions.

Now I'm filling in the rest of the per-class table, covering the remaining rows of the k=3 grid.

Now I'm filling in the row-by-row values for classes 4 and 5 across the four column positions, and starting on class 6.

Now I'm filling in the row-by-row values for class 9 across the four column positions.

Now I'm filling in the last of the "/" table values for class 9 and the remaining percentages for the (1,2) check.

Now I'm filling in the remaining rough estimates for the "/"(2,1), (2,2), (0,1) and (0,2) checks, row by row across the nine classes.

Now I'm weighing the rough estimates for the (3,3) and (0,2) checks, and I'm planning to shrink the less reliable ones toward the middle so they don't skew the result too much.

Now I'm weighing the last features at about half strength, then trying a lower scale factor of 0.25 for the classifier checkpoint, since there are more inputs now and they overlap more.

Now I'm setting up the classifier tables in code, with the measured and rough values for each check and a reliability weight for the rougher estimates.

Still filling in the per-class grid, with the remaining cells of the "/" table for classes 0 through 3.

Still filling in the per-class grid, with the remaining rows of the "/" table for classes 9 and the last checks.

Still filling in the "/" reliability weights and clipping bounds for the classifier, and I'm writing the code that sets them up.
