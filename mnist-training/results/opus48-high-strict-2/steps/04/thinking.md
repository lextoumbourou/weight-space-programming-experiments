Accuracy has dropped to 21% and the loss went up. The "1" over-prediction is back, so now nearly everything gets predicted as 1, and I'm wondering whether the normalization let the "1" template win again. Looking at the counts, "1" soaks up most of the other digits.

The "1" template keeps winning, so I think the normalization is the cause: the unit-norm templates let whichever one concentrates weight in the center, and "1" does that. Since the center-heavy feature maps favor it, I'm now looking at why the vertical detector scores "1" so high across digits.

I'm going to drop the raw ink approach, since the center-heavy blur means position weighting can't be trusted. Instead I'll lean on the ratio of total vertical to total horizontal response, plus the overall shape from the periphery.

I'm going back toward the step 2 design, since its scalar vertical and horizontal preferences got the best accuracy, and I want to normalize only the spatial ink template so the dense templates stop dominating. I'll also adjust the scalar weights to pull 5 and 6 back and give 0, 2, and 7 a better chance.

I'm going to drop the explicit subtraction idea for now and just downweight the center cells in the templates, since they hold little information that separates the digits. Peripheral cells are where the differences should show up, so I'll give those more weight.

I'm going to build each template as its ink pattern minus the average ink pattern across all ten digits, so the shared center-heavy baseline cancels out. After normalizing those deviations, the dot product with the feature map should reward whichever digit departs from the typical shape in the same direction, and I'll apply the same subtraction to the vertical and horizontal templates separately.

I'm going to subtract each feature's mean template across the ten digits before normalizing, so the shared center-heavy baseline cancels out. I'll keep ink as the primary template and give the vertical and horizontal ones a smaller weight, since I'm not sure their magnitudes are comparable.

I'm planning a fourth version: the ink template gets mean-subtracted across digits and normalized, while the vertical and horizontal preferences are applied as scalars with their own means removed.

I'm going to subtract the mean ink grid across all ten digits from each digit's ink grid, then normalize the result, so the shared center-heavy baseline cancels out. The vertical and horizontal preferences will get the same mean-removal treatment as scalars, since the step 2 version handled them without the 1 over-prediction.

I'm going to pick conservative gains here, Gi=12 and Gv=Gh=5, and leave the bias at zero for now and tune it later from the confusion counts. I'm also checking whether mean-subtracted ink templates rank the digits correctly, since the common-baseline term should cancel out of the comparison.

I'm checking whether subtracting the mean ink grid actually stops the "1" template from winning, since dividing by each template's norm leaves a residual baseline term that doesn't fully cancel.

The "1" template's negative periphery should keep it from winning generic digits, so I'm planning the vertical and horizontal scalars next and will set their values by hand.

Setting the vertical and horizontal scalars by hand, I'm centering each digit's value around the mean so it reads as relative preference. The gains on those features will be applied uniformly across positions.

Checking the magnitudes now so the gains don't blow up the loss: I'm settling on Gi=12 and Gv=Gh=6, with the scalars centered across digits, and then I'll write the code for the ink template.
