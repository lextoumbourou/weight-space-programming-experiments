# What Astra inspected before guessing Enduro

This is an excerpt of the observable tool trace and final answer from the blind run, not an internal chain-of-thought transcript. Astra used `xhigh` and made 24 tensor-reader calls. It received anonymous tensors, no candidate games, no action labels, no code, and no screenshots or model executions.

## The sequence in the log

| Reader call | Actual request | What was returned |
|---|---|---|
| 1 | `catalog()` | Eight anonymous tensor shapes, including a 9-by-256 output matrix called `t007`. |
| 2 | `statistics(ids=[...])` | Descriptive statistics for all eight tensors. |
| 3 | `axis_statistics(id="t001", axis=3)` | Statistics and relationships between first-convolution input channels. |
| 7 | `axis_statistics(id="t007", axis=1)` | Statistics across the output weights of each hidden unit. |
| 10 | `values(id="t007", index=[null,90])` | The nine output coefficients for hidden unit 90. |
| 16 | `values(id="t007", index=[null,87])` | The nine output coefficients for hidden unit 87. |
| 23 | `values(id="t007", index=[null,19])` | The nine output coefficients for hidden unit 19. |

These are selected steps from the full log, not a claim that they were its only inspections. [All 24 requests and outputs, plus the final answer](enduro-inspection-trace.json).

## What it reported

Its final guess was **Enduro**, explicitly marked speculative, with confidence **0.60**.

Astra's final explanation:

> Using zero-based indices, t007 column 90 strongly penalizes output rows {3,6,8}: {-1.202,-0.734,-0.951}, versus {0.045,0.016,0.032} for {2,5,7}. Column 87 reverses this pattern. These learned coefficients suggest opposing control groups.

It then related another column to its prior knowledge of the Enduro action ordering:

> In t007 column 19, rows {4,5,6} have coefficients {0.049,-0.035,0.006}; every other row is negative, between -0.335 and -0.117. Under standard Enduro ALE ordering, {4,5,6} are DOWN/DOWNRIGHT/DOWNLEFT, consistent with a braking-related distinction. Hidden-unit semantics remain unverified.

## What we checked afterwards

The quoted coefficients match the checkpoint. Under the [official Enduro action order](https://ale.farama.org/environments/enduro/), rows 3/6/8 are LEFT/DOWNLEFT/LEFTFIRE, while rows 2/5/7 are RIGHT/DOWNRIGHT/RIGHTFIRE. The [Beam Rider action order](https://ale.farama.org/environments/beam_rider/) differs even though both networks have nine outputs.

The source model applies ReLU to the last hidden layer, then a linear output layer. Conditional on a hidden unit activating, its negative output coefficients lower the corresponding Q-values. We did not observe its activations, test an intervention, or establish that any unit detects braking, a car, or a particular scene.

The action labels in the figure were added after the blind run. The figure shows exactly the numerical columns Astra requested, with their original output-row order retained.

![Output weights for three hidden units inspected in the Enduro checkpoint, with action labels added after the blind run.](enduro-output-weights.png)

*Output weights requested during the blind Enduro run. Action labels were added afterwards using the conventional ALE mapping. Coefficients show how an active unit contributes to output scores; the experiment did not measure activations.*

## The control that matters

The shape-only run guessed **Beam Rider** for this Enduro checkpoint. The numerical run guessed **Enduro**. Across the three games, shape-only top guesses scored 2/3 and numerical-weight top guesses scored 3/3. This is one run per game and condition, with action-count clues and no independent training seeds, so it is a promising example rather than a general accuracy estimate.

## Downloadable material

- [Figure, SVG](enduro-output-weights.svg)
- [Figure, PNG](enduro-output-weights.png)
- [Exact plotted coefficients](enduro-output-weights.json)
- [Complete sanitized inspection trace](enduro-inspection-trace.json)
- [Plot source](plot-enduro-output-weights.py)
