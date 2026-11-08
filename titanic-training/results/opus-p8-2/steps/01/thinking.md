I'm planning the first step with a logistic-style model built from ReLU hidden units. One option is a single unit carrying a linear score, shifted by a bias offset so it stays positive, with the second layer subtracting the offset back out. Another is a pair of units, one for the positive part and one for the negated part, whose difference gives the exact linear logit. I also want a few interaction units, such as female-and-third-class and male-child.

I'm working out the survival score with coefficients for sex, class, and age, and I'm handling unknown ages by giving them a fixed penalty. I'm also planning a hidden unit for women in third class and another for young boys.

I'm setting the baseline so a male in first class lands near even odds, and I'm trying intercept -1.0 with pclass1 at +0.6 and pclass2 at -0.6 to see whether male second class comes out close to the observed rate.

I'm checking the female third-class score next, with the intercept at -1.0 and the male and female baselines worked out, and I'm weighing whether the female first-class result needs a higher value.

I'm settling the remaining weights: cabin and embarked-C get small positive values, parch and sibsp small negatives. For boys I'm adding a bonus unit, though age alone already lifts young children by about one, so the total for a three-year-old in third class still comes out positive.

Still refining the boy weight against the sibsp penalty for third-class families.
