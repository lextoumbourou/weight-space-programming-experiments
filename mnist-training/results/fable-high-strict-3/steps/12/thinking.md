The 56.7% result is about where step 9 landed. Digit 8 mistaken for 2 rose to 343, and 2 mistaken for 9 rose to 268, while the count of correctly classified 2s fell to 386. I suspect the forbidden region I added for 2 is part of the problem: it covers the left side of the mid-height band, which is where real 2s put their diagonal, so it clips ink that belongs to the digit and doesn't just protect the template.

I'm weighing whether to pull 2's forbidden region back to the step-9 version, and I'm considering a narrower extra region near the lower-left to catch the 8s that are being read as 2s.

I'm weighing whether 3 and 5 can be told apart with a targeted negative region, since both sit close together in the current feature space. The orientation maps already encode the top bar of a 5 versus the arc of a 3, but raising that scale would disturb everything else, so I'd rather keep it and look for a narrower fix.

I'm moving on to 2→9 now: the 9's forbidden bottom-left region probably doesn't reach 2's base, which sits outside the visible window, and 2's diagonal at mid-height runs partly into that region.

Now I'm looking at 8s getting misread as 2s and 3s, while the 8 template itself only catches about 345 of them correctly. Since non-8 digits are already matching 8, I'm thinking the 8 template is too weak rather than the others being too strong. I'll set the 9's bottom-left mask to reach x<0.45 for y 0.7 to 1.0, which is a cautious widening that still protects its own stem.

I'm thinking the 8 template is too wide compared with real 8s, which would explain why 8s slide into 3 and 2 while other digits land on 8. I'd narrow it to about half-width, and I'm also wondering whether the forbidden region for 3 is positioned to cover the left side that real 8s occupy.

I'm now checking why 5s are being pulled into 8, which seems tied to the same spacing problem around the 8 template's left side.

I'm adding the top-right corner of the 8's forbidden region back in, since the 5's top bar reaches that area, while leaving the top-left corner alone because the 7 and 2 features don't need it.

I'm going through the per-digit counts from step 11 and comparing each against its true total. The shifts are small, with 6 and 0 pulling the most. I'll adjust the bias values by those amounts.

I'm adjusting the 8's shape to be narrower and adding a top-right corner mask to keep 5s and 7s out. I'm also widening the forbidden regions for 2, 3 and 9 and recalculating the per-digit biases from the step 11 counts.
