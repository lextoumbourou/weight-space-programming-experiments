I'm concluding that the modest improvement means the features themselves need work, not just tuning. The current max pooling over wide regions likely blurs spatial detail, so I'm considering whether that's what limits the templates.

I'm checking the example errors against the templates, like 1 → 7 where slanted 1s share the diagonal of a 7. I'm also weighing a few ways to improve the features: more orientation channels, signed edge or curvature features, or a likelihood-style classifier in place of cosine matching.

I'm weighing whether more prototypes per class could help, but a linear layer can't OR them together, and conv2 units only see about 13 pixels of the input, so they can't act as whole-digit prototypes. I'm also considering whether my drawn digits match the real MNIST size distribution, since most digits fill a 20-pixel-tall box, and the mean-subtracted class weights are probably fine for separating confusable pairs.

I'm now weighing a different representation: a finer 8x8 grid built from conv2's orientation channels, with narrower templates. That gives more detail but also more sensitivity to variation, so it isn't clearly better. I'm also checking which features would separate the main confusions, like 1 versus 7, where a slanted 1 shares the diagonal of a 7 and the template would need a "/" component.

I'm weighing whether to build several templates per class from varied drawings, since a single slanted-1 template can't be OR'd with a vertical one through linear weights. The 1-versus-7 confusion is the sharpest case, so I'm thinking about giving 1 a slanted component and strengthening 7's top bar. I'm also checking whether averaging over generated samples to set the weights would break the rules I'm working under.

I'm considering building the templates from a few hand-drawn stroke variants, weighting each stroke, rather than generating synthetic examples. I'm also thinking about extra orientation channels from conv1 to give the features finer direction detail, similar to what HOG-style descriptors use.

I'm looking at the confusion counts now: the errors into 8 (2→8, 5→8, 9→8) and into 7 (9→7, 1→7) are the largest. Column totals show 8 absorbing about 1,984 predictions against roughly 1,016 for 7, so the bias I raised on 8 last step seems to be pushing too many digits into it, and I'll need to rebalance it.

I'm weighing a lateral-inhibition idea for conv2, where each orientation channel gets reduced by a share of the overall stroke intensity, so the features reflect relative orientation rather than raw ink amount. That could make the templates less sensitive to how heavily a digit is drawn, though I'm not yet sure it would be a clear gain. I'm also starting to consider an LDA-style alternative, where the weights come from the inverse covariance of the features rather than from hand-drawn templates.

I'm thinking about whether whitening can be approximated by sharpening the templates: subtract a neighbor-averaged version of each centered template, since neighboring features are positively correlated. I'm planning to apply that decorrelation with a factor of 0.5, and I'm also noting that the intensity channel will end up with less weight because it tracks the orientation sum.

I'm thinking about whether a more realistic set of MNIST-style prototype drawings would help more than tweaking the math. My sense is the digits should match the typical size and placement, like 0 as a slightly tilted oval about 14 pixels wide and 1 as a line slanted roughly 12 degrees.

I'm now going through the stroke layout for 7 and 9: 7 has a horizontal top bar and a steep diagonal, while 9 adds a loop on the left and a bottom horizontal near row 13. That loop is what separates them, since 7 has only the top bar, so the 7 template's diagonal may be too shallow compared with real 7s.

I'm looking at the feature-template setup now, and whether the 1 and 7 templates can be sharpened, so the weights reflect what separates the digits rather than their overlap. I'm considering a decorrelation step on the templates, plus a slanted stroke for 1, and I'll keep the bias adjustment at half strength since changing the templates shifts what the old bias was correcting.

I'm making each class's weights zero-sum across features as well, so a thick-inked digit doesn't get a free boost. That should stop the heavy-coverage templates, especially 8's, from pulling in thick digits.

I'm going to double-center each class's weights so that a thick-inked digit doesn't get a free boost, and I'm dropping the bias back to zero since that changes the picture. I'm also adding a second, weighted stroke to the 1 template to give it the slant.

Still writing the 1 template with its two weighted strokes...
