The latest attempt scored worse: the 8 is over-predicted again, with the ink map giving it no penalty, and 9 also did worse, possibly from the loop weight or the ink term. Still, the ink channel's positive part seems to favor dense templates, though it's normalised, so I'm not sure that's the cause. The stubborn 0→6 error points to something systematic, and I'm wondering whether my geometric assumption is off, such as the cell offsets or a vertical flip.

I'm checking whether the index mapping and row-column offsets are correct, and they look right. The 0-versus-6 confusion might come from thick strokes weakening the bar responses, or from the 6 template's loop width happening to overlap a slanted 0.

I'm wondering whether real 0s often have a small gap or overshoot at the top, which would fire the end-detectors that the 0 template penalises and that the 6 template rewards.

I'm weighing whether to give the 0 template weak end marks at the top, since real 0s often have a small gap there that gets penalised. I'm also considering explicit ink-based discriminators for 0 versus 6 on the upper-right cells, though the ink penalty looks small relative to the logit scale.

I'm considering dropping the ink channel's positive part and keeping only a penalty, since the positive side is what rewards the 8. I'm thinking about a bias-plus-weight term for the missing-ink case instead, but I'll revert to the step-2 config and try targeted 5x5 detectors over the orientation and end maps at a larger scale.

I'm considering a bias term for the 0 template: a positive bias, paired with a negative weight on the central sharp-ink cells, so that an empty centre is rewarded. That could help against both the 0→6 and 0→8 confusions. The risk is that digits like 7, 1, 4, 2 and 3 pass near the centre too, so I'd need to check them.

I'm estimating the size of the bias B from the logit scale, with the centre-ink weight k set so that non-zero digits, which all have ink through the centre, get pushed well below zero. Next I'm turning to the 3-versus-5 confusion, looking for an upper-left vertical stroke paired with a top bar that extends to the right.

I'm working out sharp vertical-stroke detectors for telling 3 from 5: a stroke in the upper-left for 5, and one in the upper-right for 3, each with a negative weight on the other side.

I'm weighing a class bias for 8, pulling its score down since its dense template avoids penalties, and I'm thinking about the bias value without yet knowing the right scale.

I'm setting the 5 and 6 biases negative, the 9 bias positive, and small positive biases for 3 and 2. That's a rough fix, but it targets the over-predictions directly. I'm reverting to the earlier ink-free base and leaving the 9 loop weight alone for now, since I'm not sure it's the cause.

I'm working on the 3-versus-5 split now, planning a sharp vertical-stroke channel and checking where the 5's left vertical falls in pixel terms.

I'm working out sharp vertical-stroke weights to separate 3 from 5: a left-side vertical in the upper cells favours 5, while a right-side one favours 3, with the opposite sides penalised.

I'm setting the 3-versus-5 weights on the sharp vertical channel: positive for 5 on the upper-left verticals and negative on the upper-right, with the reverse for 3. For 9 versus 5 and 7 versus 5 the same channel should give the right separation.

Now I'm adding sharp vertical-stroke weights to separate 9 from 6 and 9 from 7, plus the upper-right vertical for 9 against 6. Next I'm turning to 2 versus 3, looking at lower-right vertical strokes.

Still writing the weight table for the sharp vertical channel...

Still writing the sharp vertical weight table for the 5, 3, 9, 6, 7 and 2 templates...

Still writing the sharp vertical weight table, now with the per-class entries for 0, 4 and 7 and the small top-end allowances for the 0 template.
