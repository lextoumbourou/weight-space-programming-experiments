I've got a small improvement so far, but the biases have saturated, so the next gains need better template or feature work across the remaining five steps. The main confusions are 4↔9, 7→9, 2→3, 9→8, 0→2, 3→5, and the spread on 8. I'm weighing a few structural changes, and the first is the shear amount: I don't know the typical MNIST slant, maybe around 0.2 to 0.25, and testing it would cost a step.

I'm working through template shapes next, since the center-of-mass shift changed where the 9 would land. Walking through the 4 first: its crossbar sits around 60% of the height, which seems right, but the 9's loop could end up overlapping the 4's crossbar region once it shifts down. Working out the 9's center of mass suggests its stem would reach close to the bottom edge, which looks too low for real MNIST 9s.

I'm checking whether the 9's loop and stem still sit plausibly after the center-of-mass shift, and they land near the bottom edge like real MNIST 9s sometimes do. The 7 works out similarly: its top bar drops to about row 8 and the diagonal reaches row 26, which seems reasonable. I'm also wondering whether the 7→9 confusion comes from the 7's slightly curved top-right corner, since its bias is already at 1.1.

I'm weighing whether a linear template could handle the 4/9 and 7/9 ambiguity better by summing two variants per class, such as open and closed 4s or 7s with and without a crossbar. That would effectively draw the union of both strokes into one template, which is still hand-built and not too hard to try.

I'm working out whether a single slanted stroke is too narrow for the 1s, since they vary so much in tilt. I'm considering drawing the 1 as a union of two or three hand-described variants, upright, mid, and strongly slanted, each centered on its own before combining, and I'm checking whether that counts as an acceptable hand-built template.

I'm adding two more variants for the 1s, a straight upright one and a strongly slanted one, alongside the current slant. For the 7s I'm trying a wider top bar with a more vertical diagonal, and for the 4s an alternative closed-top shape with a diagonal from the upper right down to the left.

I'm going to give the 1s, 4s, 7s, and 0s two hand-drawn variants each and sum them into one template, which should cover more of the real stroke variety. I'm keeping the 2s and 8s as they are, and I'll need to retune the biases afterward since the union changes the template norms.
