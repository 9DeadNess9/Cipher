import sqlite3

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()
    # Создаем таблицу для хранения купюр
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS banknotes (
            denomination INTEGER PRIMARY KEY,
            quantity INTEGER NOT NULL
        )
    """)
    # Добавляем начальные данные (если таблица пустая)
    cursor.execute("SELECT COUNT(*) FROM banknotes")
    if cursor.fetchone()[0] == 0:
        initial_data = [
            (5000, 10),
            (1000, 20),
            (500, 30),
            (100, 40),
            (50, 50)
        ]
        cursor.executemany("INSERT INTO banknotes (denomination, quantity) VALUES (?, ?)", initial_data)
    conn.commit()
    conn.close()

# Получение всех доступных купюр
def get_banknotes():
    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()
    cursor.execute("SELECT denomination, quantity FROM banknotes ORDER BY denomination DESC")
    banknotes = cursor.fetchall()
    conn.close()
    return banknotes

# Обновление количества купюр после выдачи
def update_banknotes(updated_banknotes):
    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()
    for denomination, quantity in updated_banknotes.items():
        cursor.execute("UPDATE banknotes SET quantity = ? WHERE denomination = ?", (quantity, denomination))
    conn.commit()
    conn.close()

# Восстановление начального состояния купюр
def reset_banknotes():
    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()
    initial_data = [
        (5000, 10),
        (1000, 20),
        (500, 30),
        (100, 40),
        (50, 50)
    ]
    cursor.execute("DELETE FROM banknotes")
    cursor.executemany("INSERT INTO banknotes (denomination, quantity) VALUES (?, ?)", initial_data)
    conn.commit()
    conn.close()