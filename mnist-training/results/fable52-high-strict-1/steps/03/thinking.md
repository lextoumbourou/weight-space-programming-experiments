At 49.6% progress, class 8 is still being over-predicted, with 3845 predictions. A negative bias on 8 looks like the simple fix, but I want to understand why it wins in the first place: its template covers the center columns with many strokes, so it's a generic shape. Under cosine similarity, a broad template overlapping everything scores decently against every input, which explains the bias.

I'm weighing a hand-specified negative stroke or region per class rather than subtracting a mean template, since the mean could look like deriving weights from generated feature vectors. For how much to bias 8, I don't know the margin distribution, so I'm estimating from the logit scale and typical cosine differences.

I'm still weighing how strong a negative bias to put on class 8, since too much would cost the 8s I already get right. A more principled angle is why 8's template wins so often: its broad central strokes overlap many digits. The slanted 1s look especially close to it, because a diagonal stroke through the center matches 8's central diagonal, and 1's own template is dominated by its vertical stroke.

I'm considering penalizing the features that 1 never has, and for 8 the question is which features it never has, like a narrow bottom tip.

I'm checking whether the features that 0, 2, and 6 have but 8 lacks, like ink on the far left and right in the middle rows, could push those inputs away from 8, since 8's center waist is the part that makes it win.

I'm trying to work out why class 0 loses to 8 on real zeros: a rounder zero probably puts ink in different columns than my template, so 8's broad center overlap still wins on cosine.

I'm thinking about how to separate class 0 from 8: 0 has vertical strokes at the outer sides in the middle rows, while 8 has diagonals through the center. So I'm considering negative weights on 8's template for the outer-column vertical strokes that 8 doesn't have.

I'm thinking about whether a negative weight on class 8 for the outer-column vertical strokes would separate it from 0, since 0 has those in the middle rows and 8 doesn't. The trouble is that 8's vertical strokes sit in wide row windows, so the boundary isn't clean.

I'm noticing that subtracting a shared mean from every class template wouldn't change the argmax at all, since the same vector is removed from each score, so centering doesn't help here. That leaves a simple per-class bias on 8 as the more practical fix, and I'd need to tune its size carefully so I don't lose the 8s I already get right.

Now I'm weighing how to set per-class biases using feedback, since the raw template scale doesn't settle things. The predicted counts show 8 at 3845 far above its share, with 6 and 3 also high and 2, 4, 5 low, so I'd nudge each bias toward roughly equal prediction counts.

I'm settling on how to convert these counts into per-class biases: class 8 gets the biggest cut, since it's predicted 3845 times against a target near 1000, with 3 and 9 pulled down a little, and the classes that are under-predicted nudged up. I don't know the margin distribution, so I'm guessing the logit spread is around 1 to 2. The loss of 1.49 at 50% accuracy suggests the margins are fairly small, which means the biases shouldn't be too large.

I'm settling on roughly −1.0 for class 8, since the loss of 1.49 suggests the logit margins are order one, so a bias of about ±0.5 to 1 is a meaningful adjustment. I also want sharper templates for the 5-versus-3 and 5-versus-6 confusions, and I'm starting to think about negative weights on class 3 for the features 5 has.

I'm working through the remaining confusions: for class 4, I'm considering negative weights on the horizontal bar at the top and on the full vertical structure, while class 9 would get a penalty on the top tips and class 8 a negative on its features that 4 and 9 don't have.

I'm comparing class 7 against 9 now: the difference is mostly the loop, since 9 has ink on the left-of-center and the lower-right features that 7 lacks. So I'm considering positive weights on those loop features for 9 to offset the shared top bar and stem.

I'm weighing whether to lower class 9's bias and raise the gain on its loop features, since 7 can be separated from 9 mostly by the presence of the lower-right and left-of-center loop ink.

I'm settling on a structural term per class: a region-based penalty or reward on the LR and UD features, thresholded around 0.35, so that absent required strokes count against a class and forbidden ones count against it too. Since those pooled features may be noisy, I'll keep the weights moderate, and I'm sorting the grid into row and column bands so each rule applies to a clear region.

I'm now setting up explicit rules for each class: a required pattern at certain points, and a penalty on channels that class should never have. The class 1 and class 7 rules both penalize the left-right and up-down features, since neither class has them.

I'm sorting out the forbidden and required channels for each class, which ones should be penalized or rewarded, and I'm now working through class 10 for the upper-left channel.

I'm now listing which structural channels each class should forbid or reward: class 9 gets penalized on the upper-left and upper-right channels, class 2 is rewarded on the upper tip and penalized in the lower region, and class 5 is rewarded in the lower region only. I'm also noting that the top tip is required for class 1 and class 4, and kept only mildly forbidden for 2 and 3.

I'm now going through the rest of the per-class channel rules: the bottom stroke, the left and right tips, and which classes should be penalized or rewarded on each.

