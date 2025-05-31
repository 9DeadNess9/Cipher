#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Скрипт для создания файла алгоритмов RSA."""

with open('alg.py', 'w', encoding='utf-8') as f:
    f.write('''import math

def encrypt(message, public_key):
    """
    Шифрует сообщение с помощью открытого ключа RSA.
    """
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

def decrypt(cipher, private_key):
    """
    Дешифрует сообщение с помощью закрытого ключа RSA.
    """
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
    if not public_key:
        raise ValueError("Необходимо предоставить публичный ключ")
        
    numbers = text_to_numbers(text)
    encrypted = [encrypt(num, public_key) for num in numbers]
    return encrypted

def decrypt_text(encrypted, private_key=None):
    """
    Дешифрует зашифрованное текстовое сообщение.
    """
    if not private_key:
        raise ValueError("Необходимо предоставить приватный ключ")
        
    decrypted = [decrypt(num, private_key) for num in encrypted]
    return numbers_to_text(decrypted)
''') 