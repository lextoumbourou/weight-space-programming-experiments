I've reached 57%, so I'm looking for a stronger approach. Since the classifier is linear, it's effectively a nearest-centroid method, which suggests averaging templates over variations like slants, widths, and small shifts to better approximate each class mean.

I'm averaging each digit's features over slants, stroke widths, and small shifts, and adding per-digit variants like open or closed 4s and crossbar or no-crossbar 7s. I'm also considering centering each image on its center of mass at about pixel 14.

I'm working out a bounding-box normalization that scales each digit so its larger dimension fits 19 pixels, then checking how the center-of-mass shift affects classes like 7, 6, and 9. I'm also noting the main confusions to target, 6 to 0, 8 to 2/6/7, and 4 to 9, and sketching variant shapes for 0, 1, 2, 3, and 4 to add to the templates.

I'm sketching a few more per-digit variants, like a curved-stem 6, a straight-stem 9, and a vertical-stroke 4. I'm also planning augmentations over slant, width, and small pixel shifts, which means roughly 30 versions per variant.

Still writing the vectorized feature code...

I'm keeping the center-of-mass alignment at roughly pixel 14 and the same feature normalization, and I'm not changing the loss target of 1.26 at 57% for now.
