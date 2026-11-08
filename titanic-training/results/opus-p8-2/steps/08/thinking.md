The scale at 1.15 came out slightly worse, so the calibration looks about right and I'll keep it at 1.0. Next I'm looking at male first-class passengers: the current model puts a 40-year-old there at 0.45, while the actual survival rate is 0.37, though younger first-class men seem to do better. I'm considering a stronger age effect for adult men, or adding a fare term on the log scale, since fare tracks class closely.

Checking whether a missing-age penalty can be fixed by adjusting the age coefficient and intercept together, so known-age results stay the same while the missing case moves.
