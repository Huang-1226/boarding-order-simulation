"""
登机顺序优化模拟 (Boarding Order Optimization)
运行环境：Python 3 + matplotlib（推荐 Google Colab，浏览器直接跑）
"""

import random
import statistics

# ============================================================
# 模拟核心
# ============================================================
def simulate(order, R, STOW):
    """order: 乘客按登机顺序的 '目标排号' 列表。
    返回：总登机时间（tick 数），越小越快。"""
    n = len(order)
    aisle = [None] * (R + 3)      # 过道格，索引 = 排号
    target = list(order)
    nextp = 0                     # 下一个进舱的人
    seated = 0
    stow_left = {}                # 正在放行李的人 -> 剩余时间
    t = 0
    while seated < n:
        t += 1
        # 1) 机头放一个人进过道（若门口空）
        if nextp < n and aisle[1] is None:
            aisle[1] = nextp
            nextp += 1
        # 2) 乘客从后往前移动（先处理靠里的，方便填缝）
        for pos in range(R, 0, -1):
            p = aisle[pos]
            if p is None or p in stow_left:
                continue
            if target[p] == pos:          # 到座位 -> 开始放行李
                stow_left[p] = STOW
                continue
            if aisle[pos + 1] is None:    # 前面空就前进
                aisle[pos] = None
                aisle[pos + 1] = p
        # 3) 放行李计时，完成者坐下（离开过道）
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
    return t


# ============================================================
# 三种登机策略
# ============================================================
def order_random(R):
    """随机（自由座）"""
    seats = [r for r in range(1, R + 1) for _ in range(6)]
    random.shuffle(seats)
    return seats

def order_back_to_front(R):
    """从后往前：后排先登机"""
    return [r for r in range(R, 0, -1) for _ in range(6)]

def order_zones(R, nzones):
    """分区：后面的区先登机，区内随机"""
    zsize = R // nzones
    order = []
    for z in range(nzones, 0, -1):
        lo = (z - 1) * zsize + 1
        hi = z * zsize if z < nzones else R
        seats = [r for r in range(lo, hi + 1) for _ in range(6)]
        random.shuffle(seats)
        order += seats
    return order


# ============================================================
# 运行实验
# ============================================================
if __name__ == "__main__":
    R, STOW = 30, 3
    random.seed(0)

    rand_times = [simulate(order_random(R), R, STOW) for _ in range(20)]
    bf_time    = simulate(order_back_to_front(R), R, STOW)
    zone_times = [simulate(order_zones(R, 5), R, STOW) for _ in range(20)]

    print("随机      ：平均 %.1f tick" % statistics.mean(rand_times))
    print("从后往前  ：%d tick" % bf_time)
    print("分5区     ：平均 %.1f tick" % statistics.mean(zone_times))

    # 画柱状图
    import matplotlib.pyplot as plt
    labels = ["随机", "从后往前", "分5区"]
    vals = [statistics.mean(rand_times), bf_time, statistics.mean(zone_times)]
    plt.bar(labels, vals, color=["#cc0000", "#00aa00", "#0066cc"])
    plt.ylabel("登机总时间 (tick)")
    plt.title("不同登机策略对比")
    for i, v in enumerate(vals):
        plt.text(i, v, "%.1f" % v, ha="center", va="bottom")
    plt.show()
