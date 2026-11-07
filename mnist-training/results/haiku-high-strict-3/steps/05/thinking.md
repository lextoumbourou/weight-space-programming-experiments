The accuracy has stalled at 26.8%, with predictions piling up on 1, 8, and 9. I suspect zero-centering stripped out useful signal and left the biases out of line. The fully connected layer on pooled features looks too weak for hand-set templates, so I'm weighing a more principled template built from typical digit shapes.

I'm weighing whether the hand-set fc templates are just guesses, since I have no data to check them against. Looking at the pipeline, the 4x4 pooled grid with 16 channels leaves 256 features, and I'm wondering whether a nearest-template approach on that coarse occupancy would work any better, though building it would mean hand-drawing the class maps.

I'm weighing whether a nearest-template approach on the 4x4 pooled features would beat the hand-set fc weights, though it would mean drawing the class maps by hand. The hand-template route seems to top out around 35-40%, so I'm considering features that are more directly informative, such as stroke-type density per cell, even if the conv layers only allow limited variety.

Going back to the step-2 approach looks more promising, since it reached 36% with only per-cell mean subtraction. I'm wondering whether the per-class zero-centering I added is what pushed accuracy down to 26.8%. Class ink totals also matter here: a 1 carries far less ink than a 0 or an 8, so a template with a positive sum favors dense digits, and removing that generic offset may be what skews the predictions.

I'm checking whether the per-class zero-centering is making class 1 look like a positive generic match on any high-activity image, which is the opposite of what I intended, and whether a matched-filter form with a shared constant offset would avoid that.

I'm considering dropping the per-class zero-centering and instead using a shared mean subtraction per cell, with the biases adjusted to offset the skew toward 1, 8, and 9. That would essentially be the step-2 approach, plus the grouping I never tested on its own.

Grouping the channels seems to have hurt: step 2 without grouping reached 36%, while the grouped version fell to 14% and then 27% with zero-centering. I'll test the ungrouped approach, with equal weights across channels and per-class biases tuned to offset the skew toward 1, 8, and 9.

I'm weighing a naive Bayes-style fc, where each class template is the log-odds of a cell being inked, drawn from hand-made ink probability maps. Bernoulli-like scoring would fit the 4x4 occupancy, though activations aren't binary, so thresholding would be needed and that adds complexity. The current templates already capture the rough stroke layouts for 0, 1, 2, and 7, so I'm wondering why they still land near 36%.

I'm checking whether the conv1 channels actually encode ink occupancy, since the stroke detectors and blob channels all look positive wherever ink is dense. The 4x4 grid with roughly 7px cells seems too coarse for hand-set templates, so I'd expect them to top out around 50%. Increasing the effective resolution might be the better lever.

I'm considering keeping the per-entry mean subtraction across classes but dropping the per-class zero-centering, then tuning the biases to balance the predictions. Last time that combination let 8 dominate, so I'll need to watch for that.

I'm weighing whether to make every class template sum to zero, without subtracting the per-entry mean, and I'm wondering if that's already happening implicitly. Step 4 applied both, and class 1 ended up dominating, so I'll need to check which of the two steps actually caused that.

I'm checking whether centering each class's template to zero makes class 1 win on high-activity images, since its strong centre column lines up with where most digits have ink. The per-entry mean removal and the class-wise centering together may be what pushes its score up.

I'm weighing whether templates that concentrate weight on the central cells are inflating scores for every class, since most digits have ink there. Subtracting the per-entry mean across classes should shrink that effect, but I can't tell how much without feedback. With only 11 steps left, I'm considering simplifying to a correlation against a per-class prototype built from hand-drawn ink maps, using normalized activity.

I'm checking whether a Gaussian template match can be written as a linear layer: expanding the squared distance gives a dot product with the prototype plus a constant bias of minus half its squared norm. That would make the fc a nearest-prototype classifier, which should stop dense digits from winning on raw ink.

I'm switching to a nearest-prototype view, where each class gets a prototype activity map set by an occupancy guess, scaled by a constant alpha. I'm still unsure what typical activity levels look like, so I'm working from rough guesses.

I'm reframing the classifier as nearest-prototype matching: a Gaussian template score can be written as a dot product with the prototype plus a bias of minus half its squared norm. That would stop dense digits from winning just on raw ink, and I'm still unsure what activity scale to pick for the prototypes.

I'm going to try a nearest-prototype classifier: score each class by a dot product with a prototype activity map, plus a bias of minus half the prototype's squared norm, so dense digits stop winning on raw ink. I still need occupancy maps for the channel groups, and the activity scale is a guess, but the feedback from the next run should show whether this matches the data.

I'm settling on a nearest-prototype setup, where each class prototype is an occupancy map derived from the hand-drawn S values, mapped into the 0 to 1 range, with the bias set to minus half the squared norm.

I'm settling on a nearest-prototype setup: each class gets a prototype activity map built from occupancy guesses, and the bias is set to minus half its squared norm so that dense digits stop winning just on raw ink. The scale is still a guess, so the next run's feedback will show whether the logits land in a sensible range.

Setting the prototype logits to a Gaussian-style form: a dot product with the prototype minus half its squared norm, scaled by a factor around 0.03. Next I'm writing the code that builds the per-class prototypes from the occupancy values.

Setting the bias to minus half the squared prototype norm, scaled by beta, and dropping the old step-2 biases in favour of it. Group 4's blob channels will carry the same dense centre for the 8 prototype, which is expected.

Writing the prototype code now: occupancy maps from the S values, a bias of minus half the squared prototype norm, and a fc that does nearest-prototype matching.

Next I'm writing the code for the nearest-prototype classifier.
