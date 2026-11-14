Baseline accuracy is at 61.65%, and I'm looking at which digit pairs get mixed up most. The biggest problems are 4 being read as 9 (567 cases) and 2 being read as 3 (505), with 2 also often confused for 8, which suggests the template for 2 is weak. Several other pairs, like 0→6, 5→3, 7→9, 9→3 and 1→8, show up as smaller but recurring errors.

I'm weighing a few ways to improve the classifier: tuning biases, or adding hand-built pairwise weights that separate the confusable digits, like 2 versus 3. I suspect my drawn 2 doesn't resemble typical MNIST 2s well enough, so I'm considering adding structural features such as end-stops and cavities.

I'm weighing a principled, hand-designed way to make the classifier more discriminative. Subtracting a mean over all class templates changes nothing, and a non-oriented occupancy penalty would just reduce orientation selectivity, so neither seems useful. Instead I'm thinking about per-pair structural features, starting with 2 versus 3: a 2 has a base stroke running to the bottom-left, while a 3 has its bowl on the right in the lower half and is open at the lower-left.

Comparing the two digit templates in terms of their bottom-left and lower-right cells, I notice the 3 template scores high on real 3s but also pulls in many 2s, while the 2 template only catches a small share of actual 2s. That points to my drawn 2 not matching typical MNIST shapes, maybe in where its base sits or how wide it is, since MNIST 2s tend to be wider than the width I gave it.

I'm thinking about whether to tune per-class gains, since the weak templates for 2 and 4 might need higher weighting to compete with over-predicted classes like 3. That's a crude fix, though, and I'm also wondering whether feedback from the confusion matrix could refine the templates more directly, even though it only gives me a hundred numbers per step. Then I want to look at the 4-versus-9 confusion, where the orientation features look nearly identical.

I'm checking why 4 keeps losing to 9: the 9 template has a top stroke closing its loop that a real 4 doesn't have, so the overlap should favor 4, yet 9 still wins most of the time. That suggests my 4 template is misplaced, perhaps its crossbar sits higher than in typical MNIST 4s, and I'm wondering whether the left stroke of the 4 is also positioned differently from the 9's loop.

I'm settling on a negative-weight scheme for 4, penalizing top-centre horizontal ink that the 4 template lacks, since that gap is what separates it from 9. The general form I'm considering subtracts a scaled version of the class-average template wherever a digit has no ink, so features common to other digits but absent from this one count against it.

I'm weighing whether to penalize ink in cells where a digit has no stroke, as an explicit negative term, rather than relying on cosine similarity alone. That would target the 4-versus-9 gap, since 9's top stroke is exactly what the 4 lacks. I'm still uneasy about whether using the other templates as a reference counts as a gray area, so I'm leaning toward a purely geometric version that depends only on the template's own coverage.

I'm working out a negative term for each template: wherever a digit's template has no ink, that empty region counts against it, so it can penalize the stray top stroke a 9 has but a 4 lacks. The intent is to shape each weight vector as a clipped function of the template's own coverage, with the same structure applied to every class.

I'm comparing the Euclidean form against cosine matching here: with a per-class offset, a template that penalises ink where it shouldn't be acts as a saturating box. The open question is normalisation. Classes with large support, like 8 and 3, would be treated differently in the mask term than in the cosine form, and I'm not yet sure whether that mismatch matters for the 4-versus-9 gap, where 9's top stroke is the unmatched part.

I'm checking why the 4 template is so weak: real 4s keep matching the 9 template better, and 9s almost never get classed as 4. The 4 template's left stroke and crossbar might be placed differently from typical 4s, so I'm considering whether its geometry is the real problem rather than the weighting scheme.

Now I'm working through where the 4 template's vertical stroke and crossbar land after scaling and centering, converting the normalized coordinates into pixel positions on the 28×28 grid.

I'm checking whether my 4 template's vertical stroke sits too central, since real 4s often look wider with the stroke farther right. Then I want to work out why the 9 template would match a real 4 better than my own 4 template does.

I'm working out where the 9 template's loop and stem land in pixel coordinates, and comparing that against where a typical real 4 would put its vertical stroke. I suspect my 4 template's vertical is placed too centrally, which could explain why real 4s keep matching the 9 template better.

I'm noticing that the 4 template seems to be the weak one, since real 4s keep matching the 9 template better. My guess is that the vertical stroke sits too central, and I'm wondering whether the "peaky" long-stroke templates like 4 lose out to the broader, curvier ones that pick up ink in many orientations.

I'm weighing whether to compress the templates with a square-root nonlinearity so they stop being so peaky, and whether to broaden the orientation tuning, since a thin straight stroke loses most of its match when it's displaced by a cell. Another option is to adjust per-class gains, though that's a cruder fix.

Now I'm looking at whether adding structural features, or keeping the template approach, would best help the classifier, and I'm wondering how the true class-mean features would behave.

