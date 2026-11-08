I'm going to build a logistic-style model where two ReLU units split the linear score z into positive and negative parts, so their difference reproduces z exactly. I'm also considering adding interaction units on top of that.

I'm now working out the coefficients for the Titanic model: a roughly +2.6 boost for female, penalties for second and third class, and a small negative weight on age. I'm also adding terms for unknown age and cabin, and setting the intercept so a male first-class passenger aged 30 lands near the observed survival rate.

I'm working out the intercept and the age terms: an unknown age gets a penalty of -1.2, which I'm offsetting with an age-known term, and I'm checking whether the total for a 30-year-old male first-class passenger still comes out to the -0.5 I aimed for.

I'm checking the age term: it works out to -0.4 per year relative to 30, with an unknown age contributing nothing, so a male first-class passenger still lands at -0.5. Females in third class come out near 0.5, but males in third class fall too low, since their observed survival is closer to 0.14. That points me toward separate hidden units for the female-by-class combinations rather than one shared term.

I'm adding a child-age unit, and I need to make sure it doesn't fire for passengers whose age is unknown.

Still working through the age term, and I'm weighing a rectified child-age unit that only switches on when age is known, so unknown-age passengers don't get the boost. I'm also trimming the age and sibling coefficients, with the family-size penalties kept as separate small negative weights.

Still wiring the output weights: one unit gets +1 and the other -1, and the rest stay at zero.
