The model is at 90.5% with loss 0.328 and 24 steps left. The biggest remaining confusions are 5→3 (58 errors) and 8→5 (53), followed closely by 2→3 and 9→7.

I'm weighing whether to tune the scales and biases, which looks like a few steps for a modest loss gain, or to add targeted features. The pairs worth targeting are 9 against 7 and 8, 5 against 3, and 0 against 2, 8 and 5, since those account for most of the remaining errors.

I'm circling back to hole detection for the 0, 9, 6 and 8 confusions, wondering whether a centre-versus-surroundings test can work inside conv2 despite the lack of a clean minimum over directions. The endpoint idea also seems to already capture closure, since 0s and 8s have no open ends, so I'm weighing whether refining the per-cell endpoint tables or improving the naive Bayes feed is the better use of the remaining steps.

I'm considering a cheap bias correction: nudging each class bias by a step proportional to the log ratio of true to predicted counts. That would push 9 up by roughly 0.3 and 3 down by about 0.2, with smaller moves for 5, 0 and 6. I'm also wondering whether the model is over- or under-confident, which I'd check with temperature scaling.

I'm weighing whether a temperature change could improve the loss, though it would be hard to separate from any bias adjustment. Since the lowest-training-loss step is what gets selected, and higher accuracy usually tracks lower loss, I'd rather not spend many steps on temperature.

I'm weighing a few ways to squeeze out more accuracy with the steps left. Probing the unmeasured "/" presence cells looks like a modest gain, and a second-order feature to capture the pairwise dependencies that naive Bayes misses might help more.

I'm thinking about using long-stroke features, measured at a higher mass threshold, to separate 9 from 7 and 2 from 3: a long horizontal bar at the top might point to 7, and a long base at the bottom to 2.

I'm weighing whether to spend the remaining steps on high-mass "long stroke" features, such as heavy horizontal ink at the top or bottom, to separate 9 from 7 and 2 from 3. I'd have to probe several heavy-presence cells to make that work, so it's a costly option.

I'm weighing a few more ideas for the remaining steps: a line search on one scalar to pin down a pair-specific bias, per-orientation scale factors or dropping redundant features to counter the correlation problem in naive Bayes, or new conv2 channels that AND two presence cells together.

I'm considering an enclosure detector that sums vertical presence at the left and right sides of a row with horizontal presence at the top and middle, a fixed ring roughly six pixels across. Each single-cell term is capped at one, so a threshold of three across four terms should only fire when the ring is closed.

I'm working out a ring detector from four single-cell presence terms, each capped at one, so a threshold of three only fires on a closed loop of a fixed size. The catch is that it would only match loops of one exact dimension, so I'm weighing whether to run several ring sizes in parallel, with each side allowed to match either of two adjacent cells.

I'm checking whether a ring detector built from four capped single-cell presence terms can separate closed loops from open strokes. With each side contributing roughly 1 to 1.4, a threshold of 3 would let three strong sides pass by mistake, so I'm considering a higher threshold of about 3.5 to rule that out.

I'm now weighing a ring detector built from four single-cell presence terms, which could separate closed loops from open strokes, though it would only match loops of one fixed size. Checking the 9-versus-7 errors, the misclassified 9s are probably the ones with small, squashed, or open loops, and a ring detector wouldn't fire on those either.

I'm now weighing "heavy stroke" features to separate 5 from 3, since 58 fives are being called threes. The 5s and 3s differ at the top, where a 5 carries a left vertical while a 3 carries an upper-right bowl, and those cues are already in the model, yet many 5s still slip through.

I'm now comparing the 5-versus-3 and 2-versus-3 confusions, and wondering whether a different kind of spatial information, perhaps finer localisation near the centre, would help more than tuning biases. Tuning biases with a few more steps might gain half a point or so, so I'm weighing that against new features.

I'm considering whether a probe could estimate pairwise discriminant weights directly, perhaps by looking at feature frequencies among the 5-to-3 misclassifications, though that would need the probe to condition on the previous classifier's errors.

I'm working out whether a probe can read off the previous classifier's decisions jointly with a feature bit, but with ten classes that would need twenty outcomes, so I'm considering dropping a few rarely predicted classes to fit the budget.

I'm now weighing a different route: measuring, for images of true 5s predicted as 3 versus predicted as 5, how often each feature fires, then using those frequencies to correct the weights. That would need a probe to condition on the earlier classifier's decision, which seems too slow for the steps left. Looking at the 9-versus-7 pair, the 9s carry a left-side vertical at the upper-left and middle-left, a backslash stroke lower down, and a horizontal bar near the middle, features that separate them from 7s.

I'm now looking at whether the remaining 9-versus-7 errors are simply hard cases where the features don't differ, since small or open loops wouldn't trigger a ring detector either. A more promising route might be shifted, half-cell presence grids that capture positions between the current 4-pixel cells.

I'm now weighing "heavy" features based on stroke length: long vertical strokes for 1, 4, 7 and 9, and long horizontal bars for 7, 2, 5 and 4, against short arcs in the other digits. Measuring horizontal presence in the top and bottom rows could separate 2 from 3 and 7 from 3 and 9.

I'm sketching a "heavy" feature that fires only when a stroke run exceeds some length A, using a graded score that drops from 1 to 0 as the measured amount rises to 2A, so that the probe's 0.5 threshold lands at A. I'm also considering how that would add horizontal bars at rows 0 and 3 and at row 2 for the 4's crossbar, plus vertical ones, for roughly seven more steps and maybe a gain of about one percent.

I'm working out how a "heavy" amount feature would behave: its value drops linearly from 1 toward 0 as the measured stroke amount rises to 8, so it works as a graded linear amount term. Full-height vertical strokes and long horizontal bars would land near 5.7, a shorter centred bar closer to 4.3, and the pooled version takes the minimum over shifts.

I'm sizing up a "heavy stroke" feature: a graded amount that falls from 1 to 0 as the measured stroke length grows, so a threshold near 4.5 separates long centred strokes from shorter ones. Covering the full set of positions would take around seven steps, so I'm considering a smaller subset first, such as horizontal bars in the top and bottom rows and vertical stems, and running the cheap bias correction before that.

I'm going to adjust the biases rather than the scales, since the confusion counts are lopsided: 9s are called 7s far more often than the reverse, and 5s are called 3s far more often than 3s are called 5s. Shifting the 9 and 5 biases upward relative to their confusable partners looks like the cheapest gain, and I'll run that as step 27.

I'm now going through the confusion counts to see which classes are over-predicted. Class 3 absorbs too many errors, while 0, 9 and 6 are under-predicted, so I'm sketching small bias shifts for each class, with a few tenths of a logit up for 0, 9 and 6 and slightly down for 3 and 5. The margins among the confusable pairs are roughly one logit, so shifts of that size should flip only a modest share of the borderline cases. I'll apply those biases as step 27.

I'm deciding against changing the scales at the same time, so I can see what the bias shifts alone do. Going ahead with step 27.
