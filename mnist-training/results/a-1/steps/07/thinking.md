The first run of tests came in a bit better, with 8 now mostly reading as 7 and 9. I'm wondering whether the templates themselves are the problem, since their positional spread may not match the spread of the real feature maps.

I'm now going to check whether the templates were the problem, since their shape may not match the MNIST digit size and position. I'm considering a slant or shear for the digits, because handwritten digits tend to lean to the right.

I'm building the templates as a mean over several shears, so each digit tolerates a range of slants. For the 1 and the 7, I'm starting from upright versions and then applying the same shears.

I'm now writing the shear step: applying 0 to 0.4 shears to the upright drawings and averaging them, with the 7 drawn as a bar and a stem.

Still working out the shear, which keeps the sign and offset of the column change tied to the row distance.
