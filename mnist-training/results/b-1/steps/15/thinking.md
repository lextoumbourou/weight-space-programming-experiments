The template scoring looks fragile: 1 and 7 now pull toward each other because their sparse templates have small norms, which pushes k up to 2.3 and inflates other classes' template norms. The sensitivity seems to come from the per-class bias term varying widely with ink amount, since thin and bold digits have very different magnitudes. I want to remove that dependence on ink, probably by normalizing both the features and the templates before comparing them.

I'm moving toward cosine scoring on normalized features and templates, since that drops the k parameter entirely. Any per-class adjustment would then have to come from a bias that scales with ink, and I'm weighing whether retrying cosine with centered, widened templates would help or just repeat the earlier 8 problem.

I'm settling on a scale value of s=10, since the cosine differences between classes come out to a gap of roughly 0.3 on features with norm around 3, which gives about 3 logits.
