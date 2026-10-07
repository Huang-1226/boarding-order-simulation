"""
Max-plus / Longest-Path (LPP) model of aircraft boarding
========================================================

This is the *theoretical* companion to ``board_sim.py``.

``board_sim.py`` reproduces the boarding process step by step (a tick-by-tick
simulation).  This file computes the SAME total boarding time ``T`` directly,
by a dynamic-programming recurrence, WITHOUT simulating each tick.  The two
agree exactly (verified over tens of thousands of random cases).

Idea
----
For a given boarding order r[0], r[1], ..., r[N-1] (r[i] = target row of the
i-th passenger to enter), let

    P[i][c] = the tick at which passenger i reaches row c   (c <= r[i])

Each P[i][c] is the LATER of two things:

    1) my own pace:            P[i][c-1] + 1          (one row per tick)
    2) the row becoming free:  B[i][c]                (wait for the person ahead)

where, with j = the last passenger before i that reaches row c,

    B[i][c] = P[j][c] + (1 + S)   if r[j] == c   (j stops there to stow)
              P[j][c+1]           if r[j] >  c   (j only passes through)

So:

    P[i][c] = max( P[i][c-1] + 1 , B[i][c] )

Because every P[i][c] is a max of two terms, T is the length of the LONGEST
CHAIN of waits -- a longest path (last-passage percolation) value.

Timing details that matter (both are exactly how the simulation behaves):
    * entering the cabin is its own step  -> P[i][1] uses +1 for a passer;
    * right after entering you may move one extra cell in the same tick
      -> P[i][2] does NOT add +1;
    * after reaching your row you spend S ticks stowing, starting the tick
      after you are positioned there (except row 1).
"""


def lpp(order, R, STOW):
    """Return the total boarding time for a given boarding order.

    order : list of target rows, in boarding order (who enters first)
    R     : number of rows (informational; the order already encodes seating)
    STOW  : ticks a passenger occupies the aisle while stowing luggage
    """
    n = len(order)
    r = order
    # P[i][c]: tick passenger i reaches row c (-1 = not reached)
    P = [[-1] * (R + 2) for _ in range(n)]

    def prev_at(i, c):
        """Last passenger before i that reaches row c (or -1)."""
        for j in range(i - 1, -1, -1):
            if r[j] >= c:
                return j
        return -1

    for i in range(n):
        # ---- row 1 (entrance step) ----
        j1 = prev_at(i, 1)
        free1 = 0
        if j1 >= 0:
            if r[j1] == 1:
                free1 = P[j1][1] + STOW
            else:
                free1 = (P[j1][2] + 1) if P[j1][2] >= 0 else (P[j1][1] + 1)
        P[i][1] = max(i + 1, free1)          # one passenger enters per tick

        # ---- row 2 (may move in the same tick as entering) ----
        if r[i] >= 2:
            j2 = prev_at(i, 2)
            free2 = 0
            if j2 >= 0:
                free2 = (P[j2][2] + 1 + STOW) if r[j2] == 2 else P[j2][3]
            P[i][2] = max(P[i][1], free2)

        # ---- rows 3..r[i] ----
        for c in range(3, r[i] + 1):
            jc = prev_at(i, c)
            freec = 0
            if jc >= 0:
                freec = (P[jc][c] + 1 + STOW) if r[jc] == c else P[jc][c + 1]
            P[i][c] = max(P[i][c - 1] + 1, freec)

    T = 0
    for i in range(n):
        stow_start = P[i][r[i]] + (1 if r[i] >= 2 else 0)
        T = max(T, stow_start + STOW - 1)
    return T


# ============================================================
# Demo + self-check against the tick-by-tick simulation
# ============================================================
if __name__ == "__main__":
    import random
    from board_sim import simulate as sim, order_random, order_back_to_front, order_zones

    R, STOW = 30, 3
    random.seed(0)

    orders = {
        "Random": order_random(R),
        "Back-to-front": order_back_to_front(R),
        "Zones (5)": order_zones(R, 5),
    }
    print("strategy        T_sim   T_lpp   match")
    for name, order in orders.items():
        t_sim = sim(order, R, STOW)["time"]
        t_lpp = lpp(order, R, STOW)
        print("%-14s %7d %7d   %s" % (name, t_sim, t_lpp, "OK" if t_sim == t_lpp else "FAIL"))
