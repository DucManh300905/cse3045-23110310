import random
import timeit


SIZE = 100_000


def find_common_nested(list_a, list_b):
    """Find common elements using nested loops: O(n²)."""
    result = []

    for item_a in list_a:
        for item_b in list_b:
            if item_a == item_b:
                result.append(item_a)
                break

    return result


def find_common_set(list_a, list_b):
    """Find common elements using a set: O(n) average."""
    set_b = set(list_b)

    return [item for item in list_a if item in set_b]


def main():
    random.seed(42)

    list_a = random.sample(range(SIZE * 2), SIZE)
    list_b = random.sample(range(SIZE * 2), SIZE)

    # Check correctness on a smaller sample.
    test_a = list_a[:1_000]
    test_b = list_b[:1_000]

    result_nested = find_common_nested(test_a, test_b)
    result_set = find_common_set(test_a, test_b)

    assert result_nested == result_set

    print("Kiểm tra kết quả: hai phương pháp cho kết quả giống nhau.")

    # Benchmark the nested-loop method on a smaller input.
    # The algorithm is still O(n²), but using 1,000 elements
    # keeps the benchmark practical on a normal computer.
    benchmark_a = list_a[:1_000]
    benchmark_b = list_b[:1_000]

    nested_timer = timeit.Timer(
        lambda: find_common_nested(benchmark_a, benchmark_b)
    )

    set_timer = timeit.Timer(
        lambda: find_common_set(benchmark_a, benchmark_b)
    )

    time_nested = nested_timer.timeit(number=1)
    time_set = set_timer.timeit(number=1)

    speedup = time_nested / time_set

    print("\n=== KẾT QUẢ TIMEIT ===")
    print(f"Kích thước dữ liệu thực tế: {SIZE:,} phần tử/list")
    print("Kích thước benchmark: 1,000 phần tử/list")
    print(f"Nested loops O(n²): {time_nested:.6f} giây")
    print(f"Set O(n):           {time_set:.6f} giây")
    print(f"Speedup:             {speedup:.2f} lần")


if __name__ == "__main__":
    main()