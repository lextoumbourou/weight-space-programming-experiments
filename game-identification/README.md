# Game identification replay

Replays the authors' Experiment 1 ([source](https://github.com/RikiyaT/lm_understand-logs/tree/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp1_which_game)) on five other models. Each prompt holds one trained game-playing network: the 10 × 10 grid layout, the channel and action meanings, the network formula and all 17,253 weights, rounded to three decimals. No game list is given.

`prompts/sample_01.txt` to `sample_04.txt` are byte-identical to the authors' files. `source-proof.json` has the Git blob SHA-1 and SHA-256 of each. `prompts/shapes.txt` is my control: the same text with the numbers removed.

## Quick check

Send one of the authors' prompts straight to a model, with tools off:

```sh
curl -sL https://raw.githubusercontent.com/RikiyaT/lm_understand-logs/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp1_which_game/runs/breakout/prompt.txt \
  | claude -p --model claude-opus-5-5 --effort high --tools ""
```

Swap `breakout` for `pong`, `pacman` or `freeway`, then read the `Game:` line.

## Full replay

Needs Python 3.11+, Codex CLI 0.164.0 (logged in) and Claude Code 2.1.304. Claude Code's `--bare` mode needs `ANTHROPIC_API_KEY`; it does not use a subscription login.

```sh
python3 run.py --workers 4      # 25 sessions: 5 models × (4 games + 1 control)
python3 score.py
```

Or a subset:

```sh
python3 run.py --models opus sol --samples shapes sample_01 --workers 2
```

`score.py` expects all five cases for each model it finds in `runs/`.

Each case runs once, in a fresh empty folder, at `high` effort, with the authors' neutral system instruction (`instructions.md`). Tools, MCP, skills, memory, hooks and personal settings are off. The runner checks the event stream for tool use and marks the case failed if it finds any. Existing case folders are never overwritten.

Saved per case in `runs/`: the command, raw events, stderr, the answer and a `run.json` audit. Raw events can contain host and session IDs, so `runs/` is ignored by git. Check them before you share them.

Scoring uses the authors' keyword rule on the `Game:` line: Breakout or Arkanoid, Pong, Pac-Man, and Freeway or Frogger. `score.py` freezes answer hashes before it reads the answer key.

## Published results

- `results/opus-original-game-results.json`: Opus 5.5, all answers and usage. The five calls reported US$2.69.
- `results/four-model-game-results.json`: Sol, Terra, Sonnet and Haiku, with answers, scores and usage. Sonnet and Haiku reported US$1.38. Codex does not report a cost.
- `operator/`: the frozen protocols and source hashes from the original runs.

The Opus results came from a separate Opus-only runner with the same Claude settings. It is in the first commit of this repo.
