I'm overshooting: predicting 4 now happens 3150 times, while predicting 1 is right only 60 times, with 795 ones coming out as 4. The bias shifts I used, 22 and −20 for a raw difference of 42, were too big, so the margin scale must be closer to 20 than the 62 I'd estimated. That heavy-tailed loss threw me off.

I'm checking the 1-versus-4 margins: at a 42-point shift nearly all the 1s flip to 4, so those margins must sit within about 42. Fitting a rough per-class model gives a scale of around 12, far below the 62 I had assumed. That means the bias corrections should be about a quarter of what I used, something like +5 for 4, 8 and 9, and −5 for 1.

I'm now working through the per-class counts before and after the shifts, tracking how the predicted totals move for each digit.

I'm estimating per-digit bias corrections from the predicted counts: digit 4 needs about +7.5, digit 9 about +11, and digit 1 has to come down a lot, since it dropped from around 1500 predictions to 60.

I'm scaling all the bias corrections down by about 0.3, which puts digit 1 at roughly −6 and digit 4 at about +6.6. With the margin scale near 12, a 12.6-point gap between 1 and 4 still leaves about 80% of the 1s correct, so that seems workable.

I'm checking whether shifting the bias for 1 against 4 is worth it, since moving 1s toward 4 would cost about 190 correct 1s while the 4 column gains little.

I'm checking whether a smaller 4-versus-1 shift would help: the earlier numbers suggest 1s and 4s sit close together, so a shift around 8 might keep most 1s while cutting the 1-to-4 errors. My rough model puts the cost of that shift at roughly 115 misclassified 1s, which I'm weighing against the 4s I'd recover.

I'm weighing a few options for the remaining seven steps, since the bias tuning between 1 and 4 looks like it can only recover a few points.

I'm weighing three candidate approaches for the remaining steps, with the blurred-feature cosine design looking most promising, since dropping the G and K evidence that points the wrong way should recover a few points.

I'm weighing whether to fix the step-5 blurred-feature design by dropping the G and K evidence that points the wrong way and reweighting the rest from the per-digit signatures I measured.

I'm converting the measured per-digit firing rates into log-odds weights for the blurred-feature signature, so the digits that fire often get positive weight and the rare ones go negative.

I'm normalizing the per-digit log-odds for the D and G evidence, which gives the signed weights I'll use for the blurred-feature score.

I'm settling on the measured per-digit blurred-feature signatures, with the weak G evidence either dropped or kept at a small weight, since its logits sit close to the middle and saturate at the threshold.

I'm converting the per-digit firing rates into log-odds for the K evidence, centering them on the mean, and halving the result. That leaves 1 and 3 slightly negative, 2 and 6 positive, and the rest near zero.

I'm checking the measured per-digit firing rates for the blurred-feature signatures, noting that feature 6 pushes the wrong way and feature 8 has no weight yet. For the botH bins, the rates are clear for most digits, but 8 sits in the middle, so its weight should stay near zero. Other feature types still need their own measurements.

I'm now going through which features might leak across digits after blurring, since my guesses for G and K on 1s were off. The top-right feature probably fires for a 1 and for a 6, so my negative weight for 6 there is likely wrong. The bottom-left feature may fire partly for 1 and 7, which means my earlier −0.8 for 1 there is probably wrong too.

I'm weighing whether the blurred-feature design can be rescued: the horizontal vertical-stroke features look unreliable after blurring, while the row-based features separated by vertical position should hold up better. I'm estimating that fixing the design could bring it to roughly 75–77%, and I'm also considering a sharp-feature version with its own unknown calibration as an alternative.

I'm weighing whether an ensemble of the blurred and sharp features is possible, since the blurred features are roughly linear combinations of the same maps. I'm considering whether the step-5 classifier can be re-expressed on sharp features, though it won't match exactly because of the pooling. Given that both approaches sit around 70–74%, I'm leaning toward a data-driven probe approach, which seems like the only way to get reliable knowledge of the features.

I'm thinking about whether to spend the last few probes on six more blurred-space features and then fold all twelve measured features into a log-odds classifier on top of the cosine template, which I'd expect to land above 80%.

I'm still weighing which feature space to commit to: the blurred features I've already measured for items A and D look reliable, but sharp features might give cleaner separation for some digit pairs. Switching to sharp would mean remeasuring those two, and I'm not sure the cost is worth it yet.

I'm weighing two plans for the remaining steps: refining the blurred-feature classifier with the corrected signatures and a few more probes, or switching to sharp features and measuring them from scratch.

I'm thinking about switching to sharp features instead, with about twelve binary features built from zones of the image, since digits map onto segment-like patterns much as they do on a seven-segment display.

I'm mapping my seven measured features onto the segments of a seven-segment display, where each digit lights a particular subset. Under that code every digit gets a distinct pattern, and the segment letters line up with the features I've been measuring.

I'm now mapping the seven measured features onto a seven-segment display code, since each digit lights a particular subset of segments. In handwritten digits the strokes sit at slightly different horizontal positions than in a clean display, so the sharp-feature zones would need to be positioned around the centre-of-mass rather than fixed columns.

