The step-12 version, with the thicker 4 template and the new biases, dropped the score to 38.4% from 40.47%, so it made things worse. Step 11, with the thinner 4 template, is still the best result so far.

I'm reverting to the step-11 config, since the thicker 4 template made the crossbar over-attract other digits. Step 11 at 40.47% is still the best. I'll keep the revert clean and only apply the bias calibration from the step-11 marginals, leaving the template alone so the two changes don't get mixed up again.

I'm weighing whether reverting to step 11 and only recalibrating the biases will help, since step 11's 9 over-prediction and 4 under-prediction look like the clearest things to fix. I'll keep the thin template and nudge those two bias values modestly so I don't repeat the confounding that broke step 12.

I'm reverting to the step-11 template and biases, but lowering the 9 bias to -1.75 and raising the 4 bias to -1.40. The aim is to shift the 4-versus-9 boundary toward 4 without the over-attraction that broke step 12.

I'm weighing a different tradeoff now: the thicker 4 template recovered 4 recall but pulled in false 4s from several other digits. Keeping the thin template and just shifting the biases looks like the lower-risk move, so I'll apply a gentler change to the 4 and 9 values.

I'm considering a thicker 4 template paired with a lower 4 bias around -2.0, since the over-attraction in step 12 seems to come from the bias being too high rather than the template itself. I'd lower the 9 bias as well, though I'm weighing whether changing two things at once will confound the result again.

Computing the step-12 column totals now, starting with the 4 column, which comes out to 1525, well over the target. That suggests lowering the 4 bias. The rest of the marginals still need working through.

Totaling the step-12 columns now: the 4 column comes to 1525, well above target, and 9 (1357) and 1 and 2 are also over, while 3, 6, 7, 8 and 0 sit under. That points to lowering the 4 bias well below -1.30 and bringing the 9 bias down too.

I'm recalculating the bias corrections from the step-12 marginals, which put the 4 column at 1525 and the 9 column at 1357, both well above target. Applying the half-strength correction pushes the 4 bias down to about -1.51 and the 9 bias to about -1.65, while the under-predicted digits like 0 and 5 move up.

I'm weighing whether a thicker 4 template with a recalibrated bias could beat step 11's 40.47%, but I'm leaning toward a safer approach. I'll revert to the proven step-11 config and make only a small, careful bias adjustment on top of it.

I'm applying a half-strength bias correction to the step-11 values using its marginals, starting with digit 0 at about 1.93 and digit 1 at about -1.48, to see if the 9 and 4 imbalance can be reduced without changing the template.

I'm recomputing the marginals from step 11 and applying a half-strength correction to the biases, which lands on values almost identical to step 12's. That means the bias tweak alone would just repeat the step-12 setup, so I need to rethink the adjustment.

I'm going to test the step-11 template with the step-12 biases, which isolates the bias change from the template change. Step 11's thin 4 template recalled too few 4s, though, so I'll watch whether this combination actually helps.

I'm weighing a compromise: a medium-thickness 4 template that sits between the thin one from step 11 and the full-crossbar one from step 12, paired with moderate bias values. Since that would change two things at once, I'll keep it in mind as a fallback rather than the next move.

I'm going to keep the thin 4 template from step 11 and only change the biases, lowering 9 to -1.54 and raising 4 to -1.33. Since the 9 column was far over target, I expect some of those false 9s to flip back to 4 without costing much on true 9s.

Writing the bias values and template for step 13...
