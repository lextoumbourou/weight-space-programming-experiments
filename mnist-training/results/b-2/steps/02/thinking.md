I'm weighing why the 8 template wins: the unnormalized dot product rewards images with a lot of ink, and mean-subtracted templates still look like generic "stuff everywhere." I'm considering a norm-based correction, and also making each template zero-mean so that uniform activation contributes nothing.

Next I'm trying per-template zero-mean centering, subtracting each template's own mean across its 64 entries so a uniformly active feature map contributes nothing, and then renormalizing. That would also remove the bias toward the fuller 8 template, though it may discard some information about overall orientation quantity, so I'm considering a partial version instead.

I'm also considering a margin by raising the scale alpha, since the loss is high with accuracy at 0.38, which suggests confident mistakes. I'll keep the normalization after centering so the templates end up at unit norm, and try alpha 8.
