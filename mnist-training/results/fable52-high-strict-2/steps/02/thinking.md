The baseline is at 69% with a loss near 1, which is reasonable. Next I'm going through the confusion pairs: the biggest one is 2 being mistaken for 3 (341 cases), with 2 also leaking into 8 and 9. Then I'm looking at 4 going to 9, 7 going to 9 and 5, the 0 and 6 mix-up in both directions, 5 going to 3, and the many ways 9 gets confused with 3, 5, 6, and 0.

I'm now going through the 2→3 confusion, which is the largest at 341 cases. The 2 template seems to share a bottom bar and top arc with 3, so I'm looking at adding a veto stroke along the lower-left diagonal where a 2 has ink and a 3 usually does not.

I'm weighing a pairwise fix for 2 versus 3: adding positive evidence strokes to the 2 template and negative ones to the 3 template. The key difference looks like the lower-right arc, which a 3 has at around x≈18, y 14–19 and a 2 lacks, while the 2's diagonal sits more toward the centre-left.

I'm laying out a list of evidence strokes, each given in absolute pixel coordinates on the 28x28 frame with signed weights per digit class. I'm placing the key discriminative regions after normalisation, and I'm starting with the bottom-left diagonal of the 2, which should count for it and against the 3, 5, and 9.

I'm working through the remaining pixel-level evidence for the 2 template: the bottom bar running across the full width reads as a 2 feature, while the 3's lower arc curves up on the right side instead. I'm also checking the lower-right vertical stroke at around x≈17.5, which should count toward 3 and 5 and against 2 and 7.

I'm now separating 9 from 3: a 9 has a loop on the upper left that a 3 lacks, and it has no bottom bar, while a 3 has that bottom arc, so I'm weighing a veto on the bottom-centre region for 9.

Now I'm looking at the 4→9 confusion, which has 227 cases. The main difference seems to be the top of the digit: a 9 has a horizontal stroke across the top, and a 4 does not, so I'm weighing a veto for 4 along the top-centre and a bonus for 9 there.

Next I'm going after the 7→9 confusion (196 cases): a 9 has a loop with a left-side stroke and a horizontal bottom at around y≈12, neither of which a 7 has, so I'm weighing vetoes for 7 there and a bonus for 9. The 7→5 cases (90) are less clear and I'm still working out what drives them.

I'm looking at the 0↔6 confusion next, which accounts for 170 and 115 cases. A 0 has an arc on the upper right that a 6 lacks, while a 6 has a horizontal stroke through the middle of the loop that a 0 doesn't, so I'm weighing a veto against 0 in the centre and one against 6 on the upper right.

I'm moving on to the 5→3 and 3→5 pairs: a 5 has a vertical on its upper left and a top bar reaching right, while a 3 has a stroke on its upper right, so each gets a veto on the other's side. Next up is 9→5, which I'm starting to look at now.

I'm checking the 1→2 and 1→7 confusions next, which are the slanted ones. A 2 needs a bottom bar and a 7 needs a top bar with its stem, so I'm weighing whether a bias on the centre diagonal would separate them better than a veto.

I'm working out how to tell 1 from 7 in the slanted cases. The 1 prototype probably needs a broader fan of slants with more weight, and maybe a small bias toward 1. For 7 I'm looking at a veto on ink in the lower-left, since its stem sits further right near the bottom than a slanted 1 does.

I'm adding a veto for 9 along the bottom at around y≈21.5, since that bar is what 2, 3, 5, 0, 6, and 8 share. For 8, the upper-left arc doesn't clearly separate it from 2, so I'm checking the lower-right stroke around x≈17, y 16–20, which 2 lacks.

I'm now sizing the veto strokes: with unit-norm templates each entry is roughly 0.1–0.15, so a veto stroke of about 5 px should contribute a comparable magnitude, and I'm working out a scale factor so the vetoes neither dominate nor vanish.

I'm working out how to scale the veto strokes so they have a meaningful effect without swamping the template scores, and I'm settling on a weight around 0.15 for the main ones. I'm formalising each piece of evidence as a stroke with a per-class weight, and I'm starting to define how that weight enters the class scores.

