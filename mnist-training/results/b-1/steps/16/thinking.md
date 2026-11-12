The 60.7% result is the best so far, so I'm moving on to per-class tuning. The confusion pairs are the main target, and class 8 is over-predicted while 4 and 5 are under-predicted, so I'll look at a scale-invariant bias adjustment.

I'm setting the bias term to use the normalized mean template, so a β of about ±0.02 works out to a cosine-sized shift. For the templates, I think the 4 is too wide after the stretch and is losing to the 9, so I'll give it a positive β, and I'll penalize the compact 8 with a negative one.

I'm weighing a few bias offsets per class, favoring 4 and 5 and penalizing 8 and 9, and I'm also considering adding orientation channels back into the cosine, which could help separate 4 from 9 and 5 from 3, though changing two things at once is risky.

I'm going to combine the ink and orientation parts into one score, with orientation weighted at half, and I'll compute the two cosines separately so each part keeps its own normalization. I'm also thinking about raising the scale to about 12, since the loss is reasonable and the accuracy is around 60%.
