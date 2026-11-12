# Weight-Space Programming experiments

Code and results for the extra tests in [Weight-Space Programming](https://notesbylex.com/weight-space-programming.html) and [LLM Descent](https://notesbylex.com/llm-descent.html) on Notes by Lex.

The tests follow Takehi, Teoh, Zhang and Khattab (2026), who found that frontier LLMs can read and write the weights of small neural networks. Their logs are at [RikiyaT/lm_understand-logs](https://github.com/RikiyaT/lm_understand-logs).

| Folder | Question | Models |
|---|---|---|
| [`game-identification/`](game-identification/) | Can other models name the game from the authors' four game-playing networks? | Opus 5.5, Sol 6.1, Terra 6.1, Sonnet 5.5, Haiku 5.5, Gemini 4 Argon, Muse Wonder, Kimi K3.1 Pro |
| [`dqn-blind-test/`](dqn-blind-test/) | Can Astra name the Atari game from my own DQN checkpoints, through a restricted tensor reader? | GPT-6 Astra |
| [`plots/`](plots/) | The weight heatmaps in the post. | - |
| [`mnist-training/`](mnist-training/) | LLM Descent: can Claude train an MNIST CNN by writing all of its weights, improving them from training-set feedback over up to 50 steps? Two conditions: numbers only, and with example images and its own mistakes. | Opus 5.5 |

Earlier experiments (the first MNIST runs and the model comparison cited in the Fable 5.2 post, the Titanic and synthetic tabular runs, and a shelved cats-vs-dogs harness) are kept in version control at commit [`e26658b`](https://github.com/lextoumbourou/weight-space-programming-experiments/tree/e26658b).

Each folder has its own README with setup and run steps. Every run calls a paid model API.

For the DQN blind test, copy the folder to a neutral path before you run it, for example `cp -R dqn-blind-test /tmp/weight-space-harness`. Codex shows the model its working folder path, and a path with "dqn" or "weight-space" in it gives the model a hint.

## What these results do and don't show

- One fresh response per checkpoint, with no retries. Self-reported confidence is not calibrated.
- Each model also gets one shape-only control prompt. All four of the authors' networks share one architecture, so this is one control per model, not four.
- None of this reproduces training, tests new seeds or gives a general success rate.
- Model behaviour can change even when the model ID stays the same.

## Licence

My code is MIT (see [LICENSE](LICENSE)). The four game prompts in `game-identification/prompts/` are the authors' unchanged files, under CC BY 4.0 (see [`game-identification/prompts/LICENSE`](game-identification/prompts/LICENSE)). `shapes.txt` is mine.
