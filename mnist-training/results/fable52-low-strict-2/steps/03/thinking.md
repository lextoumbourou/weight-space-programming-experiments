A small gain came in, but the 2 got dropped too hard by the bias and negatives. The 0 still scores 282 against the 6 template, which doesn't make sense unless the 6 template is matching too broadly. I'm wondering whether the 6's lower loop and left stroke are what's catching the 0, since the 0 is larger and its loop sits differently.

I'm reconsidering the 0 template, since real MNIST zeros are wider than mine, around 15-16 px against my 13 and 10. I think the other digit widths are off too, so I'm adjusting the 0 to 16 and 13 and nudging several others wider.

I'm going to raise the gain to 11 and scale the biases up by about 1.5x as well, since the logit gaps look small and a bigger gain might cut the loss even at 67% accuracy. I'll check how the loss moves before trusting it, because changing both at once makes it hard to tell which one helped.

Scaling the per-digit biases by 11/8 to match the new gain: 0 goes to about +0.7, 6 to about -0.8, and 8 to about +1.1.
