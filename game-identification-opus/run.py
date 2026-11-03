"""Replay the released Experiment 1 prompts through tool-free Claude Code."""
import concurrent.futures
import datetime
import hashlib
import json
import os
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL = "claude-opus-5-5"
EFFORT = "high"


def run_one(sample):
    folder = ROOT / "runs" / sample
    folder.mkdir(exist_ok=False)
    workspace = folder / "workspace"
    workspace.mkdir()
    prompt = (ROOT / "prompts" / f"{sample}.txt").read_text()
    system = (ROOT / "operator/sources/instructions.md").read_text()
    settings = {"disableAllHooks": True, "autoMemoryEnabled": False, "fastMode": False}
    cmd = [
        "claude", "-p", "--bare", "--restricted", "--model", MODEL,
        "--effort", EFFORT, "--tools", "", "--strict-mcp-config",
        "--mcp-config", '{"mcpServers":{}}', "--disable-slash-commands",
        "--no-session-persistence", "--setting-sources", "",
        "--settings", json.dumps(settings), "--system-prompt", system,
        "--permission-prompts", "none", "--output-format", "stream-json", "--verbose",
        "--max-turns", "1",
    ]
    env = {k: v for k, v in os.environ.items() if not (
        k.startswith(("CLAUDE_", "CODEX_")) or
        k in {"PWD", "OLDPWD", "INIT_CWD", "ANTHROPIC_MODEL", "ANTHROPIC_SMALL_FAST_MODEL"} or
        k.startswith("ANTHROPIC_DEFAULT_")
    )}
    # Retain the existing API credential in memory only; never log the environment.
    env["PWD"] = str(workspace)
    record = dict(sample=sample, model=MODEL, effort=EFFORT, command=cmd,
                  started=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  prompt_sha256=hashlib.sha256(prompt.encode()).hexdigest(), status="running")
    (folder / "run.json").write_text(json.dumps(record, indent=2))
    print("START", sample, flush=True)
    start = time.time()
    with (folder / "events.jsonl").open("w") as out, (folder / "stderr.txt").open("w") as err:
        try:
            proc = subprocess.run(cmd, input=prompt, text=True, cwd=workspace, env=env,
                                  stdout=out, stderr=err, timeout=900)
            record["exit_code"] = proc.returncode
        except subprocess.TimeoutExpired:
            record["exit_code"] = None
            record["status"] = "timed_out"
    events = []
    for line in (folder / "events.jsonl").read_text().splitlines():
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    inits = [e for e in events if e.get("type") == "system" and e.get("subtype") == "init"]
    assistants = [e for e in events if e.get("type") == "assistant"]
    tools = [c for e in assistants for c in e.get("message", {}).get("content", [])
             if c.get("type") in {"tool_use", "server_tool_use"}]
    models = sorted({e.get("message", {}).get("model", "") for e in assistants})
    answers = [e for e in events if e.get("type") == "result"]
    final = answers[-1] if answers else {}
    record.update(seconds=time.time()-start, observed_models=models,
                  init=inits, tool_calls=tools, result=final)
    record["tool_free"] = not tools and bool(inits) and all(not e.get("tools") for e in inits)
    if record["status"] != "timed_out":
        record["status"] = "completed" if record["exit_code"] == 0 and final.get("subtype") == "success" and record["tool_free"] and all(MODEL in m for m in models) and models else "failed"
    if "result" in final:
        (folder / "answer.md").write_text(final["result"] + "\n")
    (folder / "run.json").write_text(json.dumps(record, indent=2))
    print("END", sample, record["status"], round(record["seconds"], 1),
          "models", models, "tool_free", record["tool_free"], flush=True)
    return record


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", nargs="+")
    parser.add_argument("--workers", type=int, default=2)
    args = parser.parse_args()
    cases = args.only or ["sample_01", "sample_02", "sample_03", "sample_04", "shapes"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        records = list(pool.map(run_one, cases))
    print(json.dumps([{k: r.get(k) for k in ["sample", "status", "seconds", "observed_models", "tool_free"]} for r in records]), flush=True)
