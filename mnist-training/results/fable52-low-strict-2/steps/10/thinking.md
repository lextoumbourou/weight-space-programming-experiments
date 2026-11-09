I'm checking how the predicted counts respond to the bias shifts: the 2 bucket moved only from 1574 to 1363, and the 9 bucket from 587 to 711, so the sensitivity is lower than I expected. Getting 9 to its true 1009 would need a much larger bias change than the roughly linear estimate suggests.

I'm weighing whether step 7 or step 9 is the better base, and the per-class numbers are mixed: step 9 helps some classes and hurts others, like 8 and 9. Since the 9 template in step 9 matches poorly, I'm leaning toward step 7 as the base and keeping its confusers for 9 and 8, while I'm unsure whether the 2 variants or the emphasis caused the recall gain.

I'm working through the per-class differences from step 7: class 1 is over-predicted by about 163, while 4 is under by about 158, with smaller gaps for 2, 3, 5, and 6.

I'm adjusting the biases on step 7 by small amounts, mainly lowering class 1 and raising class 4, since 1 is over-predicted and 4 is under. I expect only a modest gain from this, perhaps around one percentage point, and I want one template change with decent evidence behind it as well.

I'm considering adding emphasis to classes 4 and 5, since their recall improved in the earlier runs with similar biases and unchanged confusers for 4. I'm also weighing a few extra confuser weights, like 5's confuser for 3 and 6's confuser for 5, and I'd keep step 7's confuser for 7. The 9 template still needs its own emphasis adjustment, which I haven't settled yet.

I'm settling on step 7 as the base for this round and not switching to step 9's 2 variants, since step 9's precision on class 2 isn't clearly better. I'll add emphasis for classes 4 and 5, plus a heavier subtraction from 5 in the 6 template, then apply the bias adjustments I worked out.
