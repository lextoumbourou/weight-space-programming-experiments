The model's accuracy is up to 73%, with 8s now at 723. The 1s dropped to 522 from 972, with misclassifications going to 2, 6, and 8. I suspect the unit-normalized LDA and the nuisance factors are part of this, since 1s have little ink and real 1s have thicker strokes. My synthetic 1s also differ, since their slant is more varied in reality, and the horizontal shift matters too.

I'm considering whether the 1-class drop comes from the LDA weights or the zero-bias behaviour on low-ink digits, and whether the fix should be a bias adjustment on the classifier, richer convolutional features, or wider slant variants for 1s and a curved top bar for 7s.

I'm weighing whether to nudge the 4 and 9 templates apart, since closed-top 4s resemble 9s. I'm also considering a higher alpha and a small positive bias for the 1 class, and adding serif and slanted 1 variants and extra 7 variants, though changing several things at once would make the effects hard to attribute.

I'm checking how the 1-variant geometry would work: a vertical line, a flagged version, and a base-bearing version. Since the box normalization is driven by height, a slant of 5 shifts the stroke by about 10 pixels horizontally, so the slant range matters a lot for 1s.

I'm setting the slant range for the 1 variants to roughly -3 to 7 pixels, since real 1s often lean right at the top. I'm also adjusting the output biases, giving the 1 class a small boost and the 9 class a small penalty.
