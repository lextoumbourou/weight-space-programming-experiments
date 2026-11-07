I'm at 77.37 and need to reach at least 77.77 within steps 22–26 to beat the step-21 best of 77.27 by the margin I want, so I need about +0.4 in three steps. One option I'm weighing is the 3→5 and 5→8 cluster, with scores of 211 and 158.

I'm looking at a few more candidate pairs with lower scores, 4→9, 7→9, and 8→9, plus 0→8, and wondering whether the shear on 9 pushed the 7→9 and 4→9 numbers up or down. Rather than tweaking the emptiness channels, I'm considering a more targeted fix for the 3-vs-5 confusion, since the upper-left region is where they differ.

I'm going over why the 3-vs-5 split is hard to catch with these coarse emptiness windows: the 3's upper-left gap is only about 4 to 5 pixels, smaller than the detection range. So I'm turning to orientation instead, since the 5 has a vertical stroke in the upper-left where the 3 has a diagonal hook, though the 5 may still win on the shared bowl shapes.

I'm considering whether a sharper penalty mask would help only for classes 3 and 5, since both improved under the recent step, while the others either held steady or dropped.

I'm weighing whether to apply the sharper penalty mask per class instead of globally, since the step-22 change helped 3, 5, 1 and 7 but collapsed 8. The thought is that the 8 penalty is what drove the 5→8 drop, so keeping 8 blurred might preserve the gains without the damage.

I'm weighing a per-class penalty mask: a sharper one for classes 1, 3, 5 and 7, and a softer one for the rest, since the 8 penalty seems to be what hurt the 5→8 pairs. Globally applying an intermediate mask would only halve each effect, and the step-22 gains for 3 and 5 may have come from the change to 8 rather than their own masks, so I'm unsure which way it cuts.

I'm going to try a sharp penalty mask only for classes 1, 3, 5 and 7, since those are the ones that improved in the last step, and check whether that helps without the damage to 8.
