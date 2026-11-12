The accuracy sits at 0.57, so the template approach has hit its limit and I need something more powerful. My hand-designed templates cover only a coarse orientation range, which is why the errors pile up. I'm considering improving the template matching itself, starting with the orientation problems: a slanted 1 at 45° fails to match my near-vertical 1 template, and it gets predicted as a 7. I'm thinking the templates should tolerate that by blurring across orientation bins, possibly with several slanted variants.

I'm weighing whether to keep tuning the templates or switch to a different design that keeps more spatial detail, such as shifted sampling offsets in the second conv stage.

I'm working out how to get more spatial resolution out of the second conv stage: by using single-tap convolutions at different offsets, the pooling windows can start at different positions, so the grid effectively shifts by a pixel or two.

I'm working out whether the finer grid would actually help, since the pooling offsets give me 4x4 windows at a finer stride, but hand-built templates with blur might not be precise enough to exploit that resolution.

I'm weighing whether averaging several drawn variants of each digit into one template is acceptable, since it might count as averaging generated samples, though I'd only be drawing the templates myself.

I'm weighing whether to smooth the orientation bins and widen the spatial blur so a slanted 1 still lands on the 1 template, and whether drawing the 1 as a few strokes at different slants is an acceptable way to build it.

I'm redrawing the 8 template as an S shape with a crossing in the middle, since my current version looks like two touching ellipses. The 4 template also needs work: I'll combine the open and closed forms into one drawing. I'm also checking the 9, whose loop is too small and which overlaps with the 7 template.

I'm checking the per-class errors now: 3 gets confused with 7, 9 and 2, and 0 often turns into 2, while 5 slides into 6 or 7. The scoring ignores feature norm, which doesn't change the ranking for a fixed input, so the real lever is the per-class biases. Predictions skew toward 7 and 1 and away from 8, so I'm considering a small bias shift to rebalance them.

I'm thinking about a Gaussian-style log-likelihood scoring instead of raw dot products, where each class logit depends on the distance to its template scaled by an unknown feature-scale factor I'd have to tune from feedback.

I'm weighing whether the templates can be sharpened enough to get past the mid-80s, since the nearest-mean baseline on MNIST already gets around 82% from raw pixels. Better template drawing, especially for the 8, 4, and 9, probably matters more than making the spatial grid finer. A Gaussian-style score would also need a feature-scale factor I'd have to tune, and I'm not sure it's worth it yet.

I'm thinking about adding per-class bias corrections and building a few drawn variants for each digit, like open and closed 4s or slanted and upright 1s. I'm also considering a global rightward shear on all the prototypes, since MNIST digits tend to lean that way.

I'm considering adding a mirrored-shear variant of each template alongside the upright one, since MNIST digits lean. Summing those is just a transform of my own drawing, so I think it's fine. I'll also check whether the existing orientation smoothing already covers the overlap, and I'm wondering whether the loss can come down by tuning the scale of the logits, though I'm not sure yet.

Still writing the stroke coordinates for the digit prototypes...

Still writing the stroke coordinates for the digit prototypes...

Still writing the 8 and 9 prototype paths and their shear variants...

Now I'm writing the prototype code by hand, adding the shear variants and spacing the strokes to match the 4-23 row range.
