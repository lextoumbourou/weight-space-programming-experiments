I'm weighing a few small tweaks: reverting x4/x9 to 0.7 or trying them at 0.6, and testing the step-32 setup with x5 dropped, which came out at 0.4851. The results are all hovering around 0.485, so the surface looks flat.

I'm now looking at whether the x10/x11 magnitude effects are really an interaction term, since a product would only show up weakly in the abs probes. Testing that properly would need more units than I have free, so I'm considering dropping the abs terms and using the spare capacity to implement |a+b| and |a-b| directly.

I'm working out the abs-term coefficients in terms of |a+b| and |a-b|, since their sum equals 2·max(|a|,|b|). That lets me set the coefficient on |a+b| to -0.2 + g/2 and on |a-b| to -0.2 - g/2. With g=0.5, that gives 0.05 and -0.45, and I can flip the sign of g later to compare.
