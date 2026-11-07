I'm noting that the loss is still high, which I'd put down to the single thin templates being the core issue. One idea is that digit ink and thickness vary, so a distance-based classifier is sensitive to that; centering the templates and using a correlation-style score might help, since subtracting the mean doesn't change the ranking of the dot products.

I'm working through the idea of cosine similarity: normalizing each template by its norm makes the score scale-invariant with respect to the input, so the classifier becomes an argmax over normalized correlations, with per-class bias tuned afterward. I'm also wondering whether blurring the prototypes in orientation and space would better approximate each class's mean, and whether the thick strokes of MNIST digits produce weak or negative responses from my narrow detector band.

I'm testing whether a 5x5 narrow-minus-mean kernel still picks up thick strokes, and it looks fine with its current weights, so I'll keep it and maybe lower the bias to -0.2. Since cosine similarity makes the argmax scale-invariant, the scale only matters for the loss, so I'm estimating a suitable temperature κ, roughly 3 if the norm of f is around 3-5.

I'm checking the error cases now: several digits, like 9, 5, 2 and 3, keep getting pulled toward the 8 template, which is far too large. Cosine similarity should reduce that bias, and I'm also considering blurring the templates more widely and starting per-class biases at zero.

I'm checking whether subtracting a shared vector from every template would change anything, and it wouldn't, since that offset is the same for each class and leaves the ranking alone.
