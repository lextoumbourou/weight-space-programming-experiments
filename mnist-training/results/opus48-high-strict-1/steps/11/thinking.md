The accuracy is stuck around 39%, and the bias adjustments aren't changing much. The biggest persistent errors are the mutual confusion between 4 and 9, plus 8 misread as 2, 1 misread as 7 or 2, and 7 misread as 5, 9, or 1, with 7's recall especially weak.

I'm weighing whether the 4/9 confusion can be fixed by bias alone, since shifting toward 4 would just trade 4→9 errors for 9→4 ones. The hole feature should separate them, but the errors run both ways, so the features clearly aren't doing the job. I'm now looking at what structural traits could tell a 4 from a 9.

I'm checking whether the hole detector reliably separates the two digits, since 4s being pushed into the 9 class suggests either the hole fires on 4s or the 9 ink template matches them better. With no positive hole signal for 4, a true 4 leaves that feature near zero, so the decision falls back to the ink template and bias.

I'm checking whether the hole detector misses many 9 loops, which would explain why 9s drift toward 4. Making it more sensitive might recover 9s but could add noise, so I'm also considering strengthening the ink templates so 4 and 9 are more distinct, starting with what separates them in ink at 12x12.

I'm checking where 9s and 4s differ at the left edge. A 4 has ink in the left-middle from its crossbar and diagonal, while a 9's left-side ink sits higher up in its loop. The upper loop of a 9 is the most reliable marker, so I'm thinking about how to make the 9 template reflect that.

I'm redrawing the 4 template with less ink in the upper region so it stops matching the loop of a 9, and with a stronger crossbar and left-middle stroke.

Sketching the 4 template again, I'm keeping the upper-left ink minimal so it stops matching a 9's loop, and I'm checking that each row is twelve characters wide. Row 6 is the full crossbar, and the 9 template stays empty in the middle-left.

Still writing the 9 template...

I'm settling on the new 4 template, with its upper-left ink kept minimal and the full crossbar in row six, and I'm keeping the 9 template as it is. Next I want to look at the 8→2 confusion, since 8 recall is only 79 and the two-loop template may not be firing cleanly.

The 8-versus-2 confusion looks like it comes down to the lower loop: an 8 has a closed loop on the lower right that a 2 lacks, so the hole feature should separate them. But 8 recall is low, which suggests the lower hole isn't firing reliably at 12x12, and the 8 hole template may be too weak to do its job.

I'm going to strengthen the 8 template's lower-right ink, since a 2 lacks it, though the templates are binary so that's limited. The bigger payoff is the 4/9 fix through the new 4 template, so I'll focus there and only nudge the biases, keeping the 4→9 shift in mind.

I'm settling on the new 4 template as the main fix, and I'll keep the 9 template as it is, so the 4/9 balance should come from the shapes rather than the biases. I'm recomputing the column totals to check the class marginals before I adjust anything, so the biases stay balanced.

Now I'm recomputing the column totals to see how the predictions are spread across the digit classes.

I'm adjusting the biases from the column marginals, but the 4 bias has to stay around -1.8 because lowering it would hurt the already weak 4 recall. For the other classes, I'm pushing 0, 5, 6, 7 and 8 up and 1 and 3 down to even out the predictions.

Setting the 4 template to a new design now, along with the revised biases.

Still writing the 4 template rows...
