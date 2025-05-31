import sqlite3

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect("rsa.db")
    cursor = conn.cursor()
    
    # Создаем таблицу для хранения истории операций
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operation_history (
            id INTEGER PRIMARY KEY,
            operation_type TEXT NOT NULL,
            input_data TEXT NOT NULL,
            output_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# Сохранение операции шифрования
def save_encryption_operation(input_text, output_data, n, e):
    conn = sqlite3.connect("rsa.db")
    cursor = conn.cursor()
    
    # Сохраняем информацию об операции шифрования
    cursor.execute(
        "INSERT INTO operation_history (operation_type, input_data, output_data) VALUES (?, ?, ?)",
        ("Шифрование", 
         f"Исходный текст: {input_text}, Публичный ключ: (n={n}, e={e})", 
         f"Зашифрованные данные: {output_data}")
    )
    
    conn.commit()
    conn.close()
    return cursor.lastrowid

# Сохранение операции дешифрования
def save_decryption_operation(input_data, output_text, n, d):
    conn = sqlite3.connect("rsa.db")
    cursor = conn.cursor()
    
    # Сохраняем информацию об операции дешифрования
    cursor.execute(
        "INSERT INTO operation_history (operation_type, input_data, output_data) VALUES (?, ?, ?)",
        ("Дешифрование", 
         f"Зашифрованные данные: {input_data}, Приватный ключ: (n={n}, d={d})", 
         f"Дешифрованный текст: {output_text}")
    )
    
    conn.commit()
    conn.close()
    return cursor.lastrowid

# Получение истории операций
def get_operation_history():
    conn = sqlite3.connect("rsa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, operation_type, input_data, output_data, created_at FROM operation_history ORDER BY id DESC")
    results = cursor.fetchall()
    conn.close()
    
    history = []
    for result in results:
        id, operation_type, input_data, output_data, created_at = result
        history.append({
            'id': id,
            'operation_type': operation_type,
            'input_data': input_data,
            'output_data': output_data,
            'created_at': created_at
        })
    
    return history

# Очистка истории операций
def clear_history():
    conn = sqlite3.connect("rsa.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM operation_history")
    conn.commit()
    conn.close()