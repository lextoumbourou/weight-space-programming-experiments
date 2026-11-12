I'm seeing that classes 8 and 9 are under-predicted, with 8 dropping from 540 down to 87 after the β shifts, which were probably too large. The cosine differences are tiny, so I'm going to try smaller β adjustments and set 8 and 9 to 0.

I'm checking the column totals now: class 5 is over-predicted, so its β needs to come down, while class 4 is also too high and needs a smaller shift. I'm settling on a new set of β values with small nudges, leaving classes 1, 7, 8 and 9 mostly where they are.