I'm now folding the structural terms into the template: the orientation channels keep their cosine normalization, while the forbidden and required channels get added as unnormalized weights. Each required point also gets a threshold offset in the class bias, so that a missing stroke costs the class rather than being silently ignored.

I'm weighing whether to add the structural terms all at once, since a misfiring detector could penalize the true class. Each required feature would contribute a moderate positive or negative amount around the threshold, and forbidden features a smaller penalty, so the scale stays comparable to the orientation differences. Still, I'm asking whether changing this many parts together is wise, or whether I should stage the rollout to isolate any bad detector.

I'm considering a quick probe to check how reliable the structural detectors are, since a single argmax-based output could reveal each feature's firing rate in the confusion matrix. Spending one or two steps on that before committing to the full set of structural rules seems worthwhile.

I'm weighing a probe that would read out a single scalar feature by mapping it to argmax bins, one bin per class, to get its distribution per true class in one run.

I'm weighing whether a couple of probe steps are worth spending, since 13 steps remain and each one is costly. A probe that thresholds three features at once could reveal whether the structural detectors are actually reliable before I commit to the full rule set, though direct iteration on accuracy would also be informative. I haven't decided yet which path is better.

I'm weighing whether to probe the detectors directly: a single step that thresholds three features and reads the eight resulting combinations per class could show how reliable they are before I commit to the full rule set.

I'm weighing whether to run a probe that thresholds three structural features at once, since their eight joint outcomes could separate most of the classes. That would test the detectors before I commit to the full rule set, though direct accuracy iteration would also tell me something.

I'm checking whether the structural features are reliable enough to lean on, since a simple threshold on each one would make the classifier's confusions reveal which detector is failing. Then I'll look at how big the summed template response gets when a feature is present, to choose thresholds.

I'm estimating how strongly the loop-hole feature fires: across one to two pooled cells per axis, its weighted sum comes to roughly 0.8 to 2.5, comfortably above the 0.4 threshold when present.

Scaling the required and forbidden terms with A = 1.2 gives about +1 when a required feature is present and −0.5 when it is absent, while a forbidden feature that fires costs roughly 1.2 units. The thresholds are set per feature: 0.35 for the bottom stroke and 0.2 for the tips, since the thin top stroke only reaches 0.4 to 0.75.

I'm settling the normalization: only the orientation channels go into the cosine norm, so each class norm is roughly sqrt(40-80). Then I'm reconsidering the biases, since the old confusion pattern no longer maps cleanly onto the new structure, and 8 was winning partly through its structural overlap with LR and UD.

I'm going to keep the structural terms unnormalized alongside the cosine orientation scores, and then give 8 a modest negative bias since its generic template still wins too often. I'm also checking whether class 3 is leaking predictions from 5, 2, and 9.

I'm checking the class 2 errors next: it leaks into 8 and 3, and its bottom-right tip falls outside the current right-tip coverage.

Checking the remaining confusion pairs against the new structural terms: 7 falls to 9 because 9 requires top LR and UD and gets a penalty when they're missing, and 7 goes to 3 and 8 where those forbid rules apply. For 4, 9 loses on the missing top UD and the top-tip penalty, though 8 still wins some of those cases. 9 to 8 should be cut by the bottom-tip penalty on 8, and 1 to 8 still needs checking.

Now I'm checking the remaining confusion pairs by hand: 0 goes to 8 and 6, but 6 needs a bottom UD that 0 lacks. 6 to 8 is only partly covered by the forbid rules. For 5 to 6, 6 requires a bottom LR that 5 doesn't have, and 5's lower UDL should count against 6. I'll set per-class forbid strengths per channel next, scaled from a base of 0.5.

I'm settling on a per-channel forbid strength for each class, so the cells where a class's template is zero get penalized, while cells with some template weight are left alone.

I'm setting the per-channel forbid strengths as a table: each class gets a value for every structural channel, with zero-template cells penalized more heavily where the class is supposed to be absent.

Now I'm setting per-class forbid strengths for the bottom-tip channel, giving class 8 and class 9 the heaviest penalties where their templates are absent, and assigning light values to the classes that need the tip.

Now I'm setting the thresholds for each feature: a required feature adds a bias penalty scaled by the per-channel threshold, so the left and right tips and the top and bottom strokes each get their own cutoff.

I'm setting the per-point bias penalty for each required feature, scaling the threshold by a per-channel gain so the tip channels (top and left) get a 1.5 multiplier to offset their weaker magnitudes, while the others stay at 1.

Setting the attenuation to A = 1.2 and the orientation gain to S = 1.5, I'm now writing the per-channel gains and assembling the feature-correction terms in the classifier code.

Still writing the per-channel forbid table and the weighting code: each class gets a strength for every structural channel, and the penalties apply only where that class's template is near zero, with the bottom-tip channel restricted to the bottom row.

Still writing the forbid and threshold code for the class-channel table...
