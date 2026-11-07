Things got worse, and 8 is dominating again, so I'm going back to the step 6 setup. It keeps winning whenever the penalties are weak, which makes me think the feature vectors respond broadly across orientations, with thick strokes lighting up many of them, so the template with the most coverage wins. That points to conv1 not being selective enough.

Instead of nudging conv1 to be more orientation-selective, I'm considering switching to pixel-ink templates, since the feature pipeline behaves unpredictably. The problem is that the final 4x4 grid is very coarse, so a sampled ink map may not beat the orientation features. Pixel-level nearest-mean would probably land around 65-70% on hand-drawn digits, so it's not clearly better.

Now I'm tuning per-class biases from the step 6 config, since the confusion counts show 8 and 5 are overpredicted and 9 is underpredicted.

I'm re-tuning the per-class biases from step 6: pushing 8, 5 and 3 down since they're overpredicted, and 9, 4, 7 up since they're underpredicted, with 0 and 1 nudged slightly. I'm leaving the rest of the config alone so I can see what the bias change alone does.

I'm looking at the 3→5, 6→5, and 2→3 confusions and wondering whether a structural change would help, or whether the bias adjustments will mostly cover them.
