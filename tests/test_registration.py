import pytest  
import sqlite3  
import os  
from registration.registration import create_db, add_user, authenticate_user, display_users  

@pytest.fixture(scope="module")  
def setup_database():  
    """Фикстура для настройки базы данных перед тестами и её очистки после."""  
    create_db()  
    yield  
    try:  
        os.remove('users.db')  
    except PermissionError:  
        pass  

@pytest.fixture  
def connection():  
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""  
    conn = sqlite3.connect('users.db')  
    yield conn  
    conn.close()  

def test_create_db(setup_database, connection):  
    """Тест создания базы данных и таблицы пользователей."""  
    cursor = connection.cursor()  
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")  
    table_exists = cursor.fetchone()  
    assert table_exists, "Таблица 'users' должна существовать в базе данных."  

def test_add_new_user(setup_database, connection):  
    """Тест добавления нового пользователя."""  
    add_user('testuser', 'testuser@example.com', 'password123')  
    cursor = connection.cursor()  
    cursor.execute("SELECT * FROM users WHERE username='testuser';")  
    user = cursor.fetchone()  
    assert user, "Пользователь должен быть добавлен в базу данных."  

def test_add_user():  
    """Запуск тестов"""   
    with sqlite3.connect(DB_NAME) as conn:  
        cursor = conn.cursor()  
        cursor.execute('DROP TABLE IF EXISTS users')  
    create_db()   

    assert add_user('test_user', 'test@example.com', 'password123') == True  
    print("Тест 1 пройден: Пользователь успешно зарегистрирован.")  
    
    assert add_user('test_user', 'test@example.com', 'password123') == False  
    print("Тест 2 пройден: Нельзя зарегистрировать пользователя с существующим логином.")  

def test_authenticate_user(setup_database, connection):  
    """Тест успешной аутентификации пользователя."""  
    add_user('authuser', 'authuser@example.com', 'password123')  
    assert authenticate_user('authuser', 'password123') == True, "Пользователь должен быть успешно аутентифицирован."  

def test_authenticate_user_wrong_password(setup_database, connection):  
    """Тест аутентификации пользователя с неправильным паролем."""  
    add_user('wrongpassuser', 'wrongpass@example.com', 'correctpassword')  
    assert authenticate_user('wrongpassuser', 'wrongpassword') == False, "Аутентификация должна завершиться неудачей с неправильным паролем."
    
# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""