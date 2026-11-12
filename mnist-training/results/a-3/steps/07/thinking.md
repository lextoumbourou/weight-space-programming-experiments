I'm at 68.4% progress and considering per-class bias adjustments through feedback, along with tuning eps and gamma and adding features. The confusions show class 8 absorbing several others, and I'm noting the main misclassification pairs.

I'm working out per-class bias corrections from the predicted-to-true count ratios, using roughly half a logit per unit of log-ratio. Classes 1, 8, and 9 are over-predicted, while 2, 3, and 5 are under-predicted, so I'm settling on a scaling factor of about 1.0 for the adjustment.

I'm going to tune the temperature and eps together with the biases, lowering eps to 0.02 so mismatches get penalized harder. Since class 8 covers most of the image, it rarely triggers the eps penalty, so a stricter eps should help the specific templates for 2, 3, and 5. I'll change both settings at once.