I'm working out how to scale the evidence renders: normalising each one to unit length keeps its strength in the same units as the templates, so a matching stroke adds roughly 1.7 times its weight, and a weight near 0.3 would give a contribution around 0.4 against a true-class score near 4.

I'm working out the scale for the evidence strokes so their weights land in the same range as the templates, and I'm starting to place the discriminative strokes for the 9 in absolute pixel coordinates.

I'm placing the 9's discriminative strokes in pixel coordinates: a loop with a left side near x≈10, a bottom bar near y≈13.5, and a top bar near y≈5.5. I'm also setting up the 4 and 7 templates, where the 4 has an empty top-centre region and the 7 has a top bar with a stem that angles down to the left.

I'm sizing the veto for 7 along the left side, around x 9–10.5 and y 9–13, since that area is empty for a 7 but used by 9, 4, and 5. The bottom crossbar on the left, around x 9–13 and y 13–14, is also a candidate, though a European 7 with a crossbar could cross there, so I'd keep that one weaker.

Now I'm placing the 5 and 3 strokes in pixel coordinates: the 5 has a top bar, a vertical on its upper left, a belly whose right side runs down, and a bottom bar, while the 3 has a top bar, a stroke on its upper right, and a lower-right vertical with a bottom arc.

Now I'm checking the 2 against the 3 and the 5 using the stroke positions: the 5 has its vertical on the upper left, the 3 has one on the upper right, and the 2 has its tip on the left with a diagonal running down to a bottom bar. A lower-right vertical separates the 3 from the 2, and the lower part of the diagonal separates the 2 from the 3.

I'm placing the 6's loop top and right side, and noting that the 0's upper-right arc is absent from a 6's upper region, which is the cue I'd use to separate them.

Next I'm weighing a veto for 6 on the upper-right stroke at x 17.5–19, y 8–12, and a veto for 0 on the centre region around x 12–15, y 11–16, to address the 0↔6 mix-ups. I'm also noting the 1 class's errors into 2, 7, and 4, though I haven't settled how to handle those yet.

I'm now defining the first evidence item: a top closure stroke at y≈5.5 running from x 11 to 15.5. I'm weighting it positively for 9, negatively for 4, and mildly negatively for 1 and 6, since their top-right orientations don't match that horizontal bar.

I'm adding a second evidence item for the upper-left side stroke at x≈9.7, running from y 7.5 to 12. It supports 9 and works against 7, 3, 2, and 1, with the veto strongest for 7 and 3 and weaker for 2.

Next I'm placing a horizontal veto along the bottom at about y≈13.5 for the left half, which 7, 0 and 1 should avoid while 9 uses it.

I'm checking the lower-left diagonal of the 2 next: a stroke from about (12.5,16) down to (9,20.5) that 2 has and 3, 5, 9, 7, and 4 mostly lack. Slanted 1s also run through that spot, so I won't veto 1 there, and that could still lift 2 for some slanted 1s.

Now I'm thinking about 1s getting mistaken for 2s and 7s, and whether 2 needs its own vetoes at the top and bottom. I'm considering a bottom-ending channel: strokes that end in a downward tip near the bottom centre, which 2, 3, 5, 0, 6 and 8 should have but 1, 4, 7 and 9 shouldn't.

I'm adding a lower-right vertical at x≈17.7 for y 15.5–19.5, which supports 3 and 5 and works against 2, 7 and 1, while 4 and 9 get no veto there because their strokes sit too close to it.

I'm adding a veto for 1 on the stroke at x 12–14, and a weaker one for 2, since some 2s flick upward at the right end of the bottom bar. Then I'm setting up an upper-right vertical at x≈17.5 for y 7.5–11, which should count against 5 and 6 and slightly for 3 and 2, with 0, 9, 4, 7 and 8 each having something nearby that needs checking.

Now I'm sketching a veto for 6 on the upper-right, nudged a bit further from the spine, and a separate item for 5 at x≈17.5 that stays clear of the 6 region. I'm also marking a centre-empty blob that counts strongly against 0.

Now I'm adding a veto for 1 on a top-left horizontal near y≈6, which should count against it while leaving the 7 and 9 channels as they are.

I'm adding a veto for 4 on the right-side vertical near x 16–17 that's at 1.7px from its stem, so I'm leaving 4 alone there, and I'm checking the 6 veto at x 17.5 next.

