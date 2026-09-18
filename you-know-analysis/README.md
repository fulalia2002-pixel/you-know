# you-know in Human–AI Interaction: Statistical Consistency Checks

Reproducible statistical checks for the paper *Variation in Pragmatic Markers
in Human–AI vs. Human–Human Textual Interaction*.

## Contents

- `analysis.py` — verifies the internal consistency of the mixed-effects
  logistic regression table reported in the paper: recomputes z = beta / SE,
  OR = exp(beta), and 95% CI = exp(beta ± 1.96·SE) for every fixed effect,
  and recomputes the descriptive statistics (raw rate reduction vs. adjusted
  odds reduction).
- `results.json` — the output of `analysis.py` (generated).

## Model

The reported model is a mixed-effects logistic regression fitted with
`lme4::glmer` in R 4.3.2 (binomial family, logit link):

```
logit(P(you know)) = beta0 + beta1 Interlocutor + beta2 Function
  + beta3 (Interlocutor × Function) + beta4 Age + beta5 Gender
  + beta6 AI_familiarity + beta7 Clause_type + beta8 Position
  + beta9 Preceding_pause + beta10 Turn_length + beta11 Speech_act
  + u_Speaker + u_Topic + (1 + Interlocutor | Speaker)
```

This repository does **not** re-estimate the model (which requires the raw
corpus); it checks that the reported coefficients are arithmetically
consistent. The corpus is not redistributed.

## Key checks

- Interlocutor effect: β = −1.18, SE = 0.17 → z = −6.94, OR = 0.307,
  95% CI [0.22, 0.43].
- Raw rate reduction: (11.8 − 4.3) / 11.8 = 63.6%.
- Adjusted odds reduction: 1 − 0.307 = 69.3%.

## Run

```bash
python analysis.py
```

Requires Python 3.9+ (standard library only).
