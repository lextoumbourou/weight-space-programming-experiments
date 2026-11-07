The bias problem is coming back: class imbalance again, with eight classes underpredicted at 215. The blur seems to be shifting the biases, so I'm considering a calibration step that keeps the bias term independent of the template shape changes. Still, I need to get steps 13, 14, and 15 past 0.8014, which means reverting to sp=2.5 and making structural changes carefully. The sp=3 per-class result, with class 8 at 215, is worth another look too.

I'm checking the per-class numbers: class 1, 3, and 7 went up, so I can't tell whether discrimination actually improved. The safer route looks like reverting to the step 10 config with T=1.8, which lands right around the 0.8014 threshold. I'm also working through the column sums from the step 9/10 confusion matrix to get small bias corrections.

I'm thinking about structural changes that might not shift the biases much, but the bias term already accounts for the template norms, so the drift comes from the features themselves. A cosine-style scoring idea is something I've already tried and it was poor. I'll be pragmatic: revert to the step 10 config with T=1.8 and apply half-strength bias corrections, then test template changes one at a time with bias retuning.

I'm trying a tweak to the 9 template: a more compact loop and a more vertical stem. The 7 template might also need a small change. What separates a 7 from a 9 in the features is the upper-left vertical edge and the middle horizontal edge that a 9 has and a 7 lacks.

I'm settling on a template-side tweak: the 7-versus-9 confusions probably come from sevens with short tops or curly strokes, not from the template shape itself. So I'll leave the templates alone and just do the revert, the temperature change, and the bias correction, which should land around 0.795.
