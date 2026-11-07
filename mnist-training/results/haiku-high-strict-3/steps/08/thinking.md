I'm trying to work out why class 8 won at step 7 even though its bias is lower than 9's, and I suspect the zeroed row 3 and column 3 in the templates are shifting the mean subtraction toward 8's generic positive pattern.

I'm checking the centre cells, where class 8's template is the only one with a positive mean, so for most digits with ink there it should pull the logit toward 8. Class 8's raw sum across the 3x3 block comes to 6.5, which is far above the others, and that generic activity term is likely what lets it beat class 9 despite the lower bias.

I'm now checking the arithmetic behind class 8's large generic sum, which comes out to -3 for the other template. Since per-class centering helped earlier but didn't reach the target, I think the fix is to zero-centre each class template across all its cells, and to scale the biases down so they don't add to the imbalance.

I'm settling on biases of [0, 0.2, -0.3, -0.6, -0.8, -0.9, 0.9, 1.0, 0.5, 0.9] for the next pass, since step 6's values gave about 36% with the 4x4 templates and should be a sensible starting point once the per-class centering changes the template magnitudes.

Now I'm adjusting the biases so class 6 is at 1.0 and class 9 stays at 0.8, since 6 has no bias term yet and step 6's values gave a reasonable starting point.

Next I'm centring each class template over its 3x3 block so each sums to zero, then removing the per-cell mean across classes. Since every class then sums to zero, the generic activity term that favoured class 8 should disappear.

I'm settling on zero-sum templates for each class, since class 8 won at step 7 only because its total template weight was the largest, boosting any digit with centre ink.
