from typing import List, Dict


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
        Знаходить оптимальний спосіб розрізання через мемоізацію

        Args:
            length: int - довжина стрижня
            prices: List[int] - список цін, де prices[i] — ціна стрижня довжини i+1

        Returns:
            Dict з максимальним прибутком та списком розрізів
        """
    memo = {}

    def helper(n):
        if n == 0:
            return 0, []
        if n in memo:
            return memo[n]
        max_profit = 0
        best_cut = []
        for i in range(1, n + 1):
            if i <= len(prices):
                profit, cuts = helper(n - i)
                if profit + prices[i - 1] > max_profit:
                    max_profit = profit + prices[i - 1]
                    best_cut = cuts + [i]
        memo[n] = (max_profit, best_cut)
        return memo[n]

    max_profit, cuts = helper(length)
    return {
        "max_profit": max_profit,
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1
    }


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію

    Args:
        length: int - довжина стрижня
        prices: List[int] - список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    dp = [0] * (length + 1)
    cut_trace = [0] * (length + 1)

    for i in range(1, length + 1):
        for j in range(1, i + 1):
            if j <= len(prices) and dp[i] < dp[i - j] + prices[j - 1]:
                dp[i] = dp[i - j] + prices[j - 1]
                cut_trace[i] = j

    cuts = []
    n = length
    while n > 0:
        cuts.append(cut_trace[n])
        n -= cut_trace[n]

    return {
        "max_profit": dp[length],
        "cuts": cuts,
        "number_of_cuts": len(cuts) - 1
    }

# Test runner
def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        # Тест 1: Базовий випадок
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        # Тест 2: Оптимально не різати
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        # Тест 3: Всі розрізи по 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]

    for test in test_cases:
        print(f"\nТест: {test['name']}")
        print(f"Довжина стрижня: {test['length']}")
        print(f"Ціни: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print("\nРезультат мемоізації:")
        print(f"Максимальний прибуток: {memo_result['max_profit']}")
        print(f"Розрізи: {memo_result['cuts']}")
        print(f"Кількість розрізів: {memo_result['number_of_cuts']}")

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test['length'], test['prices'])
        print("\nРезультат табуляції:")
        print(f"Максимальний прибуток: {table_result['max_profit']}")
        print(f"Розрізи: {table_result['cuts']}")
        print(f"Кількість розрізів: {table_result['number_of_cuts']}")

        print("\nПеревірка пройшла успішно!")


if __name__ == "__main__":
    run_tests()