I'm weighing a veto for 6 on the upper-right at x 17.5, y 8.5–12.5, which I'd make about −0.4 for 6, since the spine sits a few pixels away. A separate bonus item for 0 would go further right at x 18.5. Then I'm turning to the bigger 4→9 confusion, wondering whether to lower 9's score on 4-like images or raise 4's.

I'm thinking about the 4s that get called 9s. A 4 has no top bar, so a veto on the top bar doesn't help 4 images; it only stops 9s from being labelled 4. What would actually help is features 4s have and 9s lack, like the two upward tips at the top and the crossbar that runs right, so I'm weighting those for 4 and against 9. The same idea applies to 7s being read as 9s, where the left end of the top bar is the distinguishing part.

I'm weighing how the 7s and 9s differ: a 9 can be pushed toward the loop features that 7s lack, by raising its weight on the loop-left and loop-bottom evidence and setting a negative bias to compensate for the response those features would give when present.

I'm working out the 2→3 confusion now: 3s should get a veto from the diagonal and bottom-right bar that 2s have, and a bonus from the lower-right vertical, while 2s get a smaller boost from the bottom bar.

I'm working out bias adjustments to correct the column imbalance: 3 is being over-predicted while 2 and 4 are under-predicted, so I'm nudging 2 and 4 up and 3 down.

I'm working through the 4→9 confusion next: I'd penalize 9 for an upward tip at the top and for a horizontal bar on the mid-right, and reward 9 for its top bar, while giving 4 credit for those upward tips and the mid-right bar. For 7→9, I'm weighing a bias shift that favors 9's loop-left and loop-bottom evidence, so that 7s stop scoring as 9s.

Now I'm weighing the 7→9 and 0↔6 pairs, nudging the top-left bar and the loop-top features so each template picks up what the other lacks.

I'm now weighing the 5→3 cases, adding a veto for 3 on the upper-left stroke and a smaller one on the top-right bar's end, with a bonus for 3 on the upper-right stroke and a small boost for 5 on the upper-left stroke.

Now I'm working through the 8s next, and the 7→5 cases.

Now I'm working through the 8s and the remaining confusions, adding vetoes for 9 on the bottom bar and for 5 on the down-tip at the bottom.

Now I'm working through the 8s and the remaining confusions, adding a veto for 8 on the lower-left diagonal that 2s carry, and a lower-left vertical that should help 6 and count against 3, 5, and 9.

Now I'm checking the upward tip at the top of the digit, along with the other ending channels for each class.

Now I'm adding a top-centre-right upward tip at x≈14–17, y≈5, which favours 4 and 1 and counts against 9, 7, 2, 3, 5, 0 and 8.

I'm checking the ending-detection vetoes and bonuses for the top and bottom tips, and wondering whether the 9s that have upward stems at the top will pick those up.

I'm now adding a rendered-evidence item built from pixel-coordinate samples, and I'm looking at how to apply the same stroke in all four orientations.

Now I'm normalising the stroke vector to unit length and adding it into the class weights, scaled by the coefficient and the gain.

I'm working out the remaining bias adjustments now, setting each compensation at about 0.8 times the gain so the stroke items don't overcorrect. I'm also weighing whether the overall scale factor should change, since the loss is still close to 1.

Now I'm compiling the per-class adjustments from the pixel-coordinate items, starting with the top horizontal bar, the upper-left vertical, and the mid-left horizontal.

Compiling the per-class adjustments from the last few pixel-coordinate items, now that the bottom-right horizontal and the lower-left diagonal are covered.

Now I'm adding a feature for the upper-right vertical stroke, which I'd veto for 5 and nudge against 6, and I'm working out how the lower-right vertical helps 3 while counting against 2, 7 and 1.

Next I'm adding a set of stroke-based items: a centre-region veto for 0, a bonus for 0 on the upper-right arc, a bonus for 4 and a penalty for 9 on the mid-right bar, and a top-left horizontal bar to finish the list.

Still adding the last few per-class items: the top-left bar, the loop-top bar for 6, the lower-left vertical, and the top-right bar for 5.

Writing the tip detectors now, listing the up-tip and down-tip positions with how each one should weight the digit classes.

