Step 9 pushed accuracy up to 37.2% with loss at 1.84, and six steps remain. I'm keeping the energy-equalised approach and turning to the sink problem, where the output is collapsing onto the digit 6.

I'm comparing per-class prediction counts and see that 9 and 0 are almost never predicted, while 6 and 3 absorb too many images. I'm considering a moderate bias adjustment, boosting 0 and 9 and lowering 6 and 3, though the logit scale is sensitive, so I'll keep the changes small.

I'm settling on small hand offsets to the class logits, nudging 0, 9 and 7 up and 6 and 3 down, but the logit scale is unclear, so I need to estimate how large those shifts actually are.

I'm applying a set of small per-class logit offsets, raising 0, 9 and 7 and lowering 3 and 6, with 9 being the most underpredicted class. I'm estimating the logit spread at around 3 to 4, so these shifts are roughly a tenth of it and should stay modest. I'm also wondering whether 9's template needs to differ more from the others, since its errors scatter toward 8, 3, 4 and 6.

I'm weighing a few small bias changes: nudging 9 and 0 up, 3 and 6 down, and keeping the adjustments modest. The 9 shift risks pulling predictions away from 4 and 7, but I'll accept that and keep the same framework.
