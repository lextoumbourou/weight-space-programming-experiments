I'm seeing the biggest confusion pairs as 4→9 at 162, then 3→8, 2→3, 3→5, and 7→9. For the 4 vs 9 case, I'm focusing on open-top 4s, which the model keeps predicting as 9, and I'm checking whether the two top endpoints of the left stroke and stem can be picked up by the endpoint detector.

I'm reasoning that a 9 template might share the stem-bottom endpoint with 4, so endpoints alone won't separate them. I'm considering penalizing 9 for endpoints in the top region, since 9 is usually a closed loop, and maybe penalizing 6 for bottom endpoints too.

I'm settling on a generic rule for the remaining confusions: for each class, add negative evidence wherever it has no endpoint. So 5 gets penalized at its top-left (9,6), 3 at its top-right (19,5), 3 at its bottom-right (20,21), and 2 at its bottom-left (9,20).

I'm working out the endpoint scaling: a per-class weight of the form g·(P − λ(1 − P)) reduces to g·((1+λ)P − λ), and the −λ term is identical across classes, so it cancels in the softmax and only rescales P. That means the uniform penalty I applied to 0 and 8 doesn't change the relative picture the way I'd assumed, and I need to recheck what it actually does to them relative to the others.

I'm noting that the endpoint term is linear in P, so the uniform −λ offset cancels in the softmax and only rescales the map, which means my earlier penalty on 0 and 8 isn't doing what I assumed. Raising the endpoint weight from 2.0 to 2.6 only gained about 0.07%, so returns are diminishing. I suspect the detector rarely fires on the 4's top endpoints because thick strokes spill across neighboring ring cells and push the sum below threshold.

I'm working through the endpoint weighting now: a ring-based detector with a center bonus and a surrounding penalty, where thick strokes could push the sum below threshold, so I'm testing whether a larger center weight with partial ring credit recovers them.

I'm checking whether a horizontal top stroke at y≈5 could separate 9 from the open-top 4s, since that feature is absent in the 4 but present in the 9's loop. The distance model is the place to test that, so I'm turning to its features next.

I'm weighing whether a bigger change to the distance model's features would help more than retuning endpoint weights. The orientation features may be worth rescaling against the ink features, though I don't know how much that would gain. I'm also considering whether the template term is overpowering the structural evidence, and whether lowering it would let the structure do more of the work. The 3-versus-8 pair looks like the next target, since the 8's closed left side versus the 3's open left side could be captured by vertical strokes at mid-upper and lower left positions.

I'm weighing whether the open-top 4 versus 9 confusion can be separated by the crossbar's right end at (20,15), since a 9 has no such stroke, and I'm considering whether the 4 templates are just poorly matched to typical 4s.

I'm considering a bigger overhaul of the template part, such as discriminative weights on the stroke features, though my earlier projection attempt slightly hurt accuracy. I'm also thinking about per-feature variance weighting in a nearest-centroid setup, but I'm not sure whether Bernoulli-style variance would help or just add noise.

I'm going to test a 4 variant with a near-vertical left stroke and a short crossbar, since that matches the images I'm looking at. I'm also nudging the class biases, raising 4 and lowering 9, to counter the current under-prediction of 4 and over-prediction of 9, then recalibrating.

Tallying the per-class column sums now, starting with the first few classes and carrying the totals forward.

I'm recalculating the per-class log-bias corrections, and the pattern is consistent across rounds: class 1 needs pulling down, class 8 down, and 3, 4, and 5 up. That suggests my 0.85 damping factor is too conservative, so I'm considering a larger step.

I'm applying a damped bias correction to the per-class log-offsets, nudging 3, 4, and 5 up and pulling 1 and 8 down, with a larger step than before. I'm also planning per-class endpoint penalties in spatial regions, like the top area for 9 and the top-right for 3.

I'm reconsidering the endpoint penalty: if each class's negative term is just the total endpoint mass minus that class's own endpoints, it mostly rescales the map again rather than adding real spatial discrimination.

I'm going to drop the scaling idea for now and only recalibrate the class biases, keeping the structural weights fixed. I'm also weighing a short 4 variant with a shorter left stroke, though I'm not sure it's worth adding yet.

I'm adding a short open-top 4 variant with a left stroke from about (10,5) to (9,14), a crossbar out to (21,14), and the stem running from (18,4) down to (18,24).
