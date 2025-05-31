import pytest
from alg import greedy_cash_withdrawal, dp_cash_withdrawal, cash_withdrawal
from database import get_banknotes, reset_banknotes

class TestPositiveCases:
    """Позитивное тестирование - проверка работы алгоритма на типовых наборах данных"""
    
    def test_repeating_denominations(self):
        """a) Купюры с повторяющимися номиналами"""
        banknotes = [(100, 5), (100, 5), (50, 3)]  # Дублирование номинала 100
        amount = 250
        result = cash_withdrawal(amount)
        assert sum(result) == amount

    def test_multiple_solutions(self):
        """b) Случаи с несколькими вариантами выдачи"""
        banknotes = [(500, 2), (200, 5), (100, 10)]
        amount = 1000
        result = cash_withdrawal(amount)
        assert sum(result) == amount

    def test_minimal_denominations(self):
        """c) Минимальное количество купюр"""
        banknotes = [(5000, 1), (1000, 1)]
        amount = 6000
        result = cash_withdrawal(amount)
        assert sorted(result) == [1000, 5000]

class TestBoundaryCases:
    """Анализ граничных условий - тестирование поведения в крайних случаях"""
    
    def test_empty_atm(self):
        """a) Пустой банкомат"""
        reset_banknotes()
        # Удаляем все купюры для теста
        conn = sqlite3.connect("atm.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM banknotes")
        conn.commit()
        conn.close()
        
        amount = 100
        result = cash_withdrawal(amount)
        assert result == "Невозможно выдать запрошенную сумму с текущими купюрами"

    def test_single_denomination(self):
        """b) Банкомат с одним номиналом"""
        banknotes = [(100, 10)]
        amount = 300
        result = dp_cash_withdrawal(banknotes, amount)
        assert result == [100, 100, 100]

    def test_zero_amount(self):
        """c) Запрос нулевой суммы"""
        with pytest.raises(ValueError, match="Сумма должна быть положительным числом"):
            cash_withdrawal(0)

class TestNegativeCases:
    """Негативное тестирование - проверка устойчивости к невалидным данным"""
    
    def test_invalid_amount_type(self):
        """a) Некорректный тип суммы (строка вместо числа)"""
        with pytest.raises(TypeError):
            cash_withdrawal("100")  # type: ignore

    def test_negative_amount(self):
        """b) Отрицательная сумма"""
        with pytest.raises(ValueError, match="Сумма должна быть положительным числом"):
            cash_withdrawal(-500)

    def test_insufficient_funds(self):
        """c) Недостаточно средств в банкомате"""
        reset_banknotes()
        amount = 1000000  # Сумма больше, чем есть в банкомате
        result = cash_withdrawal(amount)
        assert result == "Невозможно выдать запрошенную сумму с текущими купюрами"

def test_algorithm_comparison():
    """Сравнение работы двух алгоритмов на одинаковых данных"""
    banknotes = [(500, 3), (200, 5), (100, 10)]
    amount = 700
    
    greedy_result = greedy_cash_withdrawal(banknotes.copy(), amount)
    dp_result = dp_cash_withdrawal(banknotes.copy(), amount)
    
    # Оба алгоритма должны выдать корректную сумму
    assert sum(greedy_result) == amount
    assert sum(dp_result) == amount
    
    # DP алгоритм должен находить оптимальное решение (меньшее количество купюр)
    if isinstance(greedy_result, list) and isinstance(dp_result, list):
        assert len(dp_result) <= len(greedy_result)

if __name__ == "__main__":
    pytest.main(["-v", "--cov=alg", "--cov-report=html"])