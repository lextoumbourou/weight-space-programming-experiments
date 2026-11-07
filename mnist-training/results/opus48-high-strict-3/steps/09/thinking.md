Accuracy fell from 41.6% to 35.3% after the template changes. The biggest damage is to recall for 0s, which dropped from 707 to 232, and I suspect the center-hole penalty is the cause, since real MNIST 0s often have ink in the middle after downsampling. Recall for 2s also crashed, from 565 to 156.

I'm reverting the templates for 0, 1, and 2 to the original step 7 versions, since their recall losses outweigh the gains. For 4, I'd like to keep a gentler version of the top-left change, because it fixed 9→4 but cost too much 4 recall.

I'm going to drop the template changes altogether and go back to the original set, since those gave the best accuracy. Rather than tuning templates further, I'll look at the bias for the 9→4 confusion, using column totals from the step 7 run.

I'm going to revert to the original templates and pair them with the balanced bias b8, which should recover around 42%. After that, I'll use the remaining steps to make careful single changes rather than sweeping ones.

I'm dropping the templates I'd been testing and going back to the original set, since the balanced bias should bring accuracy back to around 42%. The 9→4 confusion is tricky: lowering the 4 bias could push those cases to 8 instead, so I'd rather recover the clean baseline first and see the confusion pattern clearly. Next I'm restoring the original template for 1, which had the flag stroke.

Restoring the original step 7 templates for the digit shapes, and pairing them with the balanced bias b8 I worked out from the step 7 column totals.

I'm going back to the original step 7 templates and pairing them with the balanced bias b8, aiming to recover about 42% before making any further single changes.
