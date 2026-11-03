# Blind weight-inspection harness

Companion to NotesByLex's Weight Space Programming article. Run with a logged-in Codex CLI and Python 3.11+. The original tests used Codex CLI 0.164.0 on macOS, `gpt-6-astra`, `xhigh`, NumPy 2.3.4. Model access is required. Model behavior can change even when the model ID stays the same.

This bundle contains no checkpoints, credentials or answer keys. Download or supply checkpoints separately. Use a fresh copy of this directory for each preparation, since payload and run names are fixed. Use a neutral directory name outside the source project.

## Install

```sh
uv venv --python 3.11
uv pip install --python .venv/bin/python 'numpy==2.3.4'
codex --version
```

## Reproduce the DQN pilot

In another directory, obtain the source checkpoints at Git commit `62abb11245b35bf30f6967649ae2164b6796599f` from `https://github.com/lextoumbourou/deep-q-network-mlx`. From the harness directory:

```sh
.venv/bin/python prepare-games.py --source /absolute/path/to/deep-q-network-mlx/weights
.venv/bin/python run-games.py --workers 2
```

This prepares all three epoch-200 checkpoints and runs six independent sessions: numerical weights and shape-only controls. The preparation uses the original sorted tensor order and seeded checkpoint shuffle. `operator/manifest.json` contains the answer key and integrity hashes. `run-games.py` is the original DQN runner; the preparation helper only replaces its original machine-specific source path with a command-line argument.

For a single case:

```sh
.venv/bin/python run-games.py --only sample_01 shapes
.venv/bin/python run-games.py --only sample_01 weights
```

Never run the same case twice in one directory. Existing folders are preserved and cause an error. The default worker count is two; use one for sequential execution. The model/effort and original JSON output schema are defined in the runner.

## What the model sees

Each run starts `codex exec` in an empty workspace. Personal config, rules, project instructions, skills and memory are disabled, alongside shell, browser, apps, subagents and image tools. The only configured data tool is the fixed `tensors` MCP server. The network restriction applies to agent tool use; Codex itself still connects to OpenAI to run the model.

`reader.py` can list the anonymous catalog, calculate descriptive statistics, return up to 4,096 entries per slice, summarize tensor axes and compute small singular-value decompositions. There is a 24-call budget, including rejected requests. Shape-only mode advertises only `catalog` and rejects the other operations. It does not provide a Python interpreter, arbitrary code, file paths, network requests or a forward pass.

`-s read-only` alone would not hide source files. Blinding depends on disabling general-purpose access and using this fixed reader. These are tested settings for CLI 0.164.0, not a claim of protection against every future tool implementation or malicious runtime. Review the recorded tool calls if adapting the harness to another CLI version. The reader's MCP annotations and approval mode are necessary for calls to work with `approval_policy="never"`; `code_mode_host=true` is needed to expose MCP in this CLI, while the general code tool is disabled.

## Inspect and score

Each case writes `prompt.txt`, `answer.json`, `reader.jsonl`, `events.jsonl`, `stderr.txt` and `run.json`. The latter records the exact command, model/effort, prompt hash, duration, usage and a tool-surface audit. Actual reader-call metadata records model, effort and sandbox; verify those against the intended settings. Check the final probabilities sum to one and score only after freezing the answers. Report architecture recognition separately from task identification, and always report the shape control beside the numerical result.

Raw event/reader logs may include local paths, session identifiers and host metadata. The article's trace download is a sanitized copy. These are observable tool calls plus final explanations, not hidden reasoning transcripts. One model and one response per condition do not establish a general success rate. The restricted reader is also a narrower tool surface than an unrestricted analysis sandbox.

The full prompts and schemas are embedded in the runners. Run `python run-games.py --help` for case selection. Source and payload checksums stay operator-side; do not paste the source map or this README into a blind model session.
