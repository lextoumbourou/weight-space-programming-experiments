Lowering G_D cut the overall evidence, which should make the model less confident, yet accuracy went up while loss got worse. That suggests the model has become under-confident now, so I'm thinking about raising the temperature: moving SCALE from 0.72 up to 0.8, with G_D at 0.5 and GAMMA at 0.

I'm weighing whether the gain came from GAMMA or from lowering G_D, since lowering G_D cut the diagonal weight and might have hurt loss. I'm leaning toward reverting to step 48 and either adjusting GAMMA alone or nudging G_D back up, since the loss trend suggests that direction could help.

I'm weighing the final pick now. Step 48 is already banked, so the last run is a free shot at a lower loss. Option C looks most promising: raise G_D while keeping GAMMA at 0.12. The GAMMA trend suggests 0.12 isn't much worse than 0.3, so lowering G_D was probably what hurt, and raising it may help. I'm settling on G_D around 0.74.

I'm settling on GAMMA at 0.15, a middle value between 0.12 and 0.3, with SCALE kept at 0.72.
