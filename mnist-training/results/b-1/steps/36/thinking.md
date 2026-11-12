Soft 1.2 scored worse too (0.868), though much of that comes from calibration shifting toward 6 (198 cases), so I'll keep 1.5 and go back to the step-33 base. With 15 steps left, the most promising move is refining templates for specific digits through small edits, tested one at a time, though each costs a step and the gains look modest. Another option is trying lam_ori at 2.0 with g.

I'm weighing whether to test a change to the orientation detector's sigma, since thicker strokes might respond better at 1.2, though it would alter the features the templates rely on. The gains from further lam tuning look small now, and I'm also considering whether reweighting the hole features could reduce the confident 6→0 errors.

I'm now looking at the 4→9 confusion, the largest error at 203 cases. The key difference seems to be the top: 9 has a closed top stroke while 4 usually stays open, so I'm planning a small edit to the 4 template with its bar and vertical stroke placed a bit differently.

I'm going to change the 4 template so its bar and vertical stroke sit differently, since 4→9 is the biggest error. I'm also looking at narrowing the 8 template a little, though it might push 5→8 errors up.
