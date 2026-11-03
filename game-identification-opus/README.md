# Opus 5.5 replay of the original game-identification experiment

Source: Takehi, Teoh, Zhang and Khattab (2026), https://github.com/RikiyaT/lm_understand-logs/tree/4d09ba6d6a7e891dd8063974dfe81b3d78e3494f/exp1_which_game . Original prompts/data: CC BY 4.0; original scripts: MIT. See LICENSE. The four primary prompts are unchanged and match the pinned Git blob hashes recorded in source-hashes.json. The additional shapes prompt removes numerical values and is one shared control because all architectures and interfaces are identical.

Run in a neutral directory with Python 3.11+ and Claude Code 2.1.304. Authenticate with ANTHROPIC_API_KEY in your environment; --bare does not use your Claude subscription login. Never put the key in a prompt or this directory. The tested machine already had API authentication configured. This makes billed model calls; the five completed calls reported USD 2.69247 in total. Future usage and prices may differ.

```sh
claude --version
python3 run.py --workers 2
```

The runner requests claude-opus-5-5 at high effort, as in the original Astra experiment. Effort names do not establish equal computation across models. Every case runs once in a fresh empty workspace and receives the original neutral system instruction. Built-in tools, MCP, skills, memory, project instructions and user settings are disabled with --bare, --restricted, --tools "", --strict-mcp-config and an empty MCP configuration. There is no fallback model. The environment is cleaned of model/effort overrides without logging credentials.

Outputs: runs/<sample>/answer.md, events.jsonl, stderr.txt, run.json. Check that init.tools and init.mcp_servers are empty, every assistant response uses the requested model, there are no tool-use blocks and the final result is successful. The runner performs these checks. The original authors' answer format is preserved; no JSON output schema is imposed. Existing run folders cause an error. Do not pass this README or the source answer key to a tested session.

Only after all responses are saved, compare the Game: lines with the original answer key. sample_01 = Breakout, sample_02 = Pong, sample_03 = Pac-Man, sample_04 = Freeway. The authors' scoring accepts Frogger (a road-crossing game) for Freeway. The shape-only response is a prior diagnostic, not four independent trials. This replays the released examples and does not reproduce PPO training, independent seeds or a general success rate.

The article's result JSON includes final explanations and usage. Raw private logs include returned model metadata and are preserved separately. No hidden reasoning from the organising assistant is included.
