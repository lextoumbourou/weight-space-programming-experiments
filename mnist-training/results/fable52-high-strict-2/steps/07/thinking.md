I'm decoding k as a bitmask over the G, K, and D bits, where each value of k maps to a specific combination of those flags. Then I'm tallying the per-class totals for digit 0, which come to N=991, and working out the probability of G as the sum of the odd-k counts, about .68. For K I'm adding up the counts where k is 2, 3, 6, or 7.

I'm checking whether K firing at 84% for the digit 0 is a real result or a sign my orientation convention is flipped. My D1 "/" definition and the template angle calculation agree, so I'm now testing the 0's lower-left arc segment against the D1 and V templates to see which one it actually matches.

Now I'm tallying the digit 1 counts, which total N=1064, and the probability of G for that digit comes out to about .85. Then I'm working out how the lower-left arc of the 0 gets picked up by the V and D1 templates.

Digit 1 gives G, D, and K each high rates even though the stroke sits between the ulV and lrV templates at x=9.7 and x=17.7, about 4 px away. I'm now thinking the blur must be large enough that a long vertical stroke drives responses above 1.0 for templates several pixels to either side.

I'm reasoning that the neighbouring cells on either side of the 1's stroke are picking up most of its response. The cell at column 11.5 sits about 2 px from the stroke, so even after blurring it reaches roughly half its full value, which pushes the response to around 1.0 to 1.3. That means the horizontal resolution of these features is poor.

I'm checking whether a stroke about 4 px away from a cell's centre still drives its response much, given how much the blur and pooling spread things out. My estimate is that the response falls to roughly .3 to .6 at that distance, so the features are smeared enough that neighbouring positions 4 px apart are hard to tell apart.

Now I'm tallying digit 2's counts, N=990, and the probability of G comes to about .54, with K at about .94. Before going further I want the decoding settled, so I'm checking the per-class totals for digit 1 against the other digits.

Now I'm tallying the remaining digits' class probabilities, covering digits 2 through 5 and their G, K, and D rates.

Now I'm tallying the remaining class probabilities for digits 6 and 7, with G, K, and D rates for each.

Now I'm checking the digit 8 and digit 9 totals, and the probability of G for the digit 9 comes out to about .90, which is the highest so far.

Those per-class rates show the lower-right and upper-left features are not separating digits well: the lower-right template fires above 0.8 for 1 and 7, so my earlier signature was wrong. The upper-left template is informative, staying low for 2, 3, and 7 and high for 4, 6, and 8.

I'm checking whether the blur is really broad enough that a 1's stroke, about 5 px from the upper-left and lower-right templates, still drives their responses above 1.0. The 73% and 85% rates for those templates on digit 1 suggest it is, which would mean these features are far less localised than I had assumed.

I'm working out how far the ulV template's footprint reaches horizontally: its weights on the two nearby cells come out roughly equal, while the cell about 6 px away contributes almost nothing.

I'm working out the horizontal spread of the blur, checking how a stroke at x=14.5 falls across the pooled columns at 10.5 and 12.5. The offsets give weights of about .6 and .135, and if the stroke also covers two adjacent columns, the nearer one could reach a full 1.0.

I'm working out the blur's horizontal reach: a stroke at x=14.5 lands on the cell at 11.5 with a value of roughly 0.6 to 1.0, about the same as a stroke at x=9.7 would give. So that cell can't reliably tell those two positions apart, and its effective receptive field spans roughly three pixels either side of its centre.

Measured against those blur numbers, the spatial resolution is poor at σ=1 pool unit, so the next step is to try a narrower blur in conv2, around σ=0.5, to sharpen the localisation.

I'm weighing a narrower blur in the second convolution, around σ=0.5 pool units, so that each cell covers only its own two pool columns, about 4 px wide. That would sharpen left-right discrimination, though a hard-edged template might become brittle under small shifts.

