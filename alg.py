from database import get_banknotes, update_banknotes

def greedy_cash_withdrawal(banknotes, amount):
    """
    Жадный алгоритм для выдачи денег с учетом доступного количества купюр.
    """
    result = []
    remaining = amount
    updated_banknotes = {denomination: quantity for denomination, quantity in banknotes}

    for denomination, quantity in sorted(banknotes, key=lambda x: -x[0]):
        if remaining == 0:
            break
        count = min(remaining // denomination, quantity)
        if count > 0:
            result.extend([denomination] * count)
            remaining -= count * denomination
            updated_banknotes[denomination] -= count

    if remaining != 0:
        return "Невозможно выдать запрошенную сумму с текущими купюрами"

    # Обновляем состояние банкомата
    update_banknotes(updated_banknotes)
    return sorted(result, reverse=True)

def dp_cash_withdrawal(banknotes, amount):
    """
    Метод динамического программирования для выдачи денег с учетом доступного количества купюр.
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    coin_used = [-1] * (amount + 1)
    updated_banknotes = {denomination: quantity for denomination, quantity in banknotes}

    for denomination, quantity in banknotes:
        for i in range(denomination, amount + 1):
            if dp[i - denomination] + 1 < dp[i] and updated_banknotes[denomination] > 0:
                dp[i] = dp[i - denomination] + 1
                coin_used[i] = denomination

    if dp[amount] == float('inf'):
        return "Невозможно выдать запрошенную сумму с текущими купюрами"

    result = []
    remaining = amount
    while remaining > 0:
        coin = coin_used[remaining]
        if coin == -1 or updated_banknotes[coin] <= 0:
            return "Невозможно выдать запрошенную сумму с текущими купюрами"
        result.append(coin)
        remaining -= coin
        updated_banknotes[coin] -= 1

    # Обновляем состояние банкомата
    update_banknotes(updated_banknotes)
    return sorted(result, reverse=True)

def cash_withdrawal(amount):
    if amount <= 0:
        raise ValueError("Сумма должна быть положительным числом")
    """
    Основная функция для выбора метода выдачи денег.
    """
    banknotes = get_banknotes()

    # Проверяем, можно ли использовать жадный алгоритм
    can_use_greedy = True
    for i in range(len(banknotes) - 1):
        if banknotes[i + 1][0] % banknotes[i][0] != 0:
            can_use_greedy = False
            break

    if can_use_greedy:
        return greedy_cash_withdrawal(banknotes, amount)
    else:
        return dp_cash_withdrawal(banknotes, amount)