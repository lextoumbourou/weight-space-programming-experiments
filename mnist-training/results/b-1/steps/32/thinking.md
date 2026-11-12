The result dropped to 71.7%, and the class balance shifted a lot, with 4 now over-predicted and 9 down. I can't yet tell whether the shear change or the lam_ori change is responsible. Reverting shear looks like the likely fix for the imbalance, so I'm weighing that against reverting to step 30 with only lam_ori at 1.6, or keeping shear and recalibrating instead.

I'm leaning toward reverting shear and keeping lam_ori at 1.6 with gscale 0.49, so I can test lam_ori on its own first, and maybe try shear again with recalibration later if there's room.
