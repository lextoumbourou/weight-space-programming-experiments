Now I'm totaling the per-column sums, with column 0 at 868, column 1 at 866, and column 2 at 584.

Now I'm checking the column totals against the rest of the sums, and I've got column 7 at 1756 and column 9 at 1462 running well over the others. Column 2 and column 5 are under, and some of column 8's true examples are landing in column 7. I'm adjusting the biases to pull column 7 and column 9 down and push columns 2 and 5 up.

I'm weighing a few bias tweaks for column 8 and column 3, and I'm leaning toward a slightly higher scaling factor of around 3.8 to 4.0, since the last change only added about a point.
