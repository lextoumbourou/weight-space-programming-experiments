# Four-model game-identification replay

Original experiment: Takehi, Teoh, Zhang and Khattab (2026), https://github.com/RikiyaT/lm_understand-logs/tree/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp1_which_game . Original prompt/data license CC BY 4.0, original scripts MIT; see LICENSE. source-proof.json records the exact Git blob SHA1 and SHA256 of each unchanged prompt. Each contains all 17,253 trained actor weights as supplied to the original Astra experiment, rounded to three decimals. No full-precision binary network is supplied to a tested session.

Run in a neutral folder with Python 3.11+, Codex CLI 0.164.0 and Claude Code 2.1.304. Configure normal Codex login and API authentication for Claude Code. --bare requires ANTHROPIC_API_KEY (or an explicitly configured helper); it does not use the Claude subscription login. Never place credentials in a prompt or this bundle. Calls consume model usage.

```sh
python3 run.py --workers 4
python3 score.py
```

This runs 20 fresh one-response cases: Sol 6.1, Terra 6.1, Sonnet 5.5 and Haiku 5.5, each on four original numerical prompts and one shared shape/layout-only control. All request high effort, matching the authors' game test and prior Opus replay. Effort names do not equate compute across model families. All built-in tools and MCP are disabled, personal config/instructions are excluded and the neutral system instruction matches the source. Codex's startup notice about its disabled code-mode host is expected; no code tool is exposed.

Run one subset instead:

```sh
python3 run.py --models sol terra --samples sample_01 sample_02 --workers 2
```

Do not rerun existing cases in one directory; the runner preserves them by failing if a case folder exists. Prompts, commands, hashes, raw events, stderr, final answers and audits are saved per case. Claude model IDs and empty tool/MCP lists are checked from response/init records. Codex pins the model in the exact successful command, but its public JSON stream may not expose a response model ID. No fallback is configured for either provider. Raw private event logs can contain host/session identifiers, so sanitize them before sharing.

Freeze answers before scoring the Game: line with the source rule: Breakout/Arkanoid, Pong, Pac-Man, and Freeway/Frogger (road crossing). source-proof.json maps source files to sample IDs for the operator; do not send it or this README to a tested model. Confidence is subjective. The common shape-only control is one diagnostic per model, not four independent trials. One checkpoint and one response per game cannot establish a general success rate. No training, inference through the policy network or activations are involved.
