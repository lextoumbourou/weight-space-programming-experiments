The 2-digit results are in: the loop variant leads at 265, about 27%, with the narrow upright next at 218, around 22%. The wider form and the round-top come in lower at 116 and 89, and the base form is the least common at 42. Still, the spread is pretty wide, and I'm wondering whether the narrow upright is also mostly the loop form.

Narrow-upright and loop variants both do well for the 2s, which hints that the 0.2 shear may be too strong for them. For the 3s, the M shape with the long middle bar is clearly the most common at 42%, with the wider and narrow-upright forms tied at 22%. Since the M form dominates, I'm considering building the mixture around M-based variants, but I'm wary of spending too many steps on these tournaments with the remaining digits.

Next I'm thinking about switching to a mixture of templates across all the digits instead of running separate tournaments, using a few shear and width combinations with weights. I'd test that in a real classification step, and only run tournaments for the digits where confusion still shows up.

I'm assigning weights to the zero variants, keeping the skewed-width version fixed, and giving the shear a bit of spread. For the 1s I'm listing slant angles with their shares, mostly upright and slightly tilted.

I'm settling the remaining digits with a generic three-way mixture over slant and width: a narrow upright form at 0.35, a base form at 0.25, and a wide slanted form at 0.4. The base form has been the least popular for both the 2s and the 3s, so I'm giving it the smallest weight.

Now I'm weighing whether to drop the separate digit tournaments and instead build each digit's template as a weighted mixture over a few shear and width combinations. For the digits I haven't tested yet, I'll use a narrow-upright, base, and wide-slanted mix, and I'll give the base form the smallest weight since it has lost in both the 2s and the 3s. The built-in slant on the 4s and 7s means their extra shear values should be milder.

I'm setting the bias adjustments back to zero to see the baseline, and I expect the 0, 2, and 3 digits to improve. I'm also wondering whether the blurrier mixture marginals will need a higher temperature, so I'll keep the setting at 0.2 and check the results.

Still writing the template functions...

Still writing the mixture weights for the 2s and 3s...

Still working out the mixture weights for the remaining digits.
