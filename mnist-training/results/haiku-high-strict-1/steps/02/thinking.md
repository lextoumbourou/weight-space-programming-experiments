I'm guessing the zero fc bias and the ink-based template scoring are pushing everything toward class 5, since its template has many large positive cells. Background pixels contribute nothing to any class, so ties would just go to the first index.

I'm working through the zero-feature case: every score would be zero and argmax would fall back to class 0, yet predictions are mostly 5. Checking the conv channels, the background responses look zero too, so I'm checking whether the ink feature could be nonzero on digits and whether class 5's template has the largest positive mass. Summing the template weights, class 5 comes out to about 4.5 while class 1 is -4, so class 5's template favors ink-filled regions.

I'm noticing class 5's template has the largest positive sum (about 4.5), so raw ink mass favors it over other digits. The fix I'm considering is making each template zero-sum by subtracting its mean, so a score reflects pattern rather than total ink, and then equalizing the class biases.

I'm thinking about mean-centering each template so its 16 cells sum to zero, since class 5's mean is about 0.28 and subtracting it would remove the advantage from raw ink mass. A zero-sum template would tie a fully inked image across all classes. I'm also considering a log-likelihood-style template with positive weights for expected ink and negative for expected background, and I'm wondering whether the blurred, max-pooled ink features, which give background cells near strokes values around 0.3 to 0.5, make that hard to separate.

I'm going to center each class template so its 16 cells sum to zero, then scale the templates to a common norm so no single digit dominates by sheer ink mass. Class 1 might need a bit more weight than the rest, since its template is currently small, so I'll check that after the change.

I'm now weighing whether to zero-center the horizontal channel templates too, since the horizontal feature sits at -0.3 across the board for class 1 and could skew totals the same way the ink templates did. I'll compare the total mass each class gets from that channel before deciding whether to center it as well.

I'm considering whether the horizontal templates should be zero-centered per digit as well, since the class 1 penalty on horizontal features could tilt totals the same way the ink templates did.

I'm working out how to scale the templates now, leaning toward subtracting each template's mean so the cells sum to zero. Class 1's template would come out to roughly minus 0.75 on the outer columns and plus 0.75 in the center, while the overall magnitude stays modest.

I'm deciding to subtract the mean from the ink templates so they sum to zero, but I'm leaving the horizontal templates alone. Centering those per digit would make digit 1's contribution vanish, and it would push middle-row ink on digit 2 into negative territory.

I'm settling on mean-centering the ink templates so each sums to zero, while leaving the horizontal templates as they are. Centering those would erase digit 1's contribution. I'll write up the diagnosis first, that ink mass favors class 5, and then the zero-mean fix in code.