I'm checking whether the seven segment-like features, with sharp cells in the right column, can separate the digits, since the lower-right feature already splits {0,3,5,6,8} from {1,2,7}. I estimate a naive Bayes classifier on around nine to twelve measured sharp features could reach 80–85%, which beats the current 74%, though it takes a few probe steps and the independence assumption is a risk.

I'm treating the seven measured features as segments of a display and weighing whether to hard-code measured probabilities into a naive Bayes classifier. I'm also considering whether three probes per step, or ten outcomes with one ternary feature, would make better use of the remaining budget.

I'm settling on a sharp-feature design where a feature counts how many cells in a zone are active, with a threshold of about one or two cells, so the thresholds don't need separate calibration. Next I'm picking the zones and their orientations around the sharp bank layout.

I'm laying out the sharp-bank zones for the remaining features, each as a set of row and column boxes around the stroke positions, and checking whether the boxes sit where the stroke centres should fall.

I'm laying out the zone features now, working through the sharp-bank rows and columns to choose which cells each one covers. The first candidate is a horizontal-stroke feature for the top of the digit, summing cells from the top rows of the banks, and I'm checking whether a total threshold rather than a per-cell calibration will keep it usable.

I'm settling the threshold question: a fixed θ near 0.7 makes each feature mean "a stroke of this orientation is present in the zone," which is what I want for the measured probabilities. The catch is that the count r stays unbounded, so the evidence has to be handled as a thresholded binary rather than a linear term.

I'm checking whether a thresholded count of active cells, with θ around 1.0, can act as a roughly binary feature: absent gives zero, present gives a value near 1–3, so the weight on the difference stays close to a clean yes/no signal.

I'm planning to split the remaining probes into three zone features per step, using a threshold of 1.0 so each feature reads roughly as present or absent. I'll spend steps 9 through 11 measuring them, then use the last few steps to build and test the classifier, weighing whether one more probe is worth it.

I'm weighing whether the sharp-cell naive Bayes base, which only reached about 70%, is strong enough to combine with nine measured features; I expect the measured evidence to help most on the main confusions, since my guessed weights have been unreliable.

I'm converting each measured feature into a linear term: the log-odds of the measured probability sets the slope, and log(1−P) sets the intercept, with the count r standing in for the binary presence signal.

I'm settling on the first zone feature, a horizontal-stroke check in the top band, using two banks' worth of cells at the columns where a top bar would sit, so I can test whether it separates the digits.

I'm assigning the top-bar feature to the top row of the first bank plus the first row of the second, expecting 7, 5, 2, 3, 9, 0 and 8 to light up and 1, 4 and 6 to stay dark. For the middle horizontal, I'm pulling cells from the middle band of two banks, where 4, 5, 6, 9 and 3 should show a stroke and 0, 1 and 7 should not, though 4's bar sits right on the edge of that band.

I'm sorting the zone features into bands: the mid-horizontal feature takes five cells from the middle rows so it covers the 4's bar, and the bottom-horizontal feature takes four bottom cells from one bank plus two from the next.

I'm defining the upper-left vertical zone from the sharp bank cells, using the first two rows of two banks plus a short column, and expecting 0, 4, 5, 6, 8 and 9 to light it while 1 and 2 stay dark.

I'm checking the upper-right vertical zone next: four cells in the top two rows of the right-hand banks, which should light up for 0, 2, 3, 4, 7, 8 and 9, but the 6's upper tip and the 1's position around x 14 make 5 and 6 uncertain.

I'm now defining the lower-right vertical zone, the mirror of the lower-left one, to cover the right-hand strokes of the lower half of the digit.

I'm defining the centre-lower vertical zone from the middle columns of the sharp banks, covering the stem region below the midline, and expecting it to light up for the digits with a centre stroke there.

I'm defining the last few zone features: a centre diagonal zone for the "/" stroke and a second one for the "\" stroke, both taking four cells from the middle of the banks, and I'm noting which digits should light each one up.

I'm picking the last features for the classifier: a zone for the upper-middle vertical stroke, which should catch 1 and 6, and a bottom-right horizontal cell that picks up the base of the 2. That gives nine features across three probes, and I'll leave the extra centre-diagonal probe for later if there's a fourth.

I'm checking the threshold for the zone features before probing: each zone sums a handful of cells, so a top bar should give a count of about 2 to 4, while a 9's loop top gives 1 to 2.5, and a threshold of 1.0 still separates them.

I'm going to probe the bottom-horizontal, top-horizontal and middle-horizontal zones first, since they're the most useful to know early. After that come the upper-left, upper-right and lower-left verticals, and the lower-right vertical, centre-lower and centre-diagonal zones last. I'll decide later whether to check the classifier between probes.

Setting up the probe encoding now: I'll map the three horizontal-band features to bits, with top as bit 0, middle as bit 1, and bottom as bit 2. Each feature becomes a 16×4×4 array with ones at the chosen bank, orientation, row and column cells, using the channel index 4·bank + orientation.

I'm finishing the cell layout for the middle-horizontal and bottom-horizontal zones, with the bottom one taking four cells from its row plus two from the next bank. I'm also setting θ to 1.0 for each zone and noting that the convolution layers stay on the sharp configuration while I run the probe.