I'm weighing whether blurring the features versus blurring the template makes any difference, since blur is linear and can be moved onto the template. That means sharper conv2 kernels lose nothing, apart from the max-pool step in between. I'll need to render the base templates with a larger blur width, around 3.0 px, to offset the change.

Now I'm working out how the blur's horizontal spread compares with sharper cells: with narrow fields of about 4 px, each bank tiles the centre more finely, and the row offsets give overlapping coverage.

I'm weighing whether to keep all three banks with the same column offsets or shift them so the cells split the horizontal axis more finely. Four banks of four orientations would give sharper left-right separation, but I'm questioning whether the ending channels are worth keeping, since I haven't measured them after the redesign.

I'm now looking at a four-bank layout with offsets chosen so the cells split the horizontal axis more finely, and I'm working out which row and column offsets cover the digit's extent.

I'm sketching how four banks with half-cell offsets in rows and columns could sample the digit's region more finely than the three banks I had.

I'm sorting out how to place four banks of four orientations, using row and column offsets of half a cell so the sampling is finer in both directions. The ending channels are doubtful now that the layout has changed, so I'm leaning toward dropping them.

I'm settling on four banks of four orientations, with the column offsets set so one bank has a centred cell covering 11.5 to 15.5 pixels, which should pick up the 1's stem and the 0's hole. The right edge out to about 21.5 pixels is left to the other column offset.

I'm settling on four banks of four orientations with no ending channels, and I'm picking offsets for the fourth bank (either (1,3) or (3,1)) so the set covers both the centred cell and the right edge.

I'm comparing which bank offsets cover the vertical extremes: the ca=1 and ca=3 banks reach the top and bottom strokes, while ca=2 has its own top and bottom cells that also catch bars around y=5–6.

I'm settling on four banks of four orientations each, using row and column offsets of one pool unit, so the centred column cell catches the 1's stem and the 0's hole while the outer offsets reach the edges. That leaves the top and bottom extremes covered by the row shifts at 1 and 3.

I'm weighing a layout where two banks offset by half a cell, rows at 5.5 through 19.5 and 7.5 through 19.5, give an even 2-pixel spacing down the digit. The ca=1 and ca=3 pairing would duplicate most rows, so I'm checking whether the bottom edge near y=22 is still reached by the ca=2 cell.

Now I'm working out where the top strokes sit: the tops of the digits fall around rows 4 to 6, so the stroke centre is near row 5, which is pool row 1. That's why the ca=1 bank is needed for the upper edge, while ca=3 handles the bottom strokes near rows 22 to 23.

I'm checking where the top and bottom strokes sit: the top edge falls around pool row 1, which the ca=1 bank covers, and the bottom edge around pool row 10, which only the ca=3 bank reaches. That means the three row offsets are all needed, though ca=1 and ca=3 overlap on some rows.

I'm checking whether pairing the first and third row offsets with different column offsets avoids duplicate cells, and seeing that a same-column pairing still overlaps in the middle rows.

I'm settling on four banks: P at offsets (1,1), Q at (3,2), R at (2,2), and S at (2,1), so the row and column sampling interleaves without duplicating cells. Each bank covers a different part of the digit's extent, and together they should reach both the top and bottom strokes.

I'm checking how the top and bottom edges are covered, and seeing that the top-right corner is only partly caught by the banks offset in rows and columns. I'm settling on four banks in total and dropping the ending channels. Next I'm weighing whether a single-tap kernel, taking the maximum over a 2x2 pool region, is sharp enough to keep orientation information.

I'm weighing whether a single-tap max over each pooled cell, which just asks whether a stroke of a given orientation is present in the box, is better than summing responses along the stroke. Presence-only features ignore stroke length and thickness, which seems more robust, so I'm leaning toward binary cells and templates rendered as soft presence probabilities.

I'm checking how a stroke crossing only the corner of a pooled box compares with one passing through its centre, since with a single-tap max both should register the same. I'm weighing whether a binary presence feature is the right choice here, and how the template should be rendered to match it.

