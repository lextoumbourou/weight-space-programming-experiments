Centre-versus-border contrast gives no signal, with the numbers nearly equal, so I'm setting spatial location aside. Texture is the strongest cue so far, green is modest, ears are weak and reversed, and brightness and centre-border are both ruled out. Now I'm weighing what could explain the remaining pattern, since further probes are expensive.

I'm wondering whether the texture signal comes from a particular spatial scale or orientation, or simply from overall contrast, since outdoor dog photos may be higher contrast. I'm also thinking about how cat close-ups differ from dog photos: cat eyes are prominent high-contrast blobs at this resolution, and dogs' eyes are smaller and darker. Since texture pushes everything toward "dog," a cat detector would need normalizing against texture, and I'm considering an HOG-style descriptor with a few tunable parameters as the most efficient next step.

Now I'm weighing how to build the next probes: testing vertical against horizontal texture energy first, then diagonal against the others, fine against coarse scale, and top against bottom, before moving on to colour and blob cues.

Next I'm deciding which probes to run and in what order, since I can only afford a few more: vertical versus horizontal texture energy first, then diagonal, then fine versus coarse scale, then top versus bottom.
