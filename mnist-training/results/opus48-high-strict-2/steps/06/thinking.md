The two biases of +1.2 on classes 2 and 7 are now dominating the predictions, so only those two classes come out on top. That means the template logit contributions are tiny, roughly order 1, and the bias terms overwhelm them. So the features are barely separating the classes at all, and I'm trying to work out how much of the signal is coming from there.

Going back over the numbers, the ±1.2 biases on classes 2 and 7 swamp the template logits, which only spread by about order 1, so the features are barely separating the classes. Step 2 with no bias got 29%, so the template signal is there but weak. I'm now thinking the biases need to be much smaller, around ±0.2, so they nudge the ranking without taking over.

Trying the step-2 setup again but with much smaller biases, around ±0.2 to ±0.3. I'm also considering raising the feature gain so the template signal decides more clearly, though that could backfire if the templates are wrong. Looking at the confusion pattern, classes 0, 2, and 7 have templates that compete poorly with their neighbors, and I want to understand why 0 keeps landing on 6.

I'm now weighing whether normalizing the templates but leaving the central cells in place is the right move. Those central cells look shared across digits, so they add noise rather than discrimination. I'm thinking about zeroing or down-weighting them so the classes separate on their outer structure instead.

I'm going to center each ink template, multiply it by a mask that down-weights the four central cells, and then normalize, so the discrimination comes from the periphery. I expect that to separate 0 from 1 and 7 without the dense digits winning by default, though I'm not sure the outer ink carries enough signal yet.

I'm checking whether masking out the center cells keeps 1 recognizable: with its ink concentrated there, its template turns near-zero and its low peripheral ink would score highest against the others. I'll combine that masked, normalized template with a scalar vertical feature.

I'm settling on the plan: center each ink template, down-weight the four central cells, normalize, and add scalar vertical and horizontal features with moderate gains and no biases for now.

I'm masking the four central cells of each ink template so they stop dominating, then normalizing, with the bias terms still set to zero to isolate the effect. I'm going to use the step-3 ink templates since they include the better versions of 6 and 8, and I'll take the vertical and horizontal scalar features from step 2.

I'm settling the gain balance now: the ink templates are unit-normalized and scaled by Gi=10, while the vertical and horizontal scalars come out small, so I'm raising their gains to 10 as well so orientation counts for more.

Still writing the masked templates...

Still writing the masked templates...