I'm checking whether the real problem is the geometry of my 4 template rather than the weighting: its vertical stroke probably sits too central compared with typical MNIST 4s, which would explain why real 4s keep matching the 9 template better. I'm also wondering whether ink scale and the orientation responses for thick or curved strokes behave differently from what my model assumes.

Checking the diagonal filter response on a horizontal stroke, I'm summing the zero-mean weights over the three rows the stroke covers.

Checking the diagonal filter on a horizontal stroke: summing the zero-mean weights over the three rows it covers gives about 0.25 for a stroke 45° off, so after subtracting the bias it's around 0.2, where my cosine model would predict zero.

I'm now turning to how the tuning should model orientation leakage: a stroke 45° off still gives about 0.25 response, so I'm considering a floor term that keeps nearby orientations partially active instead of cutting them to zero.

I'm working out a correction to the tuning model: a stroke 45° off still gives roughly 0.25 response, so I'll use a floor that keeps nearby orientations partially active, and then check whether that changes the 4-versus-9 picture.

I'm comparing the 4 and 9 templates directly: both have a similar vertical and bar, so the difference comes down to the 9's top loop stroke versus the 4's extra bar extension to the right. Small geometric offsets in where the stem sits (around x≈16 for the 9 versus 15.6 for the 4) could decide these close calls, so I'll look for an explicit feature that separates them.

I'm now considering whether to build the 4 and 9 templates from shared parts, so their difference isolates the distinguishing strokes, and then add explicit negative weights where the two diverge. Pairwise contrast might sharpen the gap, but mismatched common geometry would still inject noise.

I'm moving toward structural features, since the main confusions (4/9, 5/3, 0/6) depend on shape rather than raw stroke pattern. For 4 versus 9, the key is whether there's a closed loop at the top, and for 0 versus 6, whether there's ink at the upper right.

I'm proposing explicit "forbidden strokes" with negative weights for each digit, for example a top bar between the verticals for 4, to separate it from 9. I'm also considering lowering 3's gain since it acts as a generalist that absorbs errors from 2, 5, 8, and 9.

I'm now listing a set of "forbidden" strokes for each digit, with negative weights where that stroke would argue against the class. For 2, that means a lower-right vertical, and for 5 an upper-right vertical and a lower-left vertical. For 3 it's the upper-left and lower-left verticals plus a lower-left diagonal, and 0 gets penalized for any ink through the centre. Finally, 6 is penalized for upper-right ink and 9 for lower-left ink.

I'm proposing hand-drawn "forbidden" strokes with negative weights for each digit, such as an extra bottom bar for 4 or a centre mark for 0, to push apart the pairs the confusion matrix flags. I'm also thinking about using the same transform as the positive strokes so they line up, then folding them into the templates with a scaling factor. I haven't settled how strong the penalties should be yet.

I'm adding negative-weight strokes for each digit, drawn along the shapes that distinguish it from its confusion partners, and broadening the orientation tuning so nearby angles keep some response.

I'm writing out the forbidden strokes for digit 0, placing horizontal, vertical, and both diagonal marks through the centre of its ellipse frame, since ink there would argue against a 0.

Now I'm deciding on forbidden strokes for the 1 template, since 1s keep getting read as 8s, most likely when they're thick or slanted and pick up the 8's centre diagonals.

I'm thinking about whether a 1 template needs more slanted variants, since MNIST 1s often lean well past upright. Slanted strokes around 25 degrees could be weighted lower than the upright one, and I'm checking whether that would stop them from matching the 8 template's diagonals.

Next I'm setting the slanted 1 variants to weights of 1.0, 0.7 and 0.4, so the more leaning strokes count for less, and then I'm considering 2's forbidden strokes: a lower-right vertical that 3 and 8 would have, plus a weaker upper-left mark for the start of the hook.

I'm adding a forbidden stroke for digit 2: a diagonal running from the upper left down toward the centre, which is where an 8's upper loop would put ink but a 2 wouldn't. I'm also checking the centre for a horizontal mark, since that's where 3's waist sits and a 2's diagonal passes through at a different angle.

I'm adding a forbidden vertical stroke on the left side of the 3 template, in the upper half between about y=0.2 and 0.45, since the 3's upper arc starts further right and that area should stay empty. I'm also considering a matching stroke lower on the left side, around y=0.55 to 0.8.

Now I'm working out the forbidden stroke for the 3 template's lower-left: a "/" diagonal running from roughly (0.08, 0.55) down to (−0.22, 0.88), which would catch 2-like ink there, since the 3's own lower tail curls the other way.

I'm adding a forbidden top bar for the 4 template, running across the upper part of the digit to push away 9-like ink, and a weaker bottom base bar to separate it from 2, 3, 6 and 8. I'll give the base bar a lower weight of 0.7.

