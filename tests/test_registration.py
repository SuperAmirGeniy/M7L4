import pytest  
import sqlite3  
import os  
from registration.registration import create_db, add_user, authenticate_user, display_users  

DB_NAME = 'users.db'  # имя вашей базы данных  

@pytest.fixture(scope="module")  
def setup_database():  
    """Фикстура для настройки базы данных перед тестами и её очистки после."""  
    create_db()  
    yield  
    try:  
        os.remove(DB_NAME)  
    except PermissionError:  
        pass  

@pytest.fixture  
def connection():  
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""  
    conn = sqlite3.connect(DB_NAME)  
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

def test_authenticate_user(setup_database, connection):  
    """Тест успешной аутентификации пользователя."""  
    add_user('authuser', 'authuser@example.com', 'password123')  
    assert authenticate_user('authuser', 'password123') == True, "Пользователь должен быть успешно аутентифицирован."  

def test_authenticate_user_wrong_password(setup_database, connection):  
    """Тест аутентификации пользователя с неправильным паролем."""  
    add_user('wrongpassuser', 'wrongpass@example.com', 'correctpassword')  
    assert authenticate_user('wrongpassuser', 'wrongpassword') == False, "Аутентификация должна завершиться неудачей с неправильным паролем."  

def test_display_users(setup_database, connection):  
    """Тест отображения пользователей."""  
    add_user('user1', 'user1@example.com', 'password1')  
    add_user('user2', 'user2@example.com', 'password2')  
    
    users = display_users()  
    assert len(users) == 2, "Должно быть два пользователя в базе данных."  
    assert 'user1' in [user['username'] for user in users], "user1 должен быть в списке пользователей."  
    assert 'user2' in [user['username'] for user in users], "user2 должен быть в списке пользователей."
    
# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""