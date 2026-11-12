I'm weighing a small further tweak: whether to fine-tune the temperature or raise lambda to 2.8. I'm working through the rescaling for that change, with the factor of about 1.118 applied to the gscale and hs values, and I'm starting to recount the step-47 counts for the first rows.

I'm recomputing the per-row slopes for the next set of rows, applying the same slope of 40. The step-47 recount barely moved the counts, which suggests the lambda increase is offsetting the other changes, so the slope is hard to pin down. The values come out mixed in sign: rows 1 and 6 are negative, while the rest are positive.

Rows 8 and 9 come out negative, and I'm settling on lambda 2.8 as the next step.
