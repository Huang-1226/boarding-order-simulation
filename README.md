# Boarding Order Simulation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23186759.svg)](https://doi.org/10.5281/zenodo.23186759)
[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://huang-1226.github.io/boarding-order-simulation/)

A computer simulation comparing four aircraft boarding strategies — **random**, **back-to-front**, **zoning** and a **strided-descending** order — together with an exact longest-path (max-plus) theory that explains them.

> Built as an independent research project (aviation operations / supply chain / mathematical modeling).

## Key Finding

Contrary to intuition, **back-to-front is the slowest** and **random already beats it** — and a **strided-descending** order (rows grouped by residue mod 6, each group boarded from the back) is **faster still**. The gaps widen as stow time and cabin size increase.

| Strategy | Boarding time (ticks) | Relative to random |
|---|---|---|
| Strided descending | 286.0 | 0.86 |
| Random | 331.1 | 1.00 |
| Zones (5) | 400.8 | 1.21 |
| Back-to-front | 627.0 | 1.89 |

*(R = 30 rows, 6 seats per row, S = 3 ticks; random/zoning averaged over 100 runs; strided-descending and back-to-front are deterministic)*

**Why?** Random spreads passengers across rows so many rows stow luggage **in parallel**; back-to-front makes the six passengers of a row stow **one after another**, under-using the aisle. The simulator measures this directly via **parallelism** (average passengers stowing at once: **1.26** strided-descending, 1.09 random, 0.90 zoning, **0.57** back-to-front). An exact **longest-path (max-plus) model** reproduces every boarding time bit-for-bit and shows that boarding so that passengers stop *before* the previous stower keeps the critical path short.

## Live Demo

**Online:** https://huang-1226.github.io/boarding-order-simulation/

Or open [`index.html`](index.html) in any browser — no installation, no internet required.
It shows an animated top-down cabin (four strategies side by side; passengers walk, stow, and sit down) together with an averaged statistics table. Adjust **rows (R)**, **stow time (S)**, **repeats**, and the **interleaved stride (k)** of the strided-descending strategy, then export the results as CSV.

*(You can enable GitHub Pages in the repository settings to host it as a website.)*

## Repository Structure

```
boarding-order-simulation/
├── index.html                 # Interactive web simulation
├── src/board_sim.py           # Simulation (tick-by-tick, in Python)
├── src/lpp_model.py           # Theory: longest-path / max-plus recurrence
├── data/results.csv           # Simulation results (tidy table)
├── data/results.xlsx          # Same results + charts
├── docs/Research_Report_Boarding_Optimization.pdf    # Full report (EN)
├── docs/Research_Report_Boarding_Optimization_ZH.pdf # Full report (中文)
└── LICENSE
```

## Model

- Single-aisle cabin; passengers enter from the front and walk to their row.
- On reaching the row, a passenger stows luggage, occupying the aisle for `STOW` ticks (followers cannot pass).
- Each passenger advances at most one cell per tick; no overtaking.
- One passenger enters per tick.
- Total ticks until everyone is seated = boarding time (smaller = faster).

## Running the Python Version

```bash
pip install matplotlib
python src/board_sim.py     # the simulation
python src/lpp_model.py     # the theory + self-check vs the simulation (no matplotlib needed)
```

## Theory: longest-path / max-plus model

`src/lpp_model.py` computes the same boarding time **without** simulating every tick, via a dynamic-programming recurrence. For a boarding order `r[i]` (target row of the i-th passenger), let `P[i][c]` be the tick passenger `i` reaches row `c`. Then

```
P[i][c] = max( P[i][c-1] + 1 , B[i][c] )
B[i][c] = P[j][c] + 1 + S   if r[j] == c   (person ahead stows at row c)
          P[j][c+1]         if r[j] >  c   (person ahead only passes through)
```

where `j` is the last passenger before `i` that reaches row `c`, and `S` is the stow time. Every `P[i][c]` is a max of two terms, so the total

```
T = max_i ( P[i][r[i]] + S - 1  (+1 if r[i] >= 2) )
```

is the length of the **longest chain of waits** — a longest-path (last-passage percolation) value. The model reproduces the simulation **bit-for-bit** (verified over tens of thousands of cases), which validates the theory and explains *why* strategies differ: **the boarding time is the longest chain of waits, and a good order spreads stowing across many rows while letting each passenger stop before the previous stower, keeping the critical path short.**

## Report

See [`docs/Research_Report_Boarding_Optimization.pdf`](docs/Research_Report_Boarding_Optimization.pdf) for the full English write-up (abstract, methods, results, discussion, limitations).

## License

MIT License — see [LICENSE](LICENSE).

## Author

Zihao Huang (Huang-1226)
