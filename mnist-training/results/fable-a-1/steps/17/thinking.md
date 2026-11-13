Initial results came in at 81.6% accuracy with a loss of 0.643, roughly on par with the hand-built corner templates. The measured zone stats didn't improve on the hand cell templates, though the errors differ. Now I'm checking how the predictions are distributed across the ten classes, and class 8 stands out as heavily under-predicted, with 631 of 1009 missed and many of those going to 6 and 9.

I'm looking at the top-heavy errors now: class 8 is badly under-predicted, mostly leaking into 6 and 9, and the zone features may be scaled too large, which would explain why 8 keeps losing its bias while the low-count classes gain.

I'm weighing whether Z_TYP is set too high, and guessing the typical Z when a corner fires is nearer 0.35 than 0.6. The cleanest fix seems to be matching Z_TYP to the median of Z given the feature fires, so I'd like to check the level distribution for a couple of corner types first.

I'm weighing a finer measurement of the Z distribution for TL-upper and BR-lower, with about ten level bins each, against just trying Z_TYP=0.35 directly. A real run would be informative too, since the 1/7 over-prediction and the 8 under-prediction should show whether the change helps.

I'll try the direct change first: lowering Z_TYP from 0.6 to 0.35. I also want to bring back the hand corner templates for their within-zone positional information, though I'm setting that aside for now. Freeing channels for clipped corner features could make the zone signal more binary, which is worth a look later.

Lowering Z_TYP from 0.6 to about 0.35 should make the zone features fit the actual fire levels better, and that might let class 8 recover its bias. I'm also thinking about whether the magnitude of Z carries useful signal, since a linear fit could work if it's calibrated. Testing that directly with the new value and a slightly higher GAMMA_C should show whether the 1/7 over-prediction and the 8 under-prediction improve.

I'm comparing class 8 against class 6 now. Each zone feature contributes a weight scaled by Z over Z_TYP, plus a bias term from ln(1−p), and class 8's negative bias sum is about −19 while its weights total about 18.3.

I'm checking whether class 8 can overtake class 6 if the typical fired Z lands around 0.3 to 0.4, since the margin depends on how big Z is against Z_TYP.

I'm going to lower Z_TYP to about 0.33, since 8 only overtakes 6 when the typical fired Z is above roughly 0.24 to 0.4. I'm also checking the per-class rates for 4 and 6 to see how the 4→6 confusion shifts.

I'm checking the per-class rates for 4 and 6 and finding they overlap heavily, so the 4-vs-6 split depends mostly on the orientation features. I'm keeping GAMMA for the hole feature at 0.5 and going ahead with Z_TYP set to 0.33.
