My first bias correction for 8 overshot, and now 8 is a huge sink at 2976. The calibration keeps oscillating because the template changes interact, and 3 has collapsed to 83.

Those 8 overshoots came from the bias and alpha changes together. The alpha updates pushed down the logits for 2, 3 and 5 on 8-like images, but the compensation only holds on average, so the 3 template got heavily negative and real 3s lost out. I over-engineered it, so I'm going back to step 3 as the base and making only modest changes.

I'm thinking about making the representation more robust, perhaps with coarser features, since the confusions are between plausible pairs. Nearest-centroid with accurate centroids could reach around 80%, and my current templates are off. I'm recalling typical MNIST class shapes, like the fat ring for 0 and the vertical bar for 1, to get the templates closer.

I'm sketching the digit templates by hand from memory: a fat ring for 0, a vertical bar for 1, a bar with a diagonal for 7, a loop with a stem for 9, and so on. The bigger problem is that my 8x8 grid cuts off the top two rows, which drops ink from 2, 5 and 7 and removes some of what separates them.

I'm weighing whether a shifted window helps: taps at (1,2) would cover rows 4 to 21, but the digits span roughly rows 4 to 23, so either choice drops two rows. Pooling tricks in conv2 stay linear, so they can't squeeze more rows into the same 8 cells.

I'm checking how the pooling could cover more rows: two channels with different row offsets would together span all twelve rows of the first pooled map, at the cost of some duplicated coverage.

I'm weighing whether 8x8 at 2px over the central region beats a 6x6 layout at 4px with full coverage, and I lean toward keeping the 8x8. Shifting the crop either way drops two rows, so the choice is roughly a wash, and I'll keep the current window.

Reverting to the step 3 setup and looking at its confusion matrix: 3 gets pulled into 5 heavily, 8 scatters into 2, 3 and 5, and 9 leaks into 4.

I'm checking the 3↔5 confusion in both directions, which points to the templates themselves rather than bias. The 5 template has its upper bar and left vertical, while the 3 template's upper part sits on the right, so those should separate at 8x8. I'm wondering why real 5s still land on 3, and what the drawing of those digits is doing to the upper half.

I'm wondering whether my 5 template's bowl is too large, since that could be pulling real 5s toward 3. Looking at the numbers again, 8 barely gets classified correctly (127 right), and its bias jumped from −0.6 to +0.75 along with the alpha changes, which may explain the surge in 8 predictions. The logits also look quite flat, so small bias shifts have an outsized effect, and I'm considering a higher scale to sharpen them.

I'm weighing whether the 9→4 confusion means my 9 template is off from real 9s, probably a loop that's too large or a stem that sits too central. Scaling the calibration steps down to about 0.3 times the log ratio should keep the flat logits from swinging too far.

I'm wondering whether my 9 template's loop is too small, since real 9s may have a wider loop and a stem that curves left at the bottom. For 4, the template's right stroke might be too long compared with real 4s, which often have a shorter top. I'm also considering pooling ink into larger regions in some channels for a coarser, more robust signal, though the linear layer can't take on extra features.

I'm weighing whether the template normalization is distorting things: dividing by 0.55 times the max ink value means a double-density crossing point like the waist of an 8 shrinks the rest of that template's strokes, so I'm considering whether to normalize differently.

I'm checking whether the 8 template is the problem: two stacked ellipses at 0.48 and 0.58 of the height, which seems close to what real 8s look like. That makes the 8 errors harder to explain by shape alone, so I'll look at the bias and alpha effects again.

I'm weighing whether the 8 surge is from its bias moving to +0.75 along with the alpha changes, since at step 2 it was already a sink without them. The 8 template may need better shape, so I'll revert to the step 3 templates and biases, drop the alphas, and apply only a gentle bias calibration from step 3's counts.

I'm recalculating the bias corrections from step 3's counts with a 0.35 step, which pushes 8 and 9 up slightly and pulls 3, 4 and 5 down. Then I'm nudging the 9 template toward a bigger loop, with the stem running from the upper right down toward the lower middle.

Next I'm tuning the 9 template's stem as a polyline and reviewing the 6 and 5 shapes, which look fine as they are. I'll also consider whether raising the scale would help, but with the logits this flat I'm leaning toward leaving it alone.

I'm weighing whether the orientation filters help or hurt, and a quick test would be to zero their scale and compare. I suspect the negative side lobes pick up the soft antialiased edges of the strokes and weaken the responses.

I'm turning over whether the orientation maps help, since the ink maps are inherently fat after max-pooling and can't be sharpened by a smaller filter. The orientation channels might be where the stroke detail comes from, so I'm weighing whether they add signal or just noise.

I'm weighing whether the 9 template's stem and loop need changing, and whether the 4 template's strokes are too long. A structural change to the classifier won't help, since the linear layer still only sees the same features, so the gains have to come from better templates. Having no data to check against, I'll make small, interpretable adjustments at each step, starting with a note that averaging a few hand-drawn style variants per class could make the templates more representative.

I'm weighing whether the 5 template's left vertical and top bar are placed correctly, since real 5s land on 3 too often. The 3↔5 confusion looks tied to the 5 template's shape and bias together, so I'm checking the 5 geometry against how real 5s are drawn.

I'm checking the 5 template's bowl geometry, where the middle stroke sits around y 0.44 to 0.52, which looks close to where real 5s place it. I'm also weighing how the 3's middle at 0.5 overlaps with that, since the two classes share that region.

I'm looking at the 5 and 3 confusion now: the 5 template has a left vertical that 3 lacks, but with the blur the gap is small, so the bias term is doing much of the work. The 6-to-5 errors are the other side of it, since 6 shares 5's left stroke and bowl and differs mainly in where its top stroke ends.

I'm now checking the 6 template's top stroke: my polyline puts it too far right at mid-height, while real 6s curve in toward a left side closer to x≈0.25 by y≈0.3. That shift could help separate 6 from 5 without touching the bias terms.

I'm changing the 6 template's top stroke so it curves in closer to the left side, and making the loop a bit wider on the left. I'm also lowering the 4 bias, since 4 is being over-predicted overall, and I'll go back to the step 3 templates and add gentle calibration with the 6 fix and the bigger 9 loop.
