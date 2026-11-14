The temperature check at T=1.2 came out slightly better than at T=1.0, with the loss nearly flat between them, so the optimum looks to be around 1.1. That means the model is already close to well calibrated, and I'll keep T=1.1. Next up are the remaining 10 steps on group scale experiments, since the temperature is essentially settled.

I'm running through the group scale experiments with temperature fixed at 1.1, starting with the presence weight and then the end and draw votes. Since the earlier bias retune and the sE change suggested the end vote was under-weighted, I'll try raising sE to 1.0 and sD to 0.75 together, and keep the change only if loss improves.

I'm scaling the end and draw votes up together, sE to 1.0 and sD to 0.75, which is roughly the same as lowering the presence and hint weights while letting temperature drift a bit higher.
