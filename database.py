import sqlite3

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect("rsa.db")
    cursor = conn.cursor()
    # Создаем таблицу для хранения ключей RSA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rsa_keys (
            id INTEGER PRIMARY KEY,
            n TEXT NOT NULL,
            e TEXT NOT NULL,
            d TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# Сохранение пары ключей
def save_key_pair(n, e, d):
    conn = sqlite3.connect("rsa.db")
    cursor = conn.cursor()
    
    # Преобразуем большие числа в строки для хранения
    n_str = str(n)
    e_str = str(e)
    d_str = str(d)
    
    cursor.execute(
        "INSERT INTO rsa_keys (n, e, d) VALUES (?, ?, ?)",
        (n_str, e_str, d_str)
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid

# Получение последней пары ключей
def get_last_key_pair():
    conn = sqlite3.connect("rsa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT n, e, d FROM rsa_keys ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    
    if result:
        n, e, d = result
        return {
            'public_key': {'n': int(n), 'e': int(e)},
            'private_key': {'n': int(n), 'd': int(d)}
        }
    else:
        return None

# Получение публичного ключа
def get_public_key():
    conn = sqlite3.connect("rsa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT n, e FROM rsa_keys ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    
    if result:
        n, e = result
        return int(n), int(e)
    else:
        return None

# Получение приватного ключа
def get_private_key():
    conn = sqlite3.connect("rsa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT n, d FROM rsa_keys ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    
    if result:
        n, d = result
        return int(n), int(d)
    else:
        return None

# Получение всех ключей
def get_all_keys():
    conn = sqlite3.connect("rsa.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, n, e, d, created_at FROM rsa_keys ORDER BY id DESC")
    results = cursor.fetchall()
    conn.close()
    
    keys = []
    for result in results:
        id, n, e, d, created_at = result
        keys.append({
            'id': id,
            'public_key': {'n': n[:20] + '...' if len(n) > 20 else n, 'e': e},
            'private_key': {'n': n[:20] + '...' if len(n) > 20 else n, 'd': d[:20] + '...' if len(d) > 20 else d},
            'created_at': created_at
        })
    
    return keys

# Удаление ключа
def delete_key(key_id):
    conn = sqlite3.connect("rsa.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rsa_keys WHERE id = ?", (key_id,))
    conn.commit()
    conn.close()