Column 8 is underpredicted by about 340, so I'm shifting its bias to +0.4. Next I'm totaling the column sums: column 4 comes to 1401, column 2 to 975, column 7 to 921, and I'm still tallying column 1.

I'm nudging the bias for digit 8 up by 0.5, trimming digits 4, 6 and 9 slightly, and bumping 0 and 5 a little. The digit 8 is still the weakest, so I'm considering whether to strengthen its template weights directly. I'm also finishing the column tallies, which put column 6 at 1377, column 9 at 1361 and column 3 at 965.

I'm weighing a per-class scale on digit 8's template weights, around 1.5x, since its template carries little signal. Scaling zero-mean weights would amplify responses in both directions, though, and I'm not sure that helps, so I'm settling on bias adjustments alone.
