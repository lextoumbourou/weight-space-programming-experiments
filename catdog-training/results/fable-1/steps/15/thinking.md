I'm working out the coarse hit rates for cats and dogs, which gives a d' of about 0.28, and then setting up the loss equation in σ, which reduces to a quadratic in σ.

I'm solving the quadratic for σ to get about 0.060, which puts the optimal individual weight near 4.7 and the mean near 0.008. Across the three scales the d' values are 0.37, 0.32, and 0.28. Next I'm estimating how much combining them helps under moderate correlation, where the gain is modest.

I'm working through the combined-feature weights under two correlation assumptions, landing on roughly (3.3, 2.5, 1.7) for the three scales, with T and G held at 1.2 and 2.5. Next I'm setting the class centres and a small extra bias, and estimating the expected loss at about 0.650.