Still tuning the bias terms, now on the 9 class: the top bar, the upper-left stroke and the mid-left bar each get a bonus, with a compensating negative bias so they don't overshoot.

Now I'm settling the bias terms for the final classes: 9 gets about −0.6 after the tip contribution, 5 about −0.42, 3 about −0.6 with the frequency correction, 2 about −0.16, and 4 gets a small +0.1 from the top-left stroke.

Now I'm settling the bias for class 4: the ending-based bonuses might not fire, so I'm using a gentler compensation, which brings 4 to about −0.3. For 6, the two loop-top and lower-left features plus the top-tip bonus put its bias near −0.45, and I'm checking the 0 entry next.

Now I'm setting the last biases for 8 and 1, using 8's missing mid-side bars and the up and down tip vetoes to decide whether it needs a negative term.

Tuning the biases for the 8 class now: it has no mid-side bars, so I'm adding small negative terms from the mid-right bar, the top-right bar and the bottom-right bar, and a modest overall bias near −0.15.

Working out the magnitude of the stroke features now: a 4.5 px stroke should give a nearest-cell template entry around 0.45 and smaller values for neighbouring cells, so each bank's norm comes to roughly 0.9 rather than the 1.5 I had assumed.

Now I'm checking the magnitudes: each stroke item should contribute about 2·g when present, so a compensation of −0.6·g is conservative, and a veto of −0.4 produces about −0.8 against a margin of roughly 0.5.

I'm checking whether the veto on the lower-left stroke, which should be strong for 3 and 5, could also fire partially on nearby 6s, since its spine sits a few pixels away. I'm also weighing whether the 3's tail, curling up-left, has the right orientation to avoid that veto.

Now I'm checking the vertical stroke at the upper left, which would penalise 3, and I'm noticing that the 3's tail end points steeply up-left, so it could trip the lower-left vertical veto too.

I'm checking the 3-class veto on the upper-left stroke, since the tip of a 3 starts up-right and only has a short diagonal there, so I'm giving it a moderate penalty. For 2, the lower-right vertical veto stays as it is. For 1, I'm dropping the bottom-horizontal penalty since 1s rarely have serifs, and keeping only a light penalty from the upper-left flag.

I'm now going back over the vetoes and biases for the remaining digits: class 1 doesn't need penalties since its false positives are few, so I'll leave it mostly alone, and instead make 2, 7 and 4 less attractive for 1-images by adjusting their biases and tip vetoes. I'm also checking whether class 0 needs the same kind of review, given its confusion with 6.

Now I'm weighing the 8 class, which gets false positives from 2, 5 and 3, and I'm considering whether an upper-left arc feature could help separate it from those.

Now I'm adding a lower-left bonus to the 8 class, since 3 and 5 lack that stroke and 2 only has a diagonal there, and I'm setting its bias to about −0.15. I'm also checking the top-centre veto for 4, which should stay strong since closed-top 4s don't have a horizontal bar there. For 6, I'm dropping the top-centre veto and softening the top-right one to about −0.15, since curled tops can still show that stroke.

Now I'm going back over the vetoes for class 9: its penalties from the tip and centre features could drop its recall, which is already at 541, so I'm weighing whether the vetoes on 3, 5, 6, 7 and 0 can handle those confusions without it.

Writing the evidence-rendering helper now, starting with a function that densifies a polyline into sample points for the stroke features.

Writing the feature helpers now, turning stroke and tip points into normalised template vectors.

Now I'm writing the per-class weight table, with each evidence item mapped to its digit boosts and penalties.

Still tuning the evidence weights, now on the item for the lower-right vertical stroke, which should favour 3 and 5 and push 2 down.

Still assigning the per-class evidence weights, now on the items for the top-centre bar, the upper-left and lower-right verticals, and the lower bar, plus their boosts and penalties for each digit.

Still writing the evidence weights, now on the top-left stroke entry for the 4s and 6s and its penalty for 9.

Now I'm fixing the penalty and bonus weights for the tip features at the ends of strokes, and setting the baseline biases for classes 0 and 1.

I'm settling the remaining biases for each digit, with 5 and 3 getting the largest bonuses so their negative biases are balanced by the evidence terms.
