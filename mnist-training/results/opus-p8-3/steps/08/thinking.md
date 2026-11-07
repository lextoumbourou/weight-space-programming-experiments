I'm finding little change in the HB/VB response and am unsure those detectors fire at all. The nearest-template approach sits around 67%, so I'm wondering whether there's a systematic flaw, perhaps in the conv1 orientation filters, whose zero-mean Mexican hat at s=1.5 on a 5x5 grid may not suit thick MNIST strokes.

Checking whether the orientation filters hold up on thick strokes: a horizontal filter gives about 0.49 response on a 4-px stroke against 1.0 for a centered 3-px one, so that part seems fine. The diagonal detectors may only partly respond to horizontal strokes, which is also probably acceptable.

I'm considering normalizing each class template to unit length and using a cosine-style score, with a single temperature scaling the logits, and per-class bias tweaks to fix the attractor classes like 3 and 8.

I'm weighing whether cosine normalization would help, since broad averaged templates like the one for 8 might be pulling in dense digits, and I'm not sure the normalization changes that much. Dividing by the template norm penalizes wide templates like 8 in a way that nearest-mean with its norm penalty also does. I'm leaning toward trying coordinate descent over a few scalar hyperparameters, since I can't inspect the data directly and the template quality itself seems to set the ceiling.

I'm wondering whether the nearest-template ceiling reflects a flaw in my templates rather than the features themselves. Typical nearest-mean accuracy on raw MNIST pixels is around 82%, and with orientation-pooled features I'd expect somewhat better, so the roughly 20-point gap may come from how far my templates sit from the true class means. Without the data I can't measure that gap directly, so I'll need to revisit my rendering assumptions for anything systematically off.

I'm now checking whether the ink-presence features are doing any real work, since they're nearly always on in the central cells and may not separate digits at all. I'm also wondering whether the orientation features, which are pooled and saturate easily, lose the distinctions between classes that matter.

I'm weighing whether features that are present in the input but absent from a class template can act as negative evidence, and whether per-feature weights based on how much the templates differ would do better than treating every feature equally.

I'm treating the shared-feature penalty as consistent with nearest-mean, then wondering whether heteroscedastic classes, like tight 1s against broad 8s and 2s, need class-specific variance terms that act as biases. I'm leaning toward handling that through the bias tuning and refining templates against the main confusions.

I'm comparing which features separate a 2 from an 8 and from a 3, especially the bottom bar and the diagonal strokes, and checking whether the 8 template's side loops are working against it.

I'm wondering whether the 2 template is simply mismatched to real 2s, since many have a bottom-left loop and a curved diagonal that might read as 8-like. The 1 class is performing well at 1002 of 1064, while 2, 5 and 8 are the weakest, so I'll look more closely at those.

I'm tracing how input coordinates map through the conv and pooling layers to the final grid cells, checking a sample of rows to see where the boundaries fall.

I'm checking how the grid cells line up with the digit's extent: centers at rows 6 through 21 are covered, but the strokes at rows 22-23 barely reach the last cell and the ones at rows 4-5 only weakly reach the first, which could be a real source of error for digits like 2.

I'm considering widening conv2's receptive field so each final cell spans more rows, which would let strokes near the top and bottom edges register instead of falling between cells. I'm also weighing whether summing overlapping taps would inflate responses on aligned strokes, and whether center-weighted taps might avoid that.

I'm considering spreading conv2's taps over a 3x3 block with equal weights, so a stroke passing through registers across several taps. That would let each final cell cover a wider band of rows, roughly the input rows 4 through 11 for the first cell, which might catch the top and bottom strokes that currently fall between cells.

I'm settling on a 3x3 Gaussian-style weighting for conv2, with the center tap at full weight and the edges at half and quarter, so a stroke through the center registers fully and one on a neighboring row still registers at about half. That should extend each final cell's coverage to roughly input rows 4 through 11 for the first cell, which would catch the top and bottom strokes that currently fall between cells. I still need to update the template coverage to match.

I'm now defining the coverage function for each cell: full weight for stroke centers in the core rows, half weight for the neighboring rows, falling off beyond that. I suspect the bottom bar of the 2s, which sits near row 22, is being underweighted, and the top bars of 5s and 7s near rows 4-5 may be too.

I'm applying the same 3x3 weighted blur to the second convolution, so each final cell picks up strokes near the top and bottom edges. The template coverage needs updating to match, and the rest of the pipeline stays as it is.
