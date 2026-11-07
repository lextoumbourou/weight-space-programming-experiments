Now I'm considering structural changes, since the features are coarse and the templates are rigid. One idea is to blur the templates or features spatially so they tolerate variation, with max-pooling already giving some of that. A second is to use each template's difference from the mean template, though subtracting the mean doesn't actually change the logits, since f·T̄ is the same across classes.

I'm weighing whether a third option, negative evidence from template regions where the feature map has ink, would add anything. The distance formulation already handles that implicitly, so I'm leaning toward leaving it alone. Next I'd try tuning κ, since the per-class error pattern suggests 6 is being overpredicted.

I'm thinking about softening the templates so strokes can shift a bit, and about averaging several style variants per digit to make them less rigid. I'm also considering lowering κ to about 0.3 and widening the spatial falloff, while leaving β at 0.6 for now.

I'm planning to add template variants for several digits: slanted and vertical strokes for 1, a straighter diagonal for 2, open and closed-top versions for 4, a straighter 7, a slanted-stem variant for 9, and a slanted 8. Then I'd average the variants within each class to form each template.

I'm making the templates softer with a wider spatial falloff, averaging several stroke variants per digit, and lowering κ to 0.35.
