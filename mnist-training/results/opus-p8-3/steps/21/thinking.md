I'm working through the slot encoding, checking which combinations of the F flags map to each slot value. I've confirmed slot 1 and slot 3 come out to zero counts, and I'm now looking at slots 2, 4, and 5, with slot 6 still in progress.

I'm tallying the per-class counts for each flag combination, and the loop-top rates look high for class 3, around 25%, while class 0 sits near 7%. The numbers are noisy enough that I'm still working out what they say about LOOP_s.

I'm now weighing the LOOP_s and HB_s top presence rates by class, noting that 3s show a high loop-top rate while 9 is only moderately separated from 7. I'm planning to use these per-half fractions as the basis for the row templates, though I still need to reconcile them with the per-cell argmax counts I used before.

I'm weighing whether more probes for stroke features are worth the remaining steps, since the stroke templates may be the biggest source of error. A feature-by-feature binary probe would be too slow, so I'm considering aggregated groups or a scalar threshold sweep instead, and I'm not yet sure which will give more information per step.

I'm picturing the 7-versus-9 confusion as needing a single direction that splits them, with a scalar score whose per-class histogram would show where a threshold falls. Rather than searching for that direction by hand, I'll keep the template approach and add the new LOOP_s and HB_s data into the next classifier, then judge the stroke adjustments by full classification accuracy and calibrate the threshold at the end.

I'm thinking about turning the topology features into near-binary inputs by scaling the conv2 weights up, so a Naive Bayes classifier over the per-half presence rates becomes principled. That would let the measured probabilities feed directly into the weights rather than relying on hand-built templates.

I'm now considering a naive Bayes score over the per-half presence features, converting each measured firing fraction into a log-odds weight scaled by a typical activation magnitude. That would sit alongside the template correlation score, weighted by a tunable factor, so the probabilistic part has a meaningful scale.

I'm setting up the naive Bayes features next, starting with the loop and bowl presence rates for the top and bottom halves, then the cavity counts and the per-row loop measurements.

I'm weighing a naive Bayes term over the topology presence rates, with a damping factor since the features aren't independent, and keeping the stroke templates on the first five channels with a sharper scale.

I'm estimating each class's presence probability from the counts with a small smoothing bump, since the argmax counts undercount features that fire alongside others. Then I'll set the correlation weight to 4 and the naive Bayes weight to 0.6.
