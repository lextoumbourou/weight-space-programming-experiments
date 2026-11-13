The loss has dropped to 0.3431 with 90.07% accuracy, though the gains are shrinking, so GAMMA_C near 0.3 looks close to optimal. With 15 steps left, I'm deciding whether to spend 6 of them measuring the other-half H/V cells for 16 features, leaving 2 spare, since orientation features seem to carry the most value.

I'm weighing whether the extra measurements are worth it. Based on earlier gains, the other half of the H/V cells should add about half a percent, which may beat spending those steps on tuning, so I'm leaning toward measuring them and still leaving eight steps for tuning.

I'm settling the measurement order now: three H cells, then three more, the rest of the H cells, then the V cells, with the last two steps going to the two diagonal cells I kept as spares.
