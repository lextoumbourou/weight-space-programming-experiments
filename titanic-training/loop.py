"""Can an LLM train a Titanic survival MLP by writing its weights, guided only by validation loss and a confusion matrix?

Each step, the model replies with a complete `build_weights()`. The harness runs it in the sandbox, scores the network
on the validation set (the model sees loss, accuracy and confusion matrix) and on the test set (stored, never shown),
then sends the feedback as the next message of the same conversation (Messages API, full history each turn).
Everything needed for the write-up is saved per step.

    uv run python loop.py --run-id opus-high-strict-1         # 15 steps, Opus 5.5, effort high
    uv run python loop.py --run-id opus-high-strict-1 --resume # continue an interrupted run
    uv run python loop.py --run-id plumbing-check --fake --steps 3   # no API calls: random weights each step
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

import data
import network
from claude_client import PRICES, Conversation, request_settings
from sandbox import run_submission

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"
SYSTEM_PROMPT = "Answer the user's request."
MAX_OUTPUT_TOKENS = 128_000  # the model maximum, so a long reply is not cut off
PROMPTS, CLASSES, ARCHITECTURE = HERE / "prompts", network.CLASSES, network.PYTORCH_DEFINITION


def set_variant(anonymous):
    """The anonymised variant hides the dataset: shuffled, standardised columns and its own prompt files."""
    global PROMPTS, CLASSES, ARCHITECTURE
    if anonymous:
        PROMPTS, CLASSES, ARCHITECTURE = HERE / "prompts/anonymous", network.ANONYMOUS_CLASSES, network.ANONYMOUS_DEFINITION


def initial_prompt(steps, run=None):
    shapes = "\n".join(f"    {name}: {shape}" for name, shape in network.SHAPES.items())
    stop_rule = plateau_rule(run) + " " if run and run.get("patience") and run.get("rule_told", True) else ""
    return (PROMPTS / "task.md").read_text().format(
        steps=steps, architecture=ARCHITECTURE, n_params=network.N_PARAMS, shapes=shapes,
        stop_rule=stop_rule, scored=scored_text(run))


def scored_text(run):
    if run and run.get("score") == "best_val_loss":
        return "the network from the step with the lowest validation loss"
    return "the network from your final step"


def confusion_text(confusion):
    names = CLASSES
    width = max(len(n) for n in names) + 2
    header = "true \\ predicted".ljust(18) + "".join(f"{n:>{width}}" for n in names)
    rows = [f"{names[d]:>17} " + "".join(f"{v:>{width}d}" for v in row) for d, row in enumerate(confusion)]
    return "\n".join([header, *rows])


def plateau_rule(run):
    if run.get("plateau_metric") == "loss":
        return (f"The run stops early, after any step, once the best validation loss has not improved by at least "
                f"{run['min_gain'] * 100:.0f}% over the previous {run['patience']} steps.")
    return (f"The run stops early, after any step, if validation accuracy has not improved by at least "
            f"{run['min_gain'] * 100:.1f} percentage points over the previous {run['patience']} steps.")


def feedback_message(step, steps, metrics, error, history, run=None, extension_note=None):
    if error:
        result = f"your code could not be run, so there is no validation result for this step.\n\nError:\n{error}"
    else:
        result = (f"validation loss {metrics['loss']:.4f}, accuracy {metrics['accuracy']:.4f}.\n\n"
                  f"Confusion matrix (rows: true class, columns: predicted class):\n\n{confusion_text(metrics['confusion'])}")
    table = ["step | loss | accuracy", "---- | ---- | --------"]
    for h in history:
        table.append(f"{h['step']} | {h['val_loss']:.4f} | {h['val_accuracy']:.4f}" if h["ok"] else f"{h['step']} | error | error")
    left = steps - step
    if run and run.get("patience") and not run.get("rule_told", True):
        remaining = (f"At most {left} step{'s' if left != 1 else ''} left. Reply with the complete build_weights() "
                     f"for step {step + 1} in one Python code block.")
    elif run and run.get("patience"):
        remaining = (f"At most {left} step{'s' if left != 1 else ''} left. {plateau_rule(run)} The network from the "
                     f"last step that runs is scored on the test set. Reply with the complete build_weights() for "
                     f"step {step + 1} in one Python code block.")
    else:
        remaining = (f"{left} step{'s' if left != 1 else ''} left. Reply with the complete build_weights() for step "
                     f"{step + 1} in one Python code block.")
    if extension_note:
        remaining = extension_note + "\n\n" + remaining
    return (PROMPTS / "feedback.md").read_text().format(
        step=step, steps=steps, result=result, history="\n".join(table), remaining=remaining)


def extract_code(reply):
    blocks = re.findall(r"```(?:python|py)\s*\n(.*?)```", reply, re.S)
    return blocks[-1] if blocks else None


def fake_reply(step):
    """Plumbing test only: PyTorch-style random weights, different each step."""
    return (f"Fake step {step}: random weights.\n\n```python\nimport numpy as np\n\ndef build_weights():\n"
            f"    rng = np.random.default_rng({step})\n"
            "    shapes = " + repr(network.SHAPES) + "\n"
            "    fan_in = " + repr(network.FAN_IN) + "\n"
            "    return {k: (rng.uniform(-1, 1, s) / np.sqrt(fan_in[k.split('.')[0]])).astype(np.float32)\n"
            "            for k, s in shapes.items()}\n```\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--model", default="claude-opus-5-5", choices=sorted(PRICES))
    ap.add_argument("--effort", default="high")
    ap.add_argument("--steps", type=int, default=15)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--fake", action="store_true", help="no API calls; random weights each step")
    ap.add_argument("--extend-to", type=int, help="with --resume: raise a finished run's step budget to this total")
    ap.add_argument("--patience", type=int, default=5, help="steps without enough improvement before stopping")
    ap.add_argument("--min-gain", type=float, default=0.005,
                    help="accuracy rule: points as a fraction; loss rule: relative improvement")
    ap.add_argument("--plateau", choices=["none", "loss"], default="none",
                    help="new runs: stop early on a validation-loss plateau")
    ap.add_argument("--min-steps", type=int, default=0, help="plateau: never stop before this step")
    ap.add_argument("--anonymous", action="store_true",
                    help="new runs: hide the dataset (shuffled, standardised, unnamed features)")
    ap.add_argument("--hide-rule", action="store_true",
                    help="plateau: don't tell the model the stopping rule; score the lowest-validation-loss step")
    args = ap.parse_args()

    run_dir = RESULTS / args.run_id
    if run_dir.exists() and not args.resume:
        raise SystemExit(f"{run_dir} exists; use --resume to continue it")
    anonymous = (json.loads((run_dir / "run.json").read_text()).get("anonymous", False) if args.resume
                 else args.anonymous)
    set_variant(anonymous)
    splits = data.load(anonymous=anonymous)
    if args.resume:
        run = json.loads((run_dir / "run.json").read_text())
        history = json.loads((run_dir / "history.json").read_text()) if (run_dir / "history.json").exists() else []
        if args.extend_to and args.extend_to > run["steps"]:
            if len(history) != run["steps"]:
                raise SystemExit("finish the current budget before extending it")
            old_steps = run["steps"]
            run.setdefault("extensions", []).append(dict(
                after_step=old_steps, to_steps=args.extend_to, patience=args.patience, min_gain=args.min_gain,
                at=datetime.datetime.now(datetime.timezone.utc).isoformat()))
            run.update(steps=args.extend_to, patience=args.patience, min_gain=args.min_gain,
                       plateau_check_from=old_steps + 1, status="running")
            note = (f"The step budget has been extended. Step {old_steps} was not your last step: you now have up "
                    f"to {args.extend_to - old_steps} more steps, up to step {args.extend_to} in total.")
            last = history[-1]
            metrics = json.loads((run_dir / "steps" / f"{old_steps:02d}" / "metrics.json").read_text())
            nxt = run_dir / "steps" / f"{old_steps + 1:02d}"
            nxt.mkdir(exist_ok=True)
            (nxt / "message.md").write_text(feedback_message(
                old_steps, run["steps"], metrics["val"], None if last["ok"] else last["error"], history, run, note))
            (run_dir / "run.json").write_text(json.dumps(run, indent=2))
    else:
        (run_dir / "steps").mkdir(parents=True)
        plateau = (dict(plateau_metric="loss", patience=args.patience, min_gain=args.min_gain, plateau_check_from=1,
                        min_steps=args.min_steps, rule_told=not args.hide_rule,
                        score="best_val_loss" if args.hide_rule else "final")
                   if args.plateau == "loss" else {})
        prompt = initial_prompt(args.steps, plateau)
        (run_dir / "prompt.md").write_text(prompt)
        import mlx.core as mx
        run = dict(run_id=args.run_id, model="fake" if args.fake else args.model, effort=args.effort, anonymous=anonymous, **plateau,
                   steps=args.steps, anthropic_sdk=anthropic.__version__, mlx=mx.__version__,
                   data_sha256=data.SHA256, prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(),
                   request=None if args.fake else request_settings(args.model, args.effort, MAX_OUTPUT_TOKENS, SYSTEM_PROMPT),
                   prices_usd_per_million_tokens=None if args.fake else PRICES[args.model],
                   started=datetime.datetime.now(datetime.timezone.utc).isoformat(), status="running")
        (run_dir / "run.json").write_text(json.dumps(run, indent=2))
        history = []
        first = run_dir / "steps" / "01"
        first.mkdir()
        (first / "message.md").write_text(prompt)

    conversation = None if args.fake else Conversation(run_dir / "messages.json", run["request"])
    if conversation and history:
        # Drop any turn saved after the last recorded step (a crash between the reply and the bookkeeping).
        conversation.messages = conversation.messages[:history[-1]["messages_len"]]
    total_cost = sum(h.get("cost_usd") or 0 for h in history)
    for step in range(len(history) + 1, run["steps"] + 1):
        folder = run_dir / "steps" / f"{step:02d}"
        message = (folder / "message.md").read_text()
        start = time.time()
        if args.fake:
            reply, thinking, receipt = fake_reply(step), "", dict(stop_reason="end_turn", cost_usd=0.0)
        else:
            reply, thinking, receipt, raw = conversation.send(message)
            (folder / "response.json").write_text(json.dumps(raw, indent=1))
        receipt["seconds"] = round(time.time() - start, 1)
        total_cost += receipt["cost_usd"]
        (folder / "reply.md").write_text(reply + "\n")
        if thinking:
            (folder / "thinking.md").write_text(thinking + "\n")

        code = extract_code(reply)
        val = test = None
        if code is None:
            why = {"max_tokens": " (the reply hit the output limit before any code was finished)",
                   "refusal": " (the request was declined)"}.get(receipt["stop_reason"], "")
            sandbox = {"ok": False, "error": "no Python code block was found in your reply" + why}
        else:
            (folder / "submission.py").write_text(code)
            sandbox = run_submission(folder / "submission.py", folder / "weights.npz")
        if sandbox["ok"]:
            weights = dict(np.load(folder / "weights.npz"))
            val = network.evaluate(weights, *splits["val"])
            test = network.evaluate(weights, *splits["test"])  # stored for the write-up, never sent
        (folder / "receipt.json").write_text(json.dumps(receipt, indent=2))
        (folder / "metrics.json").write_text(json.dumps(dict(sandbox=sandbox, val=val, test=test), indent=2))

        usage = receipt.get("usage") or {}
        entry = dict(step=step, ok=sandbox["ok"], error=None if sandbox["ok"] else sandbox["error"],
                     val_loss=val and val["loss"], val_accuracy=val and val["accuracy"],
                     test_loss=test and test["loss"], test_accuracy=test and test["accuracy"],
                     stop_reason=receipt["stop_reason"], seconds=receipt["seconds"], cost_usd=receipt["cost_usd"],
                     output_tokens=usage.get("output_tokens"),
                     thinking_tokens=(usage.get("output_tokens_details") or {}).get("thinking_tokens"),
                     cache_read_tokens=usage.get("cache_read_input_tokens"),
                     cache_write_tokens=usage.get("cache_creation_input_tokens"),
                     messages_len=len(conversation.messages) if conversation else None)
        history.append(entry)
        (run_dir / "history.json").write_text(json.dumps(history, indent=2))
        shown = f"val {val['accuracy']:.4f} (loss {val['loss']:.3f}) test {test['accuracy']:.4f}" if val else sandbox["error"][:120]
        print(f"step {step:2d}: {shown}  {receipt['seconds']}s  ${receipt['cost_usd']:.3f} (total ${total_cost:.2f})", flush=True)

        if run.get("plateau_metric") == "loss":
            # Best validation loss now against the best up to `patience` steps ago; needs one step before the window.
            if step > run["patience"] and step >= run.get("min_steps", 0):
                best = lambda hs: min([h["val_loss"] for h in hs if h["ok"]], default=float("inf"))
                before, now = best(history[:-run["patience"]]), best(history)
                gain = (before - now) / before if np.isfinite(before) else 1.0
                if gain < run["min_gain"]:
                    run["stop_reason"] = (f"plateau: best validation loss improved by {gain * 100:.2f}% over the last "
                                          f"{run['patience']} steps")
                    print(run["stop_reason"], flush=True)
                    break
        elif run.get("patience") and step >= run["plateau_check_from"] + run["patience"] - 1:
            acc = lambda hs: max([h["val_accuracy"] for h in hs if h["ok"]], default=0.0)
            gain = acc(history) - acc(history[:-run["patience"]])
            if gain < run["min_gain"]:
                run["stop_reason"] = (f"plateau: validation accuracy improved by {gain * 100:.2f} points over the "
                                      f"last {run['patience']} steps")
                print(run["stop_reason"], flush=True)
                break
        if step < run["steps"]:
            nxt = run_dir / "steps" / f"{step + 1:02d}"
            nxt.mkdir(exist_ok=True)
            (nxt / "message.md").write_text(feedback_message(step, run["steps"], val, None if val else sandbox["error"], history, run))

    valid = [h for h in history if h["ok"]]
    final = valid[-1] if valid else None
    best = max(valid, key=lambda h: h["val_accuracy"]) if valid else None
    best_loss = min(valid, key=lambda h: h["val_loss"]) if valid else None
    run.update(best_val_loss_step=best_loss and best_loss["step"],
               best_val_loss_test_accuracy=best_loss and best_loss["test_accuracy"])
    run.update(status="finished", finished=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               final_step=final and final["step"], final_test_accuracy=final and final["test_accuracy"],
               best_val_step=best and best["step"], best_val_test_accuracy=best and best["test_accuracy"],
               failed_steps=[h["step"] for h in history if not h["ok"]], total_cost_usd=round(total_cost, 4))
    (run_dir / "run.json").write_text(json.dumps(run, indent=2))
    run.setdefault("stop_reason", "step budget used")
    (run_dir / "run.json").write_text(json.dumps(run, indent=2))
    print(json.dumps({k: run[k] for k in ("final_step", "final_test_accuracy", "best_val_loss_step",
                                          "best_val_loss_test_accuracy", "failed_steps", "total_cost_usd",
                                          "stop_reason")}))


if __name__ == "__main__":
    main()
