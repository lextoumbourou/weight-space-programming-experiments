Loss dropped to 0.6441 even though the model still leans toward cat at 45% dog, so I'll nudge the bias toward dog. Texture might want a bit more weight too. Separately, I'm thinking about a sharper 1-pixel gradient kernel in place of the current Laplacian.

I'm keeping the 3x3 Laplacian as it is, and I'll go ahead and set texture to 0.2.
