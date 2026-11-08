The model got worse once x4 was added, so I'm suspecting x4 isn't really Pclass3 and may be carrying a different signal. Its bounded range with a mean of zero means its negative values are fairly large, which could be pushing the gradient the wrong way. I'm also wondering whether x4 overlaps with x1, since passenger class and fare tend to move together, which would count the same effect twice. Next I want to test x4 on its own.

I'll test x4 by setting it to -0.4 to see which direction it pushes the model.
