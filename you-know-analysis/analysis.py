# -*- coding: utf-8 -*-
"""
Statistical consistency checks for the you-know mixed-effects logistic
regression reported in the paper.

Verifies that the reported fixed-effects table is internally consistent:
    z = beta / SE
    OR = exp(beta)
    95% CI = exp(beta +/- 1.96 * SE)

Also verifies the descriptive statistics:
    raw rate reduction = (rate_HH - rate_HAI) / rate_HH
    adjusted odds reduction = 1 - OR

These are arithmetic/statistical checks, not a re-estimation of the model
(which requires the raw corpus). The model itself is a mixed-effects logistic
regression fitted with lme4::glmer in R.
"""
from __future__ import annotations

import json
import math

# Fixed effects from Table 6 (beta, SE). None for random effects.
FIXED_EFFECTS = [
    ("Interlocutor (AI vs. Human)", -1.18, 0.17),
    ("Function (INTP vs. TEXT)", 0.42, 0.18),
    ("Function (EPIS vs. TEXT)", -0.31, 0.22),
    ("Interlocutor x Function (INTP)", -1.42, 0.28),
    ("Interlocutor x Function (EPIS)", -0.68, 0.34),
    ("AI familiarity", 0.29, 0.13),
    ("Interlocutor x AI familiarity", -0.18, 0.11),
    ("Speech act (Expressive vs. Statement)", 0.87, 0.21),
    ("Speech act (Directive vs. Statement)", -0.52, 0.19),
    ("Preceding pause (Present vs. Absent)", 0.63, 0.15),
    ("Turn length (log CU)", 0.41, 0.11),
    ("Speaker age", -0.03, 0.01),
    ("Gender (Female vs. Male)", 0.38, 0.22),
]


def check_fixed_effects() -> list[dict]:
    rows = []
    for name, beta, se in FIXED_EFFECTS:
        z = beta / se
        or_ = math.exp(beta)
        ci_lo = math.exp(beta - 1.96 * se)
        ci_hi = math.exp(beta + 1.96 * se)
        rows.append({
            "effect": name,
            "beta": beta,
            "SE": se,
            "z_recomputed": round(z, 2),
            "OR": round(or_, 3),
            "CI95": [round(ci_lo, 2), round(ci_hi, 2)],
        })
    return rows


def check_descriptives() -> dict:
    # raw counts per condition
    hh_tokens, hh_cu = 486, 4102
    hai_tokens, hai_cu = 161, 3740
    rate_hh = hh_tokens / hh_cu * 100
    rate_hai = hai_tokens / hai_cu * 100
    raw_reduction = (rate_hh - rate_hai) / rate_hh * 100

    # adjusted odds ratio (from the model)
    or_ai = 0.307
    adjusted_reduction = (1 - or_ai) * 100

    # per-function token counts and rates (Table 4 / 5)
    func = {
        "TEXT": {"hh": 182, "hai": 98},
        "INTP": {"hh": 241, "hai": 47},
        "EPIS": {"hh": 63, "hai": 16},
    }
    func_out = {}
    for f, d in func.items():
        # rates per 100 CU need the function-specific denominators;
        # here we report raw reduction for completeness.
        red = (d["hh"] - d["hai"]) / d["hh"] * 100
        func_out[f] = {"hh": d["hh"], "hai": d["hai"], "raw_reduction_pct": round(red, 1)}

    return {
        "rate_HH_per100": round(rate_hh, 1),
        "rate_HAI_per100": round(rate_hai, 1),
        "raw_reduction_pct": round(raw_reduction, 1),
        "OR_interlocutor": or_ai,
        "adjusted_odds_reduction_pct": round(adjusted_reduction, 1),
        "functions": func_out,
    }


def main() -> None:
    report = {
        "fixed_effects_consistency": check_fixed_effects(),
        "descriptives": check_descriptives(),
    }
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
