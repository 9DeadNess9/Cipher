import pytest
from alg import encrypt, decrypt, encrypt_text, decrypt_text

# Тестовые ключи RSA (используются только для тестирования)
TEST_PUBLIC_KEY = {'n': 3233, 'e': 17}  # n = p*q, где p=61, q=53
TEST_PRIVATE_KEY = {'n': 3233, 'd': 2753}

def test_basic_encryption_decryption():
    """Проверка базового шифрования и дешифрования текста"""
    text = "Hello World"
    encrypted = encrypt_text(text, TEST_PUBLIC_KEY)
    decrypted = decrypt_text(encrypted, TEST_PRIVATE_KEY)
    assert decrypted == text

def test_empty_string():
    """Проверка шифрования пустой строки (граничный случай)"""
    text = ""
    encrypted = encrypt_text(text, TEST_PUBLIC_KEY)
    assert len(encrypted) == 0
    decrypted = decrypt_text(encrypted, TEST_PRIVATE_KEY)
    assert decrypted == text

def test_message_too_large():
    """Проверка ошибки при слишком большом сообщении (негативный случай)"""
    message = TEST_PUBLIC_KEY['n'] + 1
    with pytest.raises(ValueError, match="Сообщение слишком длинное для данного ключа"):
        encrypt(message, TEST_PUBLIC_KEY)

if __name__ == "__main__":
    pytest.main(["-v", "--cov=alg", "--cov-report=html"])