import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def rotate(v: np.ndarray, ang: float) -> np.ndarray:
    """Повертає вектор v на кут ang."""
    c, s = np.cos(ang), np.sin(ang)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1]])


def rot90(v: np.ndarray) -> np.ndarray:
    """Поворот вектора на +90°."""
    return np.array([-v[1], v[0]])


def make_square(bottom_left=(0.0, 0.0), side=1.0, theta=0.0) -> np.ndarray:
    """
    Створює квадрат як 4 точки у порядку:
    [ниж-ліво, ниж-право, верх-право, верх-ліво]
    """
    p0 = np.array(bottom_left, dtype=float)
    u = np.array([np.cos(theta), np.sin(theta)])          # напрям "вправо"
    v = rot90(u)                                          # напрям "вгору"
    p1 = p0 + u * side
    p2 = p1 + v * side
    p3 = p0 + v * side
    return np.vstack([p0, p1, p2, p3])


def square_on_segment(P: np.ndarray, Q: np.ndarray, third: np.ndarray) -> np.ndarray:
    """
    Будує квадрат на відрізку P->Q,
    !!!квадрат малюється з ПРОТИЛЕЖНОГО боку від точки third (щоб рости "назовні")!!!
    """
    d = Q - P
    L = float(np.linalg.norm(d))
    if L == 0:
        return None

    unit = d / L
    n = rot90(unit) * L  # перпендикуляр довжини L 

    # Визначаємо, з якого боку лежить third:
    # cross > 0 => third зліва; тоді квадрат треба будувати справа ->(міняємо знак n)
    cross = float(np.cross(d, third - P))
    if cross > 0:
        n = -n

    return np.vstack([P, Q, Q + n, P + n])


def pythagoras_tree(ax, square: np.ndarray, depth: int, alpha: float):
    """
    Рекурсивно малює дерево Піфагора.
    depth: скільки рівнів ще малювати
    alpha: кут (в радіанах), 0 < alpha < pi/2
    """
    if depth <= 0 or square is None:
        return

    # Малюємо поточний квадрат
    ax.add_patch(Polygon(square, closed=True, fill=False, linewidth=0.8))

    # Беремо верхню сторону квадрата: A (верх-ліво), B (верх-право)
    A = square[3]
    B = square[2]
    s = float(np.linalg.norm(B - A))
    if s == 0:
        return

    u = (B - A) / s  # одиничний вектор вздовж AB

    # Точка C — вершина прямокутного трикутника з гіпотенузою AB
    # AC = s*cos(alpha)
    C = A + rotate(u, alpha) * (s * np.cos(alpha))

    # Нові квадрати на катетах AC і CB 
    left_sq = square_on_segment(A, C, B)   # квадрат на AC
    right_sq = square_on_segment(C, B, A)  # квадрат на CB

    # Рекурсія
    pythagoras_tree(ax, left_sq, depth - 1, alpha)
    pythagoras_tree(ax, right_sq, depth - 1, alpha)


def main():
    try:
        depth = int(input("Вкажіть рівень рекурсії: ").strip())         # <- Вказуємо рівень рекурсії!!!! (норма від 1 до 12)
    except ValueError:
        depth = 10

    try:
        angle_deg = float(input("Вкажіть кут розгалуження в градусах: ").strip() or "45")     # 45' - оптимальний кут який я знайшов у прикладах Фрактала Піфагора
    except ValueError:
        angle_deg = 45.0

    # Обмеження, щоб не зламати геометрію
    angle_deg = max(1.0, min(89.0, angle_deg))
    alpha = np.deg2rad(angle_deg)

    # Початковий квадрат
    base = make_square(bottom_left=(-0.5, 0.0), side=1.0, theta=0.0)

    fig, ax = plt.subplots(figsize=(10, 8))
    pythagoras_tree(ax, base, depth, alpha)

    ax.set_aspect("equal")
    ax.axis("off")
    ax.relim()
    ax.autoscale_view()
    ax.set_title(f"Дерево Піфагора | depth={depth}, angle={angle_deg:.1f}°")
    plt.show()


if __name__ == "__main__":
    main()
