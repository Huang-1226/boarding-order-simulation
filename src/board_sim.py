"""
Boarding Order Simulation
Environment: Python 3 + matplotlib

Simulates three boarding strategies (random / back-to-front / zoning) on a
single-aisle cabin and, importantly, records MECHANISM metrics:
  - average number of passengers stowing luggage at the same time (parallelism)
  - total number of blocking events (a passenger blocked by someone stowing)
These explain WHY one strategy is faster than another (not just that it is).
"""

import random
import statistics


def simulate(order, R, STOW):
    """Run one boarding simulation.

    order : list of target rows, in boarding order (who enters first)
    R     : number of rows (6 seats per row)
    STOW  : ticks a passenger occupies the aisle while stowing luggage

    Returns a dict with: time, avg_concurrent, total_blocked, blocked_per_pax.
    """
    n = len(order)
    aisle = [None] * (R + 3)      # aisle[cell] = passenger id occupying that row-cell
    target = list(order)
    nextp = 0                     # next passenger to enter
    seated = 0
    stow_left = {}                # passenger id -> remaining stow ticks
    t = 0
    sum_conc = 0                  # accumulate concurrent stowers per tick
    total_blocked = 0             # accumulate blocking events

    while seated < n:
        t += 1
        # 1) Let one passenger enter at the front if the door cell is free
        if nextp < n and aisle[1] is None:
            aisle[1] = nextp
            nextp += 1

        blocked = 0
        # 2) Move passengers toward their row (scan from back to front)
        for pos in range(R, 0, -1):
            p = aisle[pos]
            if p is None or p in stow_left:
                continue
            if target[p] == pos:          # reached row -> start stowing
                stow_left[p] = STOW
                continue
            if aisle[pos + 1] is None:    # free ahead -> advance one cell
                aisle[pos] = None
                aisle[pos + 1] = p
            else:                         # blocked by the person ahead
                blocked += 1

        # 3) Tick down stow timers; finished passengers sit down (leave aisle)
        done = []
        for p in list(stow_left):
            stow_left[p] -= 1
            if stow_left[p] <= 0:
                done.append(p)
        for p in done:
            for pos in range(1, R + 1):
                if aisle[pos] == p:
                    aisle[pos] = None
                    break
            del stow_left[p]
            seated += 1

        # 4) Record mechanism metrics for this tick
        sum_conc += len(stow_left)        # how many stow in parallel
        total_blocked += blocked          # how many are stuck waiting

    return {
        "time": t,
        "avg_concurrent": sum_conc / t,
        "total_blocked": total_blocked,
        "blocked_per_pax": total_blocked / n,
    }


# ============================================================
# Boarding strategies
# ============================================================
def order_random(R):
    """Random (free seating)."""
    seats = [r for r in range(1, R + 1) for _ in range(6)]
    random.shuffle(seats)
    return seats


def order_back_to_front(R):
    """Back-to-front: rear rows board first."""
    return [r for r in range(R, 0, -1) for _ in range(6)]


def order_zones(R, nzones):
    """Zoning: board the rearmost zone first, random within each zone."""
    zsize = R // nzones
    order = []
    for z in range(nzones, 0, -1):
        lo = (z - 1) * zsize + 1
        hi = z * zsize if z < nzones else R
        seats = [r for r in range(lo, hi + 1) for _ in range(6)]
        random.shuffle(seats)
        order += seats
    return order


def _avg(results, key):
    return statistics.mean(r[key] for r in results)


# ============================================================
# Run experiment
# ============================================================
if __name__ == "__main__":
    R, STOW, N = 30, 3, 20
    random.seed(0)

    rand = [simulate(order_random(R), R, STOW) for _ in range(N)]
    bf = [simulate(order_back_to_front(R), R, STOW)]
    zone = [simulate(order_zones(R, 5), R, STOW) for _ in range(N)]

    rows = [("Random", rand), ("Back-to-front", bf), ("Zones (5)", zone)]
    print("%-14s %10s %18s %16s" % ("Strategy", "Time", "Avg concurrent", "Total blocked"))
    for name, res in rows:
        print("%-14s %10.1f %18.2f %16.0f" % (
            name, _avg(res, "time"), _avg(res, "avg_concurrent"), _avg(res, "total_blocked")))

    import matplotlib.pyplot as plt
    labels = [n for n, _ in rows]
    times = [_avg(res, "time") for _, res in rows]
    concs = [_avg(res, "avg_concurrent") for _, res in rows]

    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    ax[0].bar(labels, times, color=["#cc4444", "#22a352", "#1f6fb2"])
    ax[0].set_ylabel("Boarding time (ticks)")
    ax[0].set_title("Boarding time by strategy")
    for i, v in enumerate(times):
        ax[0].text(i, v, "%.1f" % v, ha="center", va="bottom")

    ax[1].bar(labels, concs, color=["#cc4444", "#22a352", "#1f6fb2"])
    ax[1].set_ylabel("Avg concurrent stowers")
    ax[1].set_title("Parallelism by strategy")
    for i, v in enumerate(concs):
        ax[1].text(i, v, "%.2f" % v, ha="center", va="bottom")

    fig.tight_layout()
    plt.show()