I'm settling on a clipped Gaussian rendering with σ around 2.6 for the templates, since presence saturates and parallel strokes shouldn't add past 1. But the features themselves have changed with the sharper cells, so the previous calibrations at θ=1.0 no longer apply, and I'm weighing whether to spend another probe or recalibrate from what I have.

I'm weighing whether the sharper binary cells let a pure template match work as a baseline before layering on the evidence items, since the earlier calibrations no longer hold. With only nine steps left, I'm thinking about whether to define the evidence directly on cells, using what the probes have shown about which digits lack the top and bottom strokes.

I'm weighing whether to drop the blur, since it smeared the G and K evidence. With sharp features, a right-column cell might separate 1 and 7 from 3 and 5, though the stroke positions I'm estimating are too rough to rely on. So I'm leaning toward a pure template match on the new features, adding only the evidence items that the probes have actually validated.

I'm weighing whether the sharper features, with less blur, actually help template matching, since the blur only drops from about 3.5 px to 2.9 px effective. I'm also wondering if keeping the old blurred features for the evidence items would be better, though the channel budget rules that out.

I'm weighing whether sharper features actually matter here, since shrinking the total blur from about 3.5 px to 2.3–2.9 px is only a modest change. Hand-drawn stroke jitter of around 2–3 px suggests a blur near 2.5 px is about right, so the gain may be small. The bigger limit is likely the linear template itself, which probably tops out around 70–75% on these prototypes, so going further would need better class statistics estimated from probes.

I'm now asking why the 2s get mistaken for 3s, since the 2s have a heavy base and a diagonal stroke that could look like the 3's curves. I'm checking how the bottom and diagonal strokes of a typical 2 line up against the template's expected cells.

Now I'm checking how the 2s and 3s differ at the lower-left and base: the 2 carries a diagonal through the centre that continues down-left and a base running right, while the 3 has a vertical near the lower-right and a tail on the lower-left.

I'm reasoning that sharper cells should separate 2 from 3: the lower-right vertical sits in the 3 but usually not the 2, while the lower-left diagonal shows up in the 2 and not the 3. That could help the template match on pairs like 2/3 and 7/9.

I'm deciding on the next step: keeping the new sharp binary features and using pure cosine templates at about σ 2.2, clipped at 1. I'm weighing whether to run a clean baseline with no evidence items, or add a few evidence items that are safe without known calibration, like vetoing the bottom stroke for 1, 7, 4, and 9, and the upper-left vertical region for 2, 3, and 7.

I'm weighing a Bernoulli naive Bayes classifier over the binary presence features, where each class gives every cell a presence probability and the absence terms also count against classes that expect many strokes. That form handles missing strokes properly, so I'm considering it as the principled option if the probabilities hold up.

I'm considering a Bernoulli naive Bayes classifier with floor and ceiling probabilities near 0.15 to avoid overconfidence, though the correlated overlapping features would overcount and need scaling down. The risk is that hand-estimated stroke positions would impose heavy penalties on absent or misplaced strokes, which a cosine template would handle more gently.

I'm weighing a softened Bernoulli version where each cell's presence probability is pulled toward the middle, so the log-odds weights stay bounded. The absence terms then penalize classes that expect ink where none is present, and I'd scale the total logit down because the features overlap and would otherwise overcount.

I'm weighing whether the naive Bayes form is more robust than the cosine template, since it penalises unexpected ink as well as missing ink. The worry is that my hand-estimated stroke positions would make those penalties too heavy, especially for variants like open or closed 4s, 7s with or without a crossbar, and 1s with a flag or base.

I'm checking whether a naive Bayes form beats the cosine template here: its absence and background terms would penalise classes that expect no ink where a stroke appears. The catch is that an unexpected stroke costs many features at once, so the effect depends on which classes expect that stroke. For a 7 with a crossbar, classes like 4, 5, 6, 9 and 3 expect ink there and avoid the penalty, which could add a sizeable swing against 7.

