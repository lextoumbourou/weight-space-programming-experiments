I'm at step 12 with a 49.06% figure and still calibrating, so next I'm setting up the predicted counts row by row, starting with the R0 through R4 values.

Now I'm filling in the remaining rows of the predicted counts matrix and tallying each column's total.

Next I'm checking which columns are over- and under-predicted against the true row sums, and the bias figures are starting to be set.

I'm weighing a bias increase for rows 6, 8, 9 and 0, since each +0.35 step multiplied their predicted counts many times over, and I'm estimating that something around +0.6 might land them near their true totals. I'm also keeping in mind that lowering the bias for row 5 pushes its images into neighboring columns, so the interactions need to be watched.

I'm bringing the bias for 0 and the other under-predicted rows up toward +0.6, and pulling 5, 2 and 3 down to about -0.28, -0.25 and -0.22 to ease their over-prediction. Lowering 7 and 4 slightly should keep the column totals in check.

I'm reviewing the prior bias settings: rows 0, 6, 8 and 9 are still well under their true totals, and pushing them to +0.6 might pull those counts up. I'm also trimming the biases for rows 2, 3, 5 and 7 because they're over-predicted, though lowering row 5 risks shifting its images into neighboring columns.

I'm settling the bias values at 0.55 for rows 0, 6, 8 and 9 rather than 0.6, to avoid overshooting, and I'm trimming rows 2, 3 and 5 further down while leaving 1 and 4 unchanged.
