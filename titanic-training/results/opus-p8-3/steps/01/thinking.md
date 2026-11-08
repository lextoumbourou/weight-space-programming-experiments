I'm sketching a first step: a logistic-regression-style model where hidden units act as linear pass-throughs via ReLU on positive quantities, with some interaction terms added. I'm also recalling rough Titanic coefficients for reference, such as a large positive effect for female, negative effects for lower passenger classes, and a small negative effect for age.

I'm working out the score for each passenger: a baseline with a +0.5 intercept, a large boost for being female, and penalties by passenger class. Female third-class passengers come out too high under that plain sum, so I'm adding an interaction term to pull them down, and I'm also adding an age adjustment around age 30.

I'm now setting up the score as a sum of terms: a base value, a bonus for female passengers, penalties by class, and an age term, with an extra adjustment for passengers whose age is unknown.

I'm adjusting the intercept so a male first-class adult at age 35 with a cabin and a higher fare lands near the target score, which puts the baseline around -0.1. Then I'm checking a male third-class passenger aged 25 with a low fare and embarkation at S, which comes out near -1.

I'm now checking a male second-class adult at age 30, which lands around 29% under the current terms, well above the roughly 8% observed. I'm adding a male-by-second-class penalty to pull that down, and I'm looking at how child passengers offset it.

I'm checking the female third-class case: with the plain sum it lands around 0.75, too high against the roughly 50% observed, so I'm subtracting an interaction penalty to bring it near 54%. I'm also noting that large families in third class do worse, which the sibling term partly covers.

Now I'm working through the female first-class case, which comes out around 96%, and then wiring the model up with two ReLU units that split the score into positive and negative parts. I'm adding a penalty unit for female third-class passengers, one for second-class men, and a child unit whose effect shrinks as age rises.

Looking at the remaining setup, I'm settling on the hidden units: all others stay at zero, so I just need to write the code.
