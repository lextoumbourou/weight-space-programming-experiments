"""LLM Descent on MNIST: Claude writes every weight of a fixed CNN, then improves them from feedback.

Each step, Claude replies with a complete `build_weights()`. The harness runs it in the sandbox, scores the network
on the training set (Claude sees the loss, accuracy and confusion matrix) and on the test set (stored, never
shown), then sends the feedback as the next message of the same conversation.

Two conditions, otherwise identical:
  a: numbers only. Claude never sees an image.
  b: Claude also sees 50 example training images at the start, and 16 of its mistakes after every step.

Up to 50 steps. After at least 15, the run stops once the best training loss has not improved by 1% over the last
8 steps. Claude is not told this rule, only that it has up to 50 steps and that its lowest-training-loss network
is scored on the test set.

    uv run python loop.py --condition a --run-id a-1
    uv run python loop.py --condition a --run-id a-1 --resume   # continue an interrupted run
    uv run python loop.py --condition b --run-id plumbing --fake # no API calls: random weights each step
"""
import argparse
import datetime
import hashlib
import json
import re
import time
from pathlib import Path

import numpy as np

import anthropic
import mlx.core as mx

import data
import images
import network
from claude_client import MODEL, PRICES, Conversation, request_settings
from sandbox import run_submission

HERE = Path(__file__).resolve().parent
PROMPTS = HERE / "prompts"
MAX_STEPS, MIN_STEPS, PATIENCE, MIN_GAIN = 50, 15, 8, 0.01
N_MISTAKES = 16

SEEING = {
    "a": "You never see any images. ",
    "b": ("You never see the training set itself, apart from 50 example images shown below and, after each step, "
          f"{N_MISTAKES} training images your network got wrong. "),
}
IMAGE_RULE = {
    "a": "",
    "b": ("- You may look at the images to understand the data, but your code must not contain them or numbers "
          "copied from them. Draw filters and templates from your own description, as before.\n"),
}


def task_prompt(condition):
    shapes = "\n".join(f"    {name}: {shape}" for name, shape in network.SHAPES.items())
    return (PROMPTS / "task.md").read_text().format(
        steps=MAX_STEPS, seeing=SEEING[condition], architecture=network.PYTORCH_DEFINITION,
        n_params=network.N_PARAMS, shapes=shapes, image_rule=IMAGE_RULE[condition])


def first_message(condition, train, folder):
    """Step 1's message: the task, plus (condition b) the example images."""
    text = task_prompt(condition)
    if condition == "a":
        return text, text
    x, y = train
    idx = data.examples(y)
    grid = images.grid(x[idx], columns=5, row_labels=[str(d) for d in range(10)])
    grid.save(folder / "examples.png")
    intro = (PROMPTS / "examples.md").read_text().strip()
    return [{"type": "text", "text": text}, {"type": "text", "text": intro}, images.image_block(grid)], \
        text + "\n\n" + intro + "\n\n[image: examples.png]"


def confusion_text(confusion):
    header = "true \\ predicted " + " ".join(f"{d:>5d}" for d in range(10))
    rows = [f"{d:>16d} " + " ".join(f"{v:>5d}" for v in row) for d, row in enumerate(confusion)]
    return "\n".join([header, *rows])


