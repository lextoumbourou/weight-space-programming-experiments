Training is at 70.5% with loss at 0.953. The new detectors look worth probing, so I'm considering a probe of the LOOP_s rows and the OPEN_L/OPEN_R features.

I'm weighing which probe design would actually show which detectors are present, not just which one wins the argmax. A per-class staircase is too inefficient, and a probe built around each slot's feature sum is only a partial fix, so I'm leaning toward targeting the known confusions instead, mainly the 6 to 0 and 6 to 5 cases.

I'm settling on a probe that reads the LOOP_s rows and the LOOP_l rows, with the first eight slots covering those rows and one slot left as the none option, since the LOOP family is what separates these classes.
