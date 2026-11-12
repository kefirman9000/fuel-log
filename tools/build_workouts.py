#!/usr/bin/env python3
"""Build workouts.json from tools/workouts_src.py and check that every reference is valid.

    python3 tools/build_workouts.py
"""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from workouts_src import EX, W, P, ACTS

root = os.path.join(os.path.dirname(__file__), "..")
errors = []
FOCUS = {"full", "upper", "lower", "push", "pull", "legs", "core", "cardio"}
GOALS = {"muscle", "strength", "fat", "endurance", "general"}
for w in W:
    for b in w["b"]:
        if b[0] not in EX:
            errors.append(f'{w["id"]}: unknown exercise {b[0]}')
    if w["focus"] not in FOCUS: errors.append(f'{w["id"]}: focus {w["focus"]}')
    if set(w["goal"]) - GOALS: errors.append(f'{w["id"]}: goal {w["goal"]}')
    eq = set()
    for b in w["b"]:
        eq |= set(EX.get(b[0], {}).get("eq", []))
    w["eq"] = sorted(eq)
    # equipment class for filtering
    if eq & {"mach", "cable"} and eq & {"bb", "db"}: w["eqc"] = "gym"
    elif eq & {"mach", "cable"}: w["eqc"] = "mach"
    elif "cardio" in eq: w["eqc"] = "cardio"
    elif "bb" in eq: w["eqc"] = "bb"
    elif "kb" in eq: w["eqc"] = "kb"
    elif "db" in eq: w["eqc"] = "db"
    else: w["eqc"] = "none"
    # body parts worked: muscles hit by at least two exercises (or by the only exercise)
    c = collections.Counter(m for b in w["b"] for m in EX.get(b[0], {}).get("m", []))
    w["mus"] = sorted(m for m, k in c.items() if k >= 2 or len(w["b"]) == 1)
    w["met"], w["metsrc"] = w["met"]
ids = {w["id"] for w in W}
assert len(ids) == len(W), "duplicate workout ids"
for p in P:
    for r in p["rot"]:
        if r not in ids: errors.append(f'{p["id"]}: unknown workout {r}')
if errors:
    raise SystemExit("\n".join(errors))
out = {"source": "Standard exercises and programming. MET values from the 2024 Adult Compendium of Physical Activities (Herrmann et al., J Sport Health Sci 2024).",
       "ex": EX, "w": W, "p": P, "acts": ACTS}
json.dump(out, open(os.path.join(root, "workouts.json"), "w"), separators=(",", ":"), ensure_ascii=False)
print(f"{len(EX)} exercises, {len(W)} workouts, {len(P)} plans, {len(ACTS)} activities")
print(collections.Counter(w["eqc"] for w in W)); print(collections.Counter(w["focus"] for w in W))
