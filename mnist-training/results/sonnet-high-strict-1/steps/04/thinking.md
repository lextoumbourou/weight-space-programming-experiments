The bias terms are clearly too large relative to the weight scale, so the logit gaps between classes end up around one. I'll raise the weight scale to about 0.9, roughly tripling it so the templates carry more influence, and shrink the biases to about 30% of their earlier size, since the old magnitudes of around 1.5 were drowning everything else out.

I'm settling on a scale of about 0.4 and multiplying the biases by roughly 1.3, which gives the biggest offsets around -0.5 for classes 4 and 6 and +0.5 for class 8.
