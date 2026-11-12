#!/usr/bin/env python3
"""Build recipes.json from tools/recipes_src.py, with nutrition per serving from foods.json.

    python3 tools/build_recipes.py

Every ingredient's food name must exist in foods.json. Salt, spices and anything
marked None are not counted.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from recipes_src import RECIPES

root = os.path.join(os.path.dirname(__file__), "..")
foods = {r[0]: r for r in json.load(open(os.path.join(root, "foods.json")))["foods"]}
missing, out = [], []
for r in RECIPES:
    tot = dict(kcal=0, p=0, c=0, f=0, fi=0, su=0, na=0)
    for text, name, g in r["ing"]:
        if not name:
            continue
        row = foods.get(name)
        if not row:
            missing.append((r["id"], name)); continue
        k = g / 100
        for key, i in (("kcal", 2), ("p", 3), ("c", 4), ("f", 5), ("fi", 6), ("su", 7), ("na", 8)):
            tot[key] += (row[i] or 0) * k
    n = {k: round(v / r["serves"], 1) for k, v in tot.items()}
    n["kcal"] = round(n["kcal"]); n["na"] = round(n["na"])
    tags = []
    if n["p"] >= 25 or (r["meal"] == "snack" and n["p"] >= 12): tags.append("protein")
    if n["kcal"] <= 400: tags.append("light")
    if r["veg"]: tags.append("veg")
    if r["mins"] <= 15: tags.append("quick")
    if r["serves"] >= 4: tags.append("prep")
    if r.get("sweet"): tags.append("sweet")
    if not r.get("cuisine") or not r.get("pro"):
        missing.append((r["id"], "cuisine/pro"))
    out.append({k: r[k] for k in ("id", "name", "meal", "mins", "serves", "cuisine", "pro") if k in r} |
               {"ing": [i[0] for i in r["ing"]], "ik": [i for i, x in enumerate(r["ing"]) if x[1]], "steps": r["steps"], **({"tip": r["tip"]} if r.get("tip") else {}), "n": n, "tags": tags})
if missing:
    raise SystemExit("Not in foods.json:\n" + "\n".join(f"  {a}: {b}" for a, b in missing))
json.dump({"source": "Original Fuel Log recipes. Nutrition computed from USDA SR26 and FNDDS values in foods.json; salt and spices not counted.",
           "recipes": out}, open(os.path.join(root, "recipes.json"), "w"), separators=(",", ":"), ensure_ascii=False)
ids = [r["id"] for r in out]
assert len(ids) == len(set(ids)), "duplicate recipe ids"
for r in out:
    n = r["n"]; print(f'{r["meal"]:9} {r["name"][:40]:40} {n["kcal"]:4} cal {n["p"]:5}p {n["c"]:5}c {n["f"]:5}f  {",".join(r["tags"])}')
print(len(out), "recipes")
