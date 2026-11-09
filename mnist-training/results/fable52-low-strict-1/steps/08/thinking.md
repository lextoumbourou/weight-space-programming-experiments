Tinkering blindly isn't helping, and 4→9 hasn't moved at all across the changes, while 7→9 got worse. My guess is that 9 is simply matching too broadly, so I'm going to step back and check whether my model of how strong the feature responses are is wrong, starting with stroke thickness: MNIST strokes are only about 2-4 px wide with soft edges, so I'm reconsidering whether my features are scaled to match that.

I'm checking whether thick, bold digits weaken the line responses so much that the class ends up decided by noise. The cosine matching is scale-invariant, so that part should hold. Then I'm looking at whether my 4 template is misaligned: real 4s may have the stem and bar sitting in different places than mine, which would make the score against it lower.

I'm weighing whether the template is too broad: a stroke a few pixels off centre still deposits a fair amount of signal, so each stroke fills a wide band and the 9 template ends up matching real 4s almost as well. The pooling windows may be generous enough that the feature responses blur together, which would explain why nothing I've tweaked moves 4→9.

I'm checking the feature strengths against the template profiles: a stroke within about 3 px gives a response of roughly 0.4 to 0.8, while the 4 template gives somewhat higher values near its centre, so the mismatch looks modest rather than dramatic. I'm also noting that the negative background weights, around -0.035, are small next to the positive values near 0.1, so they probably aren't what's driving the 4→9 confusion.

I'm checking whether my 4 template's arm sits in the right place: I'd drawn it leaning like a "/", and real 4s may have their arms converging more like a "U" or "V", so the mismatch could be coming from there. The arm placement looks roughly right on paper, though, so I'll turn to the 9 loop's horizontal span next.

I'm checking the 9 loop's horizontal span against the 4: the stem lines up, the left side sits almost where the 4's arm does, so the real difference is the top arc and the short bar extension. The 9 template carries more energy overall, which should lower the score for a 4, but the curved corners match less well, so the margin looks thin, and the mean-centring could push either way.

I'm realizing my earlier reasoning was muddled: a linear score for class 9 only drops on a 4 input if the 9 weights are negative where the 4 has ink. Emphasizing features the 4 lacks doesn't penalize anything. So the fix has to come from the ink a 4 has that a 9 doesn't, like the right end of the bar and the top of the left arm.

Now I'm weighing whether a negative weight on the 9's top-left and top-right corners could push a 4 down, though that's subtle given the crosstalk. Then I'm considering per-class biases instead, since lowering 9's and 1's and raising 4's and 8's would shift the totals directly, with the per-class prediction counts from the latest step as the reference.

I'm checking the per-class prediction counts, where 9 is far over-predicted and 4 under-predicted. Step 3 scored best, so I'm weighing reverting to that config and adding per-class biases to push 9 and 1 down and 4 and 8 up. Step 7's changes made 8 collapse, which suggests the zero-sum negatives on class 1 are leaking positive mass into the other classes.

I'm dropping the idea that zero-sum negatives will fix this, since they only inflate the other weights and pull in more predictions. Non-zero-sum changes have been unbalanced too. So I'm going back to the step-3 setup, with the original templates and no adjustments, and adding per-class biases to correct the over-predicted 9s and 6s and the under-predicted 4s.

I'm settling on per-class biases: nudging 4 and 1 up, pulling 9 and 6 down, with smaller corrections for the rest, since the step-3 totals show 4 is under-predicted and 9 and 6 are over-predicted. I'm keeping this to one change at a time, so I'm holding off on any targeted negative weights for now.

I'm now thinking about adding targeted negative weights for the 6 and 9 templates in the places where their over-prediction comes from, which should lower them directly, and pairing that with a smaller bias shift. I'll keep the negatives small, since earlier non-zero-sum changes at a larger strength wiped out class 5 entirely.

I'm dropping the idea of targeted negative weights for the 6 and 9 templates, since blobs placed close to their own strokes could easily hurt. Instead I'll revert to the pure step-3 setup and only adjust per-class biases, then make one targeted change at a time.