def feedback(step, train_metrics, error, history, condition, train, folder):
    """The message after a step: results, history, steps left, and (condition b) a grid of mistakes."""
    if error:
        result = f"your code could not be run, so there is no training result for this step.\n\nError:\n{error}"
    else:
        result = (f"training loss {train_metrics['loss']:.4f}, accuracy {train_metrics['accuracy']:.4f}.\n\n"
                  f"Confusion matrix (rows: true digit, columns: predicted digit):\n\n"
                  f"{confusion_text(train_metrics['confusion'])}")
    table = ["step | loss | accuracy", "---- | ---- | --------"]
    table += [f"{h['step']} | {h['train_loss']:.4f} | {h['train_accuracy']:.4f}" if h["ok"]
              else f"{h['step']} | error | error" for h in history]
    left = MAX_STEPS - step
    remaining = (f"At most {left} step{'s' if left != 1 else ''} left. Reply with the complete build_weights() "
                 f"for step {step + 1} in one Python code block.")
    text = (PROMPTS / "feedback.md").read_text().format(
        step=step, steps=MAX_STEPS, result=result, history="\n".join(table), remaining=remaining)
    if condition == "a" or error:
        return text, text
    x, y = train
    wrong = np.flatnonzero(train_metrics["pred"] != y)
    if len(wrong) == 0:
        return text, text
    idx = np.sort(np.random.default_rng(step).choice(wrong, min(N_MISTAKES, len(wrong)), replace=False))
    captions = []
    for i, j in enumerate(idx, 1):
        top = np.argsort(-train_metrics["prob"][j])[:3]
        probs = ", ".join(f"{d} {train_metrics['prob'][j][d]:.2f}" for d in top)
        captions.append(f"{i}. true {y[j]}, predicted {train_metrics['pred'][j]} (top 3: {probs})")
    grid = images.grid(x[idx], columns=4, cell_labels=[str(i) for i in range(1, len(idx) + 1)])
    grid.save(folder / "mistakes.png")
    intro = (PROMPTS / "mistakes.md").read_text().strip().format(step=step, captions="\n".join(captions))
    content = [{"type": "text", "text": text}, {"type": "text", "text": intro}, images.image_block(grid)]
    return content, text + "\n\n" + intro + "\n\n[image: mistakes.png]"


def extract_code(reply):
    blocks = re.findall(r"```(?:python|py)\s*\n(.*?)```", reply, re.S)
    return blocks[-1] if blocks else None


def fake_reply(step):
    """Plumbing test only: PyTorch-style random weights, different each step."""
    return (f"Fake step {step}: random weights.\n\n```python\nimport numpy as np\n\ndef build_weights():\n"
            f"    rng = np.random.default_rng({step})\n"
            f"    shapes = {network.SHAPES!r}\n    fan_in = {network.FAN_IN!r}\n"
            "    return {k: (rng.uniform(-1, 1, s) / np.sqrt(fan_in[k.split('.')[0]])).astype(np.float32)\n"
            "            for k, s in shapes.items()}\n```\n")


def plateaued(history):
    """After MIN_STEPS, stop once the best training loss hasn't improved by MIN_GAIN over the last PATIENCE steps."""
    if len(history) <= PATIENCE or len(history) < MIN_STEPS:
        return None
    best = lambda hs: min([h["train_loss"] for h in hs if h["ok"]], default=float("inf"))
    before, now = best(history[:-PATIENCE]), best(history)
    gain = (before - now) / before if np.isfinite(before) else 1.0
    if gain < MIN_GAIN:
        return f"plateau: best training loss improved by {gain * 100:.2f}% over the last {PATIENCE} steps"
    return None


