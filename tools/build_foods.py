#!/usr/bin/env python3
"""Add USDA FNDDS survey foods to foods.json.

FNDDS (Food and Nutrient Database for Dietary Studies) is the database USDA uses
for "What We Eat in America". It covers mixed dishes and foods as people
actually eat them ("Burrito with chicken, beans, and cheese", "Pizza, pepperoni,
from restaurant or fast food, thin crust"), with household portions for each.
It is public domain.

Usage:
    python3 tools/build_foods.py SURVEY_JSON_OR_ZIP [foods.json]

The SR26 rows already in foods.json are kept as they are, and the FNDDS rows are
added after them. Re-running replaces the earlier FNDDS rows, so it's safe to run
again when USDA publishes a new release.
"""
import json
import re
import sys
import zipfile

# FoodData Central nutrient numbers
N_KCAL, N_KCAL_ATWATER, N_PROT, N_CARB, N_FAT, N_FIBER, N_SUGAR, N_SODIUM = \
    "208", "957", "203", "205", "204", "291", "269", "307"

# WWEIA categories that aren't useful to an adult food log
SKIP_CATEGORY = re.compile(r"baby food|infant formula|human milk", re.I)

UNIT_FIX = [
    (r"\btablespoons?\b", "tbsp"), (r"\bteaspoons?\b", "tsp"),
    (r"\bfluid ounces?\b", "fl oz"), (r"\bounces?\b", "oz"),
]


def load_survey(path):
    if path.endswith(".zip"):
        with zipfile.ZipFile(path) as z:
            name = next(n for n in z.namelist() if n.endswith(".json"))
            data = json.loads(z.read(name))
    else:
        with open(path) as f:
            data = json.load(f)
    for key in ("SurveyFoods", "surveyFoods", "FoodData"):
        if key in data:
            return data[key]
    if isinstance(data, list):
        return data
    raise SystemExit("Couldn't find the food list in %s (keys: %s)" % (path, list(data)[:5]))


def clean_name(desc):
    """'Chicken breast, baked, NS as to skin eaten' -> 'Chicken breast, baked'.
    'NFS' means 'not further specified', i.e. the generic version, so it's dropped too."""
    parts = [p.strip() for p in desc.split(",")]
    keep = [p for p in parts if p and p != "NFS" and not re.match(r"^NS as to\b", p)]
    name = ", ".join(keep) or desc.strip()
    return re.sub(r"\s+", " ", name)


def to_num(s):
    s = s.strip()
    m = re.match(r"^(\d+)[-\s](\d+)/(\d+)$", s)
    if m:
        return int(m[1]) + int(m[2]) / int(m[3])
    m = re.match(r"^(\d+)/(\d+)$", s)
    if m:
        return int(m[1]) / int(m[2])
    return float(s)


def parse_portion(desc, grams):
    """'1 cup, chopped' -> [1, 'cup, chopped', g];  'Quantity not specified' -> [1, 'serving', g]"""
    d = re.sub(r"\s+", " ", (desc or "").strip())
    if not d or grams is None or grams <= 0:
        return None
    if re.match(r"(?i)^quantity not specified", d):
        return [1, "serving", round(grams, 1)]
    if re.match(r"(?i)^guideline amount", d):
        return None
    m = re.match(r"^(\d+[-\s]\d+/\d+|\d+/\d+|\d*\.\d+|\d+)\s+(.+)$", d)
    if not m:
        return [1, d[:40], round(grams, 1)]
    amt, unit = to_num(m[1]), m[2]
    # keep short size notes like "(8 fl oz)", drop long ones like '(2-1/4" to 3" dia)'
    unit = re.sub(r"\s*\(([^)]*)\)", lambda p: " (" + p[1] + ")" if len(p[1]) <= 12 else "", unit).strip()
    for pat, rep in UNIT_FIX:
        unit = re.sub(pat, rep, unit, flags=re.I)
    if amt <= 0:
        return None
    return [round(amt, 3), unit[:40], round(grams, 1)]


def nutrients(food):
    out = {}
    for fn in food.get("foodNutrients", []):
        n = fn.get("nutrient") or {}
        num = str(n.get("number") or fn.get("nutrientNumber") or "")
        amt = fn.get("amount", fn.get("value"))
        if num and amt is not None:
            out[num] = float(amt)
    return out


def r1(x):
    return None if x is None else round(x, 1)


def convert(foods):
    rows, seen, skipped = [], set(), {"category": 0, "no_energy": 0, "duplicate": 0}
    for f in foods:
        cat = (f.get("wweiaFoodCategory") or {}).get("wweiaFoodCategoryDescription", "")
        if SKIP_CATEGORY.search(cat):
            skipped["category"] += 1
            continue
        nu = nutrients(f)
        kcal = nu.get(N_KCAL, nu.get(N_KCAL_ATWATER))
        if kcal is None:
            skipped["no_energy"] += 1
            continue
        name = clean_name(f.get("description", ""))
        key = norm(name)
        if key in seen:
            skipped["duplicate"] += 1
            continue
        seen.add(key)
        portions = sorted(f.get("foodPortions", []), key=lambda p: p.get("sequenceNumber") or 99)
        ms, mseen = [], set()
        for p in portions:
            m = parse_portion(p.get("portionDescription") or p.get("modifier"), p.get("gramWeight"))
            if m and (m[0], m[1].lower()) not in mseen:
                mseen.add((m[0], m[1].lower()))
                ms.append(m)
        sodium = nu.get(N_SODIUM)
        rows.append([
            name, "", round(kcal, 1), r1(nu.get(N_PROT, 0.0)), r1(nu.get(N_CARB, 0.0)), r1(nu.get(N_FAT, 0.0)),
            r1(nu.get(N_FIBER)), r1(nu.get(N_SUGAR)), None if sodium is None else round(sodium), ms[:8],
        ])
    return rows, skipped


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", s.lower())).strip()


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    src, out_path = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "foods.json")
    with open(out_path) as f:
        db = json.load(f)

    base_n = (db.get("counts") or {}).get("sr26", len(db["foods"]))
    base = db["foods"][:base_n]
    base_names = {norm(r[0]) for r in base}

    survey = load_survey(src)
    rows, skipped = convert(survey)
    new = [r for r in rows if norm(r[0]) not in base_names]
    skipped["already_in_sr26"] = len(rows) - len(new)
    new.sort(key=lambda r: r[0].lower())

    if len(new) < 1000:
        raise SystemExit("Only %d foods converted. The USDA file format may have changed; not writing." % len(new))

    release = re.search(r"(\d{4}-\d{2}-\d{2})", src)
    db["source"] = ("USDA National Nutrient Database for Standard Reference, Release 26, and USDA Food and Nutrient "
                    "Database for Dietary Studies (FNDDS%s, FoodData Central survey foods). Public domain. Values per 100 g."
                    % (", " + release[1] if release else ""))
    db["counts"] = {"sr26": len(base), "fndds": len(new)}
    db["foods"] = base + new

    with open(out_path, "w") as f:
        json.dump(db, f, separators=(",", ":"), ensure_ascii=False)
    print("SR26 foods kept:  %d" % len(base))
    print("FNDDS foods added: %d" % len(new))
    print("Skipped:", json.dumps(skipped))


if __name__ == "__main__":
    main()
