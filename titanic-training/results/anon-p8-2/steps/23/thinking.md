I'm weighing whether to try -0.3 for unit 2, since going from 0 to -0.5 only gave a tiny gain and the female third cell looks borderline. I'm leaning toward keeping -0.5 and checking whether the remaining improvement lies in tuning other features like x1, x9, and x5, along with age.

I'm now trying to match the one-hot features to columns: x7 looks like Pclass_2 given its 20% share and 46% survival, and I'm checking Embarked_Q against x8 or x11 based on row counts.

I'm checking the remaining features against the survival rates: x6 seems mostly binary with a weak positive correlation, and I'm now testing x3 as SibSp, since its heavy tail fits a count of siblings and spouses.

I'm working out which features might be Parch and Age, using the rows above 0.95 and their survival rates to match them. Fare doesn't fit the 19% share with a simple threshold, so I'm considering whether it's been log-transformed.

I'm guessing that Age is x12, so I'm planning a child unit that responds to very young ages, with the weight set to +1.0. I'll test it and also check whether a large SibSp value pushes survival down further.