I'm weighing whether a Bernoulli naive Bayes form beats the cosine template here, since it would penalise unexpected ink as well as missing ink. One worry is that a stroke no class expects gets a heavy penalty against any class that predicts it, which could distort the vote, so I'd keep the probability floor fairly high to limit that effect.

I'm working out how the classifier's score comes from the binary features: each class contributes a weight per feature, plus a bias from the absence terms. I'm also questioning whether the rendered template values can be read as true presence probabilities, since the Gaussian falloff with distance from a stroke only roughly matches how often a stroke actually crosses a cell.

I'm checking how the Gaussian-rendered template values compare with the actual presence probabilities: at a distance of 2 px the rendering gives about .74 against a real .63, at 3 px .51 against .44, and near the stroke it says 1.0 where the real figure is about .82. So the rendering is a reasonable approximation everywhere except right at the centre.

I'm checking whether a floor of about 0.15 on the presence probability is the right choice, since it keeps the log-odds weights bounded at roughly ±1.7 and still penalises unexpected ink without overshooting. Then I'm working out how a short stroke through the cell contributes, starting from the integral of the Gaussian falloff over its length.

I'm settling on a scaling factor of about 0.1 for the naive Bayes logits, since the summed differences between classes run into the tens and the correlated features would otherwise overcount.

I'm weighing whether the naive Bayes form beats the cosine template here, since it uses absence information the cosine can't, though I'm unsure which is more robust. I'm leaning toward ε=0.2 for the softened probabilities, and I'm also considering the class bias term, since classes with lots of expected ink get more negative bias.

I'm checking the cell geometry for the banks: with a single tap, each cell's filter centre lands at 4i+2ca+3.5, so the box covers centres within about 1.5 pixels, and the stroke centre has to fall inside that box.

I'm settling the cell geometry for the banks: with a single tap, each cell's filter centre sits at 4i+2ca+3.5, with a half-width of about 2 to 2.5 px. I'll keep σ=2.6 for the Gaussian rendering, and write the conv channel as the stroke's presence value at the tap, with weight 1.

I'm settling the optional strokes: a variant prototype at half weight gives a probability near the middle, so its log-odds weight drops to roughly zero and the feature stays neutral where a class is uncertain. That lets me encode things like the 7's crossbar, the 4's closed top, the 2's loop, the 9's tail, and the 1's flag and base without penalising either way.

I'm adding optional strokes to the prototypes at lower weights: a flag and a base for the 1, a crossbar and a left tick for the 7, and I'm starting to sketch a closed top for the 4.

I'm adding optional strokes to the prototypes, such as a base curl on the 2, and I'm noting that the 5's upper-left vertical shows up in only about half the training examples, while the 4, 6, 8, and 9 are closer to 70–80%.

I'm settling on ε=0.2 for the softened probabilities, since the presence weights stay bounded at about ±1.39 that way. I'm also noting that the class bias term would make classes with lots of expected ink more negative.

I'm checking the bank geometry for the rendered templates and the conv2 taps, starting from the four bank pairs and how each one maps its channel onto the cell grid.

I'm checking the bank geometry for the conv2 taps and the rendered templates, with cell centres at 4i+2ca+3.5 and a clip at 1 per cell. Then I'm reconsidering the 4's prototype, since the nominal left stroke and bar may need adjusting.

I'm checking the 4's vertical and the 7's stem against typical digit shapes, and the 9's loop and tail, the 6's spine, the 5, and the 2's optional base curl all look reasonable as they stand.

Now I'm checking the zero's left and right edges: the x positions I used may sit a bit too far in, so I'm nudging them outward to match a typical zero's width.

I'm settling the scale factor α at 0.08, since the margins between the true class and the runner-up could be around 24 raw units and a larger value would make the wrong predictions too confident. The baseline term is the same for every class, so it drops out of the comparison.

I'm weighing the risk of the naive Bayes approach against the cosine fallback, and I'm fine with either outcome since I can still revert to the earlier configuration. I'm simplifying the conv2 layer to single taps, switching to the four bank pairs, and dropping the tip features from the templates while keeping the tuple format.
