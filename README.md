# Anthropic IPO Trajectory

Data Science Society Project Labs project by Ada and Mia.

**Question:** how is Anthropic's stock likely to trade after its IPO? Think day-one pop, the first few months, and the lock-up expiry.

**Motivation:** we both bought into SpaceX's IPO (SPCX, June 2026). It popped about 19% on day one, ran up to roughly 50% above the IPO price, then gave most of that back. We'd like a better-informed guess this time.

## Context (as of 2026-10-27)
- Anthropic publicly filed its S-1 on 2026-10-26 to list on the Nasdaq as `ANT`.
- Its last private round (Series H, May 2026) valued it at $965B post-money. Reported IPO valuations range from $1.5T to $2T, but no price has been set yet.

## First result: what big tech IPOs did in their first year
Notebook: [`notebooks/01_comparables.ipynb`](notebooks/01_comparables.ipynb). These are 21 comparables, from Google (2004) to SpaceX (2026).

| horizon | median, bought at offer | median, bought at day-1 close | % losing (day-1 close) |
|---|---|---|---|
| 1 month | +36% | −1% | 52% |
| 6 months | +43% | −10% | 55% |
| 1 year | +41% | −10% | 60% |

The first-day pop goes to whoever got shares at the offer price. Buying at the end of day 1 has been roughly a coin flip, and slightly worse.
Caveat: this list is biased towards famous winners. The next step is to use every US IPO over $1B.

## Setup
```bash
uv sync                        # installs pandas, yfinance, matplotlib, jupyter
uv run jupyter lab             # open notebooks/01_comparables.ipynb
```
`src/ipo.py` holds the reusable functions: price paths indexed to the offer price, the split adjustment, and the summary table.
