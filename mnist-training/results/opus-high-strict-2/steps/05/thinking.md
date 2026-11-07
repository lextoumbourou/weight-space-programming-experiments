I'm at 65% and need a bigger jump, so I'm suspecting the features themselves are the limit. One option is adding nonlinear feature types like endpoint or junction detection, though that's hard. The other is that raw ink and 8x8 orientation features should already reach around 95% with good weights, which points to the linear templates being the real problem.

I'm checking the template confusions, like 1 versus 7 and several others, and wondering whether my orientation conventions for the diagonal templates match what conv1 actually computes. The pooling geometry is what I'm verifying next.

I'm checking the pooling and conv1 geometry: the centers work out to about 2s+6, so the alignment looks right. Next I'm comparing the 3 and 5 templates, since the 3's upper arc and the 5's top bar might be too similar in the upper-left region. I'm considering whether the real 3s simply have a flatter top than my template.

I'm weighing whether to make the template weights difference-based, so the classifier emphasizes where confusable digits differ, though subtracting the shared mean wouldn't change the argmax. Scaling each feature by an inverse within-class variance could matter, but I don't have that variance estimate and would have to approximate it. Improving feature sharpness, and the mismatch between the template blur and real strokes, may be the more useful lever.

I'm thinking about whether to make the templates lean harder on the features that separate confusable digits. For 3 versus 5, the 5's top-left vertical stroke is the key difference, and for 5 versus 6 and 9 versus 0 it's the left side of the loop. Strengthening the negative weights in those discriminating regions might help more than adjusting the shared mean.

I'm thinking about whether a plain negative weight, scaled up where a template is empty, would help, but adding a constant doesn't change the argmax. So the better move is hand-drawn "should be empty" zones for each digit, such as the right-middle region for 5 or the left vertical for 3.

I'm considering whether a separate ink-based blob channel would add anything, since the orientation features already capture most of the stroke information. For the vertical strokes, the vertical detector fires strongly and the horizontal one stays near zero, which seems selective enough. The arcs produce a mix of responses, and that seems fine for now.

I'm wondering whether the bigger gap is in how the templates are shaped rather than the features themselves. Curve direction isn't captured by the axial orientations, though position partly makes up for it. I'll try refining the templates against typical digit layouts, like the 0 as a wide ellipse, the 1 as a near-central vertical bar, and the 3's arcs meeting at the middle.

I'm going through the expected stroke layouts for each digit: the 6's left curve into its bottom loop, the 7's top bar and diagonal, the 9's loop with its stem, the 4's arms and crossbar, and the 2's top arc and bottom bar. My templates look broadly consistent with those, but nearest-template matching on these orientation features probably tops out around 70-75%, so I need more discriminative power to get past that.

I'm considering a pairwise adjustment: for frequently confused digit pairs, shift each template's weights along the difference between the two templates, so the distinguishing features get emphasized. Since that only sharpens the contrast between the two templates, it stays within the feedback I have, without fitting new data.

I'm weighing whether reweighting features could change any pairwise decision, since scaling a template difference only rescales the discriminant without moving the boundary. That points toward either better templates or a different metric over features, and I don't know which feature emphasis would help. A more promising direction might be a conv2 layer that builds nonlinear cues like loop closure or endpoints, or a trade-off that cuts spatial redundancy.

I'm considering a 4x4 coarse grid for the features, which would leave room for other channels, though the resolution would suffer. Since I'm unlikely to get past roughly 70-75% with template tuning alone, I'm also thinking about whether a slightly larger template blur, around 3.5 instead of 2.5, might tolerate the ±2-3 pixel position variation in real digits better.

I'm considering a blurrier template, around σ=3.5 instead of 2.5, since real class means are softer than my sharp templates. I also want the orientation tuning to fall off more gradually, perhaps with a cos⁴ falloff rather than the clipped cos 2Δ, so that near-diagonal responses leak into neighboring orientations the way real detectors would.

I'm now trying a cos⁴ falloff for the orientation tuning, so a 22.5° offset gives about 0.73 and a 45° offset about 0.25, which lets neighboring orientations leak more. Next I'll recalibrate the biases cumulatively by adding half the log ratio of true to predicted counts, though I expect the template changes to shift those counts anyway. The specific 1→7 and 8→1 confusions are noted as things to watch.

I'm going to keep β at 3 rather than raising it to 4, since the loss is 1.07 and it's unclear whether sharper weighting would help. For the bias update, I'll carry the previous values forward and add half the log ratio of target to predicted counts from the new pass, computing it in code from both arrays.
