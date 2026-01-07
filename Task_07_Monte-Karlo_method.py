import random
from collections import Counter
import matplotlib.pyplot as plt

def simulate_two_dice(n_rolls: int, seed: int | None = None):
    if seed is not None:
        random.seed(seed)

    sums = []
    for _ in range(n_rolls):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        sums.append(d1 + d2)

    counts = Counter(sums)

    # Аналітичний розподіл
    ways = {2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:5, 9:4, 10:3, 11:2, 12:1}

    results = []
    for s in range(2, 13):
        mc_p = counts[s] / n_rolls
        an_p = ways[s] / 36
        results.append((s, counts[s], mc_p, an_p, mc_p - an_p))

    return results

def print_table(results):
    print(f"{'Сума':>4} | {'К-сть (MC)':>10} | {'MC %':>8} | {'Аналіт. %':>10} | {'Різниця %':>10}")
    print("-" * 60)
    for s, c, mc_p, an_p, diff in results:
        print(f"{s:>4} | {c:>10} | {mc_p*100:>7.3f}% | {an_p*100:>9.3f}% | {diff*100:>9.3f}%")

def plot_results(results, n_rolls):
    x = [r[0] for r in results]
    y_mc = [r[2] for r in results]
    y_an = [r[3] for r in results]

    plt.figure(figsize=(9, 4.5))
    plt.plot(x, y_mc, marker="o", label="Монте-Карло")
    plt.plot(x, y_an, marker="o", label="Аналітичні")
    plt.xticks(x)
    plt.xlabel("Сума")
    plt.ylabel("Ймовірність")
    plt.title(f"Розподіл сум двох кубиків (N={n_rolls:,})")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    N = 200_000      
    results = simulate_two_dice(N, seed=42)

    print_table(results)

    max_abs_diff = max(abs(r[4]) for r in results)
    print(f"\nМаксимальне відхилення: {max_abs_diff*100:.3f}%")

    plot_results(results, N)

if __name__ == "__main__":
    main()
