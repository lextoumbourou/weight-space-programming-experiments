Step 11 is at 45.79%, the best so far, so I'll keep calibrating and work out the predicted counts for this step from the row data.

Now I'm checking the column totals against the row data, and they add up to 10000.

I'm working through the column errors next: column 2 is far too high because true 2 and true 6 get predicted heavily, and column 5 collects large contributions from several true digits. Several predicted totals are off, and the biases show 6, 8, and 9 still need correcting.

I'm noticing the rare classes still come out far too low even after the small bias bump, so I'll push their biases up more and pull back on the big ones like 5 and 2. The step from −0.05 to +0.15 barely moved the counts, but the jump to +0.8 earlier shifted them a lot, so the useful range for those rare digits sits somewhere around 0.3 to 0.5.

Step 12 is next.

I'm weighing a few bias values for the rare digits, around +0.3 to +0.4 for 6, 8, 9 and 0. Going from 0.15 to 0.5 on class 0 roughly tripled its predictions, but pushing 8 and 9 that high at once let them swallow other classes, so the interaction between biases is the hard part.

I'm settling on bias values for the rare digits and pulling back on the over-predicted ones like 5, 2 and 3. Given the sharp nonlinearity from earlier, I'll try a moderate step on 5 and watch how the counts respond.

I'm nudging the biases for 2 and 3 down a bit more, and the rare digits 8, 9, 6 and 0 up to around +0.35, since their counts are still tiny.

I'm settling on bias values of +0.35 for the rare digits 0, 6, 8 and 9, and pulling 5, 2 and 3 down to the negative range. I'm also setting 7 to +0.05 and 4 to −0.05, then writing out the full bias vector.
