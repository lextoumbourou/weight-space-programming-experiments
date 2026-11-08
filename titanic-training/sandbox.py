"""Run a model-written `build_weights()` in a separate Python process with only numpy and math importable.

The submission gets no `open`, `exec`, `eval` or `compile`, and cannot import anything else, so it has no way to
read data. Every submission is also kept for a person to read.

Command line (used by `run_submission`): python -I sandbox.py SUBMISSION.py OUT.npz
"""
import json
import subprocess
import sys
from pathlib import Path

ALLOWED_IMPORTS = {"numpy", "math"}
TIME_LIMIT_SECONDS = 300


def run_submission(source_path, out_path):
    """Returns {"ok": True, ...} with the weights saved to out_path, or {"ok": False, "error": ...}."""
    try:
        result = subprocess.run([sys.executable, "-I", __file__, str(source_path), str(out_path)],
                                capture_output=True, text=True, timeout=TIME_LIMIT_SECONDS,
                                cwd=Path(out_path).parent)
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"build_weights() took longer than {TIME_LIMIT_SECONDS} seconds"}
    lines = [line for line in result.stdout.splitlines() if line.startswith("{")]
    if not lines:
        return {"ok": False, "error": "the code crashed:\n" + result.stderr[-2000:]}
    return json.loads(lines[-1])


def _main():
    import builtins
    import resource

    import numpy as np

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from network import SHAPES

    source_path, out_path = sys.argv[1:3]
    resource.setrlimit(resource.RLIMIT_CPU, (TIME_LIMIT_SECONDS, TIME_LIMIT_SECONDS))

    def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
        if level != 0 or name.split(".")[0] not in ALLOWED_IMPORTS:
            raise ImportError(f"import of {name!r} is not allowed (only numpy and math)")
        return builtins.__import__(name, globals, locals, fromlist, level)

    blocked = {"open", "exec", "eval", "compile", "input", "breakpoint", "__import__", "help", "exit", "quit"}
    safe_builtins = {k: getattr(builtins, k) for k in dir(builtins) if k not in blocked}
    safe_builtins["__import__"] = guarded_import
    namespace = {"__builtins__": safe_builtins, "__name__": "submission"}
    try:
        exec(compile(open(source_path).read(), "submission.py", "exec"), namespace)
        if "build_weights" not in namespace:
            raise ValueError("the code does not define build_weights()")
        weights = namespace["build_weights"]()
        if not isinstance(weights, dict):
            raise ValueError("build_weights() must return a dict")
        missing, extra = set(SHAPES) - set(weights), set(weights) - set(SHAPES)
        if missing or extra:
            raise ValueError(f"wrong parameter names: missing {sorted(missing)}, unexpected {sorted(extra)}")
        arrays = {}
        for name, shape in SHAPES.items():
            a = np.asarray(weights[name], dtype=np.float32)
            if a.shape != shape:
                raise ValueError(f"{name} has shape {a.shape}, expected {shape}")
            if not np.all(np.isfinite(a)):
                raise ValueError(f"{name} contains NaN or infinite values")
            arrays[name] = a
        np.savez(out_path, **arrays)
        print(json.dumps({"ok": True, "nonzero": int(sum((a != 0).sum() for a in arrays.values()))}))
    except Exception as error:
        print(json.dumps({"ok": False, "error": f"{type(error).__name__}: {error}"}))


if __name__ == "__main__":
    _main()
