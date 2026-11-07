Digit 1 seems to pull in a lot of wrong guesses, with 8, 6, 4 and 5 all landing there. I'm wondering why, and the template for class 1 looks like it might be the cause: a near-vertical stroke down the centre columns, with ink strongest in the middle and weaker at the edges.

I'm checking why the digit 8 keeps landing on class 1, and the dense ink of 8 seems to leave its centred template with low variance, so after normalisation its weights become unreliable while the 1 template stays high-contrast. Max-pooled features of thick strokes also give the ink map little pattern. I'm now looking at whether class 1's vertical stroke in the centre columns is pulling in digits like 4, 5 and 6 whose left-side strokes fall into the same cell.

I'm weighing whether class 1's normalisation is the culprit: its template keeps only a few non-zero maps, so each gets a large weight, while class 8's many maps share the norm and end up small. I'm considering whether unit-normalised cosine scoring, versus a squared-distance match that depends on calibrated magnitudes, would change how often 1 wins.

I'm weighing a nearest-template approach using squared distance instead of cosine, which would penalise templates with large norms. The catch is that it needs the feature magnitudes to be roughly calibrated against the templates, and I'm not sure they are.

I'm working out whether the nearest-template score for 8 beats class 1: if the features match the template scale, 8 comes out ahead, but if the features run systematically larger, the dense templates get an unfair boost.

I'm considering a nearest-template score using squared distance with a penalty proportional to each template's norm, which should stop the dense templates from being unfairly favoured. The penalty can be tuned with the confusion matrix if 8 is still over- or under-predicted. I also note that the penalty doesn't apply to features present where the template is zero, so a 7 would still overlap strongly with its own template rather than with the 1 template.

I'm checking whether the nearest-template score handles the 3-versus-8 case on its own: the overlap with 8's template minus half its norm comes out below 3's own self-match, so 3 still wins.

I'm checking whether adding a mild negative weight on the ink channel, pushing the template values below zero where there's no stroke, would sharpen the separation between digits like 3 and 8.

I'm settling on a scale for the logits, around 0.4, since the templates sit near 0.7 and a correct match could otherwise give very large differences that blow up the loss. I also want the features to stay presence-like, so I'll keep the saturation.

I'm checking whether 6's loop and the 0 confusion come from the same place, since a 0 overlaps 6's bottom loop and left side. Nearest-template scoring should show whether the shape of the loop alone is enough to explain it.

I'm settling the weights as the template plus a small negative term on the ink channels, scaled by s, and folding the norm penalty into the bias, with λ = 0.5, s = 0.4 and β = 0.15.