I'm adding a forbidden vertical stroke for the 5 template on its right side in the upper half, plus a matching one on the left in the lower half, since the 5's bowl leaves that area empty. For the 6 I'm starting to think about a forbidden stroke on the upper right, around x=0.27 between y=0.05 and 0.38, where 0, 8, 9, 4 and 3 would put ink.

I'm adding a forbidden vertical stroke on the left of the 7 template in the upper half, since 9 and 4 would put ink there, and a weaker base bar to keep it apart from 2 and 3. I'm also noting that the 9's loop bottom sits near the 7's crossbar, so the upper left vertical is the main thing separating them.

I'm settling on the last few forbidden strokes for the 7 and 8 templates. The 7 gets a weaker horizontal mark across the left side of its loop region to keep it apart from 9, and a right-lower vertical to push it away from 3. For 8, which is being over-predicted across several digits, I'm planning to lower its gain rather than add any forbidden strokes.

I'm weighing a small bias shift for 8 instead of new strokes, since the 8 gain is what's pulling in 2s, 1s, 4s and 5s. I'll hold off on that until I see how the negative strokes on the other digits change things.

I'm now weighing a negative bias for 8 rather than more forbidden strokes, since 8 needs closed loops on both sides and a 2 or 5 can pick up enough of that to score well. I'm also considering whether a general penalty on classes with broad ink support would do the same job.

I'm tuning class biases now, giving 3, 8, 6 and 9 small negative offsets and 2 and 4 small positive ones, since the broad-support digits are winning too many ambiguous cases.

I'm settling the forbidden strokes for the 9 template: a vertical on the lower left that 6, 8 and 0 would put ink on, plus a weaker bottom bar on the left, since some 9s have hooked tails there. I'm also noting that 9→3 is the worst confusion for this template, so the upper-left vertical is what I need to keep empty.

I'm assigning the 9 template a forbidden vertical on its lower left and a weaker bottom bar there, since 6, 8 and 0 would put ink in those spots. For 6, the upper-right vertical keeps 9's loop side from being matched. I'm also setting the lambda weight for negative strokes to 1.0, so a forbidden stroke penalises ink as much as a matching stroke rewards it.

I'm weighing whether a looser forbidden-stroke weight of about 0.8 will keep real digits' natural variation from being penalised too hard, and I'm also checking whether the 6's upper-right forbidden stroke will stop 0s from being read as 6s. I still want to look at whether the 2 template itself needs a wider base or a rising end.

I'm checking whether 5s get read as 6s, and since the 6 template forbids ink on its upper right, I'm looking at whether the top bar of a 5 reaches that area.

Writing the stroke-loading code...

Still writing the loader, so I'm putting the code together.

Still writing the forbidden-stroke table for each digit template.

Still working out the forbidden strokes: the 4 template gets a top bar, a weaker base bar, and a vertical on the lower left, while the 3 template's lower-left diagonal is meant to catch 2-like ink.

Still working out the forbidden strokes, and the 2 template's diagonal runs the right way, so the open space to its upper left stays clear. Now I'm checking the 7's lower-right vertical at x=0.28, which should line up with the diagonal's path.

I'm checking how the 7's lower-right forbidden stroke sits against its own diagonal, since at that distance the blurred cells would overlap its real stroke and weaken the template in those spots.

Checking the 0 template's centre vertical: its strokes sit about 5.8 px from the forbidden line, so I'm halving that weight to 0.5 to avoid cancelling its own ink. For 2, I'm now checking the right-lower vertical against its own diagonal.

Still working out the forbidden strokes for the 3 template: the upper-left vertical sits about half a unit from the bowl's right side, so it stays clear, and I'm now placing the lower-left one.

I'm checking whether the forbidden strokes for the 3 template overlap with its own tail, since at that distance the blurred cells would cancel real ink. Shortening the lower-left forbidden stroke and lowering its weight looks like the fix, though the blur may still cause some overlap.

I'm checking the forbidden stroke for the 3 template against its own bowl, since the upper-right arc of the bowl sits close to the forbidden diagonal on the lower left and the blur would cancel some real ink there. Shortening that stroke and lowering its weight should keep the two apart.

I'm checking the 4 template's lower-left forbidden stroke against its own left stroke, which ends near y=0.55, so I'm shifting it down to y 0.72 to 0.95 to keep it clear of that end.

Checking the 5 template's forbidden strokes against its own bowl, and tightening the 6's upper-right stroke next.

Checking the 6's upper-right stroke for the overlap with its own loop, and tightening the 7's left-upper stroke against the diagonal.

Setting the 9 template's forbidden lower-left vertical to span y 0.68 to 0.92, since its loop's left side and stem sit about 3.5 px away. Next I'm settling the class biases, with a positive offset for 2 and 4, negative ones for 3, 6, 8 and 9, and λ dropped to 0.8.

Writing the 1 template variants and checking the 8-row counts, where 8→6 and 8→3 look fine, so I'm moving on to the code.
