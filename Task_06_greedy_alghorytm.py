from typing import Dict, List, Tuple

items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
}


def greedy_algorithm(items: Dict[str, Dict[str, int]], budget: int) -> Tuple[List[str], int, int]:
    """
    Жадібний алгоритм: сортуємо за calories/cost (співвідношенням),
    потім беремо по черзі, якщо влазить у бюджет.
    """
    ranked = sorted(
        items.items(),
        key=lambda kv: kv[1]["calories"] / kv[1]["cost"],
        reverse=True
    )

    chosen: List[str] = []
    total_cost = 0
    total_calories = 0
    remaining = budget

    for name, info in ranked:
        c = info["cost"]
        cal = info["calories"]
        if c <= remaining:
            chosen.append(name)
            total_cost += c
            total_calories += cal
            remaining -= c

    return chosen, total_cost, total_calories


def dynamic_programming(items: Dict[str, Dict[str, int]], budget: int) -> Tuple[List[str], int, int]:
    """
    Динамічне програмування:
    dp[b] = максимум калорій при бюджеті b.
    """
    names = list(items.keys())
    n = len(names)

    # dp[i][b] = max calories
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name = names[i - 1]
        cost = items[name]["cost"]
        cal = items[name]["calories"]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]       # не беремо item
            if cost <= b:
                dp[i][b] = max(dp[i][b], dp[i - 1][b - cost] + cal)

    # Відновлення відповіді
    chosen: List[str] = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            name = names[i - 1]
            chosen.append(name)
            b -= items[name]["cost"]

    chosen.reverse()
    total_cost = sum(items[name]["cost"] for name in chosen)
    total_calories = dp[n][budget]
    return chosen, total_cost, total_calories


if __name__ == "__main__":
    budget = 100

    g_items, g_cost, g_cal = greedy_algorithm(items, budget)
    d_items, d_cost, d_cal = dynamic_programming(items, budget)

    print(f"Бюджет: {budget}\n")

    print("Greedy:")
    print("  chosen:", g_items)
    print("  total cost:", g_cost)
    print("  total calories:", g_cal)

    print("\nDP (optimal):")
    print("  chosen:", d_items)
    print("  total cost:", d_cost)
    print("  total calories:", d_cal)

# Greedy швидкий і простий, але не гарантує оптимальність.
# DP гарантує оптимальний набір за калорійністю в межах бюджету.