def save_message(folder, content, readable):
    (folder / "message.md").write_text(readable + "\n")
    (folder / "message.json").write_text(json.dumps(content))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--condition", choices=["a", "b"], required=True)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--fake", action="store_true", help="no API calls; random weights each step")
    args = ap.parse_args()

    run_dir = HERE / "results" / args.run_id
    if run_dir.exists() and not args.resume:
        raise SystemExit(f"{run_dir} exists; use --resume to continue it")
    splits = data.load()
    if args.resume:
        run = json.loads((run_dir / "run.json").read_text())
        history = json.loads((run_dir / "history.json").read_text()) if (run_dir / "history.json").exists() else []
    else:
        first = run_dir / "steps" / "01"
        first.mkdir(parents=True)
        content, readable = first_message(args.condition, splits["train"], first)
        save_message(first, content, readable)
        (run_dir / "prompt.md").write_text(task_prompt(args.condition))
        run = dict(run_id=args.run_id, condition=args.condition, model="fake" if args.fake else MODEL,
                   max_steps=MAX_STEPS, min_steps=MIN_STEPS, patience=PATIENCE, min_gain=MIN_GAIN,
                   rule_told=False, score="lowest training loss", n_mistakes_shown=N_MISTAKES,
                   anthropic_sdk=anthropic.__version__, mlx=mx.__version__, data_sha256=data.SHA256,
                   prompt_sha256=hashlib.sha256(task_prompt(args.condition).encode()).hexdigest(),
                   request=None if args.fake else request_settings(),
                   prices_usd_per_million_tokens=None if args.fake else PRICES,
                   started=datetime.datetime.now(datetime.timezone.utc).isoformat(), status="running")
        (run_dir / "run.json").write_text(json.dumps(run, indent=2))
        history = []

    conversation = None if args.fake else Conversation(run_dir / "messages.json", run["request"])
    if conversation and history:
        # Drop any turn saved after the last recorded step (a crash between the reply and the bookkeeping).
        conversation.messages = conversation.messages[:history[-1]["messages_len"]]
    total_cost = sum(h.get("cost_usd") or 0 for h in history)
    stop_reason = None
    for step in range(len(history) + 1, MAX_STEPS + 1):
        folder = run_dir / "steps" / f"{step:02d}"
        content = json.loads((folder / "message.json").read_text())
        start = time.time()
        if args.fake:
            reply, thinking, receipt = fake_reply(step), "", dict(stop_reason="end_turn", cost_usd=0.0)
        else:
            reply, thinking, receipt, raw = conversation.send(content)
            (folder / "response.json").write_text(json.dumps(raw, indent=1))
        receipt["seconds"] = round(time.time() - start, 1)
        total_cost += receipt["cost_usd"]
        (folder / "reply.md").write_text(reply + "\n")
        if thinking:
            (folder / "thinking.md").write_text(thinking + "\n")

        code = extract_code(reply)
        train = test = None
        if code is None:
            why = {"max_tokens": " (the reply hit the output limit before any code was finished)",
                   "refusal": " (the request was declined)"}.get(receipt["stop_reason"], "")
            sandbox = {"ok": False, "error": "no Python code block was found in your reply" + why}
        else:
            (folder / "submission.py").write_text(code)
            sandbox = run_submission(folder / "submission.py", folder / "weights.npz")
        if sandbox["ok"]:
            weights = dict(np.load(folder / "weights.npz"))
            train = network.evaluate(weights, *splits["train"])
            test = network.evaluate(weights, *splits["test"])  # stored for the write-up, never sent
        summary = lambda m: m and {k: m[k] for k in ("loss", "accuracy", "confusion")}
        (folder / "receipt.json").write_text(json.dumps(receipt, indent=2))
        (folder / "metrics.json").write_text(json.dumps(dict(sandbox=sandbox, train=summary(train),
                                                             test=summary(test)), indent=2))

        usage = receipt.get("usage") or {}
        history.append(dict(step=step, ok=sandbox["ok"], error=None if sandbox["ok"] else sandbox["error"],
                            train_loss=train and train["loss"], train_accuracy=train and train["accuracy"],
                            test_loss=test and test["loss"], test_accuracy=test and test["accuracy"],
                            stop_reason=receipt["stop_reason"], seconds=receipt["seconds"],
                            cost_usd=receipt["cost_usd"], output_tokens=usage.get("output_tokens"),
                            messages_len=len(conversation.messages) if conversation else None))
        (run_dir / "history.json").write_text(json.dumps(history, indent=2))
        shown = (f"train {train['accuracy']:.4f} (loss {train['loss']:.3f}) test {test['accuracy']:.4f}"
                 if train else sandbox["error"][:120])
        print(f"step {step:2d}: {shown}  {receipt['seconds']}s  ${receipt['cost_usd']:.3f} "
              f"(total ${total_cost:.2f})", flush=True)

        stop_reason = plateaued(history)
        if stop_reason:
            print(stop_reason, flush=True)
            break
        if step < MAX_STEPS:
            nxt = run_dir / "steps" / f"{step + 1:02d}"
            nxt.mkdir(exist_ok=True)
            content, readable = feedback(step, train, None if train else sandbox["error"], history,
                                         run["condition"], splits["train"], nxt)
            save_message(nxt, content, readable)

    valid = [h for h in history if h["ok"]]
    best = min(valid, key=lambda h: h["train_loss"]) if valid else None
    run.update(status="finished", finished=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               steps_run=len(history), stop_reason=stop_reason or "step budget used",
               best_step=best and best["step"], best_train_loss=best and best["train_loss"],
               best_test_accuracy=best and best["test_accuracy"],
               failed_steps=[h["step"] for h in history if not h["ok"]], total_cost_usd=round(total_cost, 4))
    (run_dir / "run.json").write_text(json.dumps(run, indent=2))
    print(json.dumps({k: run[k] for k in ("steps_run", "best_step", "best_train_loss", "best_test_accuracy",
                                          "failed_steps", "total_cost_usd", "stop_reason")}))


if __name__ == "__main__":
    main()
