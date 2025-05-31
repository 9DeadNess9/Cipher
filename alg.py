import random
import math
from database import save_key_pair, get_public_key, get_private_key

def is_prime(n, k=5):
    """
    Проверка на простоту числа с использованием теста Миллера-Рабина.
    n - проверяемое число
    k - количество итераций теста
    """
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    
    # Представляем n - 1 в виде d * 2^r
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    
    # Выполняем k тестов
    for _ in range(k):
        if not miller_rabin_test(n, d, r):
            return False
    return True

def miller_rabin_test(n, d, r):
    """
    Один проход теста Миллера-Рабина для числа n.
    """
    # Выбираем случайное число a в диапазоне [2, n-2]
    a = random.randint(2, n - 2)
    
    # Вычисляем x = a^d mod n
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    
    # Повторяем r - 1 раз
    for _ in range(r - 1):
        x = pow(x, 2, n)
        if x == n - 1:
            return True
    
    return False

def generate_prime_number(bit_size=512):
    """
    Генерирует простое число заданной битовой длины.
    """
    while True:
        # Генерируем случайное нечетное число
        p = random.getrandbits(bit_size) | 1
        # Проверяем на простоту
        if is_prime(p):
            return p

def generate_key_pair(bit_size=512):
    """
    Генерирует пару ключей RSA.
    """
    # Генерируем два простых числа
    p = generate_prime_number(bit_size)
    q = generate_prime_number(bit_size)
    
    # Вычисляем модуль
    n = p * q
    
    # Вычисляем функцию Эйлера
    phi = (p - 1) * (q - 1)
    
    # Выбираем открытую экспоненту e
    e = 65537  # Стандартное значение для e
    
    # Убеждаемся, что e и phi взаимно просты
    assert math.gcd(e, phi) == 1
    
    # Вычисляем закрытую экспоненту d
    d = pow(e, -1, phi)
    
    # Сохраняем ключи в базе данных
    save_key_pair(n, e, d)
    
    return {
        'public_key': {'n': n, 'e': e},
        'private_key': {'n': n, 'd': d}
    }

def encrypt(message, public_key=None):
    """
    Шифрует сообщение с помощью открытого ключа RSA.
    """
    if public_key is None:
        n, e = get_public_key()
    else:
        n, e = public_key['n'], public_key['e']
    
    # Преобразуем строку в число
    if isinstance(message, str):
        message = int.from_bytes(message.encode(), 'big')
    
    # Проверка, что сообщение меньше модуля
    if message >= n:
        raise ValueError("Сообщение слишком длинное для данного ключа")
    
    # Шифруем сообщение: c = m^e mod n
    cipher = pow(message, e, n)
    return cipher

def decrypt(cipher, private_key=None):
    """
    Дешифрует сообщение с помощью закрытого ключа RSA.
    """
    if private_key is None:
        n, d = get_private_key()
    else:
        n, d = private_key['n'], private_key['d']
    
    # Дешифруем сообщение: m = c^d mod n
    message = pow(cipher, d, n)
    return message

def text_to_numbers(text):
    """
    Преобразует текст в список чисел для шифрования.
    """
    # Простой подход: каждый символ отдельно
    return [ord(char) for char in text]

def numbers_to_text(numbers):
    """
    Преобразует список чисел в текст после дешифрования.
    """
    return ''.join(chr(num) for num in numbers)

def encrypt_text(text, public_key=None):
    """
    Шифрует текстовое сообщение.
    """
    numbers = text_to_numbers(text)
    encrypted = [encrypt(num, public_key) for num in numbers]
    return encrypted

def decrypt_text(encrypted, private_key=None):
    """
    Дешифрует зашифрованное текстовое сообщение.
    """
    decrypted = [decrypt(num, private_key) for num in encrypted]
    return numbers_to_text(decrypted)