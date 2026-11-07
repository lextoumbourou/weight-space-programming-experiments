I'm checking the early-stopping rule now: the best score has to improve by at least 0.5 points over the best from five steps earlier. Step 15 at 74.51 beats step 10's 73.15 by 1.36, which clears it, and at step 16 I'd need to reach 74.59 to beat step 11's 74.09.

I'm weighing bigger structural changes, since the early-stopping gate needs real gains each step. Candidate ideas include using the unused conv1 channels and temperature-scaling the logits, though I'm unsure whether a lower temperature helps accuracy. I'm also looking at the confusion pairs, especially 3 versus 5, and considering hand-tuned discriminant weights on the strokes that separate them.

I'm sketching hand-designed discriminant directions for the 3-versus-5 confusion, rather than relying on template differences, since the earlier broad approach failed. The plan is to map the relevant upper-left stroke for 5 and upper-right stroke for 3 onto the feature grid, accounting for shear and centre of mass.

I'm working out a hand-drawn discriminant for the 3-versus-5 confusion: a top-left stroke that belongs to 5 and an upper-right curve that belongs to 3. The shear shifts those positions only slightly, so the cell mapping stays manageable. Rather than deriving weights from template differences, I'm planning to render just those partial strokes and push the weights in opposite directions for the two digits.

I'm designing targeted discriminant strokes for the 5-versus-8 pair next: the top bar and left vertical belong to 5, while the right side of 8's top loop is the feature to weight against it. I'll need to handle the offset carefully so the partial strokes line up with the digit's centre of mass.

I'm now sketching the 5-versus-6 discriminant: the top bar of 5 set against the lower-left vertical that belongs to 6, with the offset kept consistent so the partial strokes line up.

I'm working out a targeted discriminant for 7 versus 9, where the loop's left side belongs to 9 and the flat top bar is what 7 has instead.

Still working out the arc and stroke layout for the 9 and 7 pair, then moving on to 4 versus 1 with a horizontal bar and left stroke as the distinguishing part.

I'm mapping out hand-designed discriminant strokes for the 8-versus-1 and 2-versus-8 pairs, using the loop sides that 8 has and the bottom bar that 2 has, and weighting them in opposite directions for each digit.

I'm settling on the 3-versus-8 case: the left-side strokes of 8's loops are the features to weight positively for 8 and negatively for 3, and I'm still weighing whether a cusp stroke would help separate them.

I'm settling the scale for these partial-stroke features: each part gets normalized to unit length and weighted at about 0.25 times the template scale. Changing one class's weights also touches the other classes in the pair, so I'll check that the side effects on neighbouring digits stay acceptable. After that, the biases will need retuning because the added weights move the mean logits.

I'm settling on a moderate scale of 0.3 for these partial-stroke weights, and I'm wondering whether the positive additions will push some classes, like 8, up on inputs that have ink in those regions. Using paired differences should keep things roughly balanced, though I still need to decide whether to keep the biases unchanged. I also need the partial renders to share the full digit's centre-of-mass offset and shear, so I'll pass that offset into the render function.

Still writing the discriminant pairs, listing the 5-versus-3 stroke comparison and the next few pair definitions...

Still writing the pair definitions, with the 4-versus-1 and 8-versus-1 entries in place, and I'm checking whether the 8 side picks up too many positive weights.

Still writing the pair definitions, setting the weight scale to 0.3 times 9 and applying the one-sided updates by adding to the positive class and subtracting from the other.
