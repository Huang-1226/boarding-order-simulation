# Boarding Order Simulation

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23186760.svg)](https://doi.org/10.5281/zenodo.23186760)

A computer simulation comparing three aircraft boarding strategies — **random**, **back-to-front**, and **zoning** — and how their efficiency changes with stow time and cabin size.

> Built as an independent research project (aviation operations / supply chain / mathematical modeling).

## Key Finding

Contrary to intuition, **random boarding is the fastest** and **back-to-front is the slowest**, and the gap widens as stow time and the number of rows increase.

| Strategy | Boarding time (ticks) | Relative to random |
|---|---|---|
| Random | 331.9 | 1.00 |
| Zones (5) | 402.6 | 1.21 |
| Back-to-front | 627.0 | 1.89 |

*(R = 30 rows, STOW = 3 ticks, averaged over 20 runs)*

**Why?** Random boarding spreads passengers across rows so many rows stow luggage **in parallel**; back-to-front makes passengers of the same row stow **sequentially**, under-using the aisle. The model measures this directly: random shows the highest parallelism (≈1.09 passengers stowing at once) and the fewest blocking events (≈950), while back-to-front shows only ≈0.57 parallelism and ≈6,525 blocking events — i.e., the mechanism behind the time gap, not just the gap itself.

## Live Demo

Open [`index.html`](index.html) in any browser — no installation, no internet required.
Adjust rows / stow time / repeats, run the simulation, and export the results as CSV.

*(You can enable GitHub Pages in the repository settings to host it as a website.)*

## Repository Structure

```
boarding-order-simulation/
├── index.html                 # Interactive web simulation
├── src/board_sim.py           # Python version of the simulation
├── data/results.csv           # Simulation results (tidy table)
├── data/results.xlsx          # Same results + charts
├── docs/Research_Report_Boarding_Optimization.pdf   # Full report
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
python src/board_sim.py
```

## Report

See [`docs/Research_Report_Boarding_Optimization.pdf`](docs/Research_Report_Boarding_Optimization.pdf) for the full English write-up (abstract, methods, results, discussion, limitations).

## License

MIT License — see [LICENSE](LICENSE).

## Author

Zihao Huang (Huang-1226)
