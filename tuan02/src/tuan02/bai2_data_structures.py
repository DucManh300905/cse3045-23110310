import random
import timeit
 
SIZE = 100_000
 
 
def find_common_nested(list_a, list_b):
    """Hai vòng lặp lồng nhau: O(n^2)."""
    result = []
    for item_a in list_a:
        for item_b in list_b:
            if item_a == item_b:
                result.append(item_a)
                break
    return result
 
 
def find_common_set(list_a, list_b):
    """Dùng set: O(n) trung bình."""
    set_b = set(list_b)
    return [item for item in list_a if item in set_b]
 
 
def make_data(n, seed=42):
    """Hai list n phần tử, lấy từ range(2n) nên có khoảng n/2 phần tử chung."""
    rng = random.Random(seed)
    return rng.sample(range(2 * n), n), rng.sample(range(2 * n), n)
 
 
def bench(func, a, b, repeat, number):
    """Thời gian mỗi lần gọi, lấy giá trị nhỏ nhất qua `repeat` lần đo."""
    times = timeit.repeat(lambda: func(a, b), repeat=repeat, number=number)
    return min(times) / number
 
 
def main():
    # 1) Kiểm tra tính đúng đắn (dữ liệu có nhiều phần tử chung).
    for n in (100, 1_000, 3_000):
        a, b = make_data(n)
        r_nested = find_common_nested(a, b)
        r_set = find_common_set(a, b)
        assert r_nested == r_set
        print(f"[OK] n={n:>5,}: giống nhau, {len(r_set):,} phần tử chung")
 
    # 2) Đo nested ở nhiều kích thước để thấy xu hướng O(n^2) và O(n).
    print("\nn        nested (s)   set (s)      speedup")
    last = None
    for n in (1_000, 2_000, 4_000, 8_000):
        a, b = make_data(n)
        t_nested = bench(find_common_nested, a, b, repeat=3, number=1)
        t_set = bench(find_common_set, a, b, repeat=5, number=20)
        last = (n, t_nested)
        print(f"{n:<8,} {t_nested:<12.6f} {t_set:<12.6f} x{t_nested / t_set:,.0f}")
 
    # 3) Đo set ở đúng kích thước đề bài: 100.000 phần tử.
    a, b = make_data(SIZE)
    t_set_full = bench(find_common_set, a, b, repeat=5, number=5)
    print(f"\nset ở n={SIZE:,}: {t_set_full:.6f} s "
          f"({len(find_common_set(a, b)):,} phần tử chung)")
 
    # 4) Ước tính nested ở 100.000 bằng cách ngoại suy bậc 2 (đây là ước tính).
    n0, t0 = last
    est = t0 * (SIZE / n0) ** 2
    print(f"nested ở n={SIZE:,} (ước tính, ngoại suy n^2 từ n={n0:,}): "
          f"{est:,.1f} s ≈ {est / 60:.1f} phút")
    print(f"speedup ước tính ở n={SIZE:,}: x{est / t_set_full:,.0f}")
 
 
if __name__ == "__main__":
    main()
 