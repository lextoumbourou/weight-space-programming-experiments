Every prediction now lands on 0, since the "0" template with its heavy border ink matches any peripheral signal once peripheral emphasis is added, and the loss stays high at 5.3. The masking just makes 0 the dense winner in the periphery, so this is the same dense-bias problem showing up in a new spot. I keep swinging between designs because each one produces a template that pulls everything toward it, and the root issue seems to be linear template matching itself.

I'm trying to make the competition fair by ensuring that, for an average digit, all the logits come out equal. Subtracting the mean template earlier pushed predictions toward 2, 3, and 6 because normalizing afterward brought the imbalance back. The core problem is that the dominant "overall ink blob" feature favors whichever template correlates most with it, and I don't know the feature distribution well enough to remove that component cleanly.

I'm working out that the shared blob direction is what keeps biasing things, so I want each template orthogonal to the average ink map. Subtracting the mean only zeroes the sum of each template, which isn't the same as orthogonality to that map. Renormalizing afterward is probably what undid the fix, so I need to handle that step more carefully.

I'm making each template orthogonal to the mean ink template by subtracting its projection onto that mean, then scaling to unit norm, since rescaling won't break the orthogonality. The mean template is only a proxy for the real common feature direction, but it's the best I have, and I might also orthogonalize the vertical and horizontal channels the same way.

I'm making each template orthogonal to the mean ink template by subtracting its projection onto that mean, then scaling to unit norm. I'm dropping the center mask since it was creating the 0-magnet, and I'm considering whether to add a moderate gain of 8 for the orthogonalized templates, since their deviations will be small.

I'm checking whether centering already removes the shared component, since the uniform direction is what it orthogonalizes against.

Subtracting the projection onto the mean ink template should keep the common blob from favoring dense digits, and rescaling to unit norm won't undo that. I'm dropping the center mask and keeping the templates clean.

I'm checking that orthogonalizing each template against the mean ink map is the right move, since subtracting the mean alone doesn't make the templates orthogonal to it. Then I'll scale them to unit norm, keep the vertical and horizontal channels as small scalar terms, and set the ink gain to 8 with zero biases.

I'm switching to the proper projection: each template loses only its component along the mean ink map, with the coefficient set per digit rather than subtracting the full mean. That should keep the orthogonality intact.
