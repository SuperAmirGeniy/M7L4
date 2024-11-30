import unittest  
import os  
import sqlite3  

DB_NAME = 'users.db'  

def create_db():  
    with sqlite3.connect(DB_NAME) as conn:  
        cursor = conn.cursor()  
        cursor.execute('''  
            CREATE TABLE IF NOT EXISTS users (  
                username TEXT PRIMARY KEY,  
                email TEXT NOT NULL,  
                password TEXT NOT NULL  
            )  
        ''')  
        conn.commit()  

def add_user(username, email, password):  
    try:  
        with sqlite3.connect(DB_NAME) as conn:  
            cursor = conn.cursor()  
            cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, password))  
            conn.commit()  
        return True  
    except sqlite3.IntegrityError:  
        return False  

def authenticate_user(username, password):  
    with sqlite3.connect(DB_NAME) as conn:  
        cursor = conn.cursor()  
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))  
        return cursor.fetchone() is not None  

def display_users():  
    with sqlite3.connect(DB_NAME) as conn:  
        cursor = conn.cursor()  
        cursor.execute('SELECT username, email FROM users')  
        for user in cursor.fetchall():  
            print(f"Логин: {user[0]}, Электронная почта: {user[1]}")  

def main():  
    while True:  
        choice = input("Введите '1' для авторизации или '2' для регистрации (или 'exit' для выхода): ")  
        
        if choice == '1':  
            username = input("Введите логин: ")  
            password = input("Введите пароль: ")  
            if authenticate_user(username, password):  
                print("Авторизация успешна.")  
            else:  
                print("Неверный логин или пароль.")  
        elif choice == '2':  
            username = input("Введите логин нового пользователя: ")  
            email = input("Введите адрес электронной почты нового пользователя: ")  
            password = input("Введите пароль нового пользователя: ")  
            if add_user(username, email, password):  
                print("Регистрация успешна.")  
            else:  
                print("Ошибка при регистрации. Возможно, логин уже занят.")  
        elif choice.lower() == 'exit':  
            print("Выход из программы.")  
            break  
        else:  
            print("Неверный ввод. Пожалуйста, введите 1 для авторизации или 2 для регистрации.")  

class TestUserDatabase(unittest.TestCase):  

    @classmethod  
    def setUpClass(cls):  
        create_db()  
        cls.test_username = 'testuser'  
        cls.test_email = 'test@example.com'  
        cls.test_password = 'password123'  
        add_user(cls.test_username, cls.test_email, cls.test_password)  

    @classmethod  
    def tearDownClass(cls):  
        if os.path.exists(DB_NAME):  
            os.remove(DB_NAME)  

    def test_add_user(self):  
        self.assertTrue(add_user('newuser', 'newuser@example.com', 'newpassword'))  
        self.assertFalse(add_user(self.test_username, 'duplicate@example.com', 'password'))  

    def test_authenticate(self):  
        self.assertTrue(authenticate_user(self.test_username, self.test_password))  
        self.assertFalse(authenticate_user('wronguser', 'wrongpassword'))  

    def test_display_users(self):  
        import sys  
        from io import StringIO  

        captured_output = StringIO()  
        sys.stdout = captured_output  
        display_users()  
        sys.stdout = sys.__stdout__  

        output = captured_output.getvalue().strip()  
        self.assertIn(f'Логин: {self.test_username}, Электронная почта: {self.test_email}', output)  

    def test_empty_username(self):  
        self.assertFalse(add_user('', 'emptyuser@example.com', 'password'))  

    def test_empty_password(self):  
        self.assertFalse(add_user('emptyuser', 'empty@example.com', ''))  

    def test_display_no_users(self):  
        self.tearDownClass()  
        create_db()  
        import sys  
        from io import StringIO  

        captured_output = StringIO()  
        sys.stdout = captured_output  
        display_users()  
        sys.stdout = sys.__stdout__  

        output = captured_output.getvalue().strip()  
        self.assertEqual(output, '')  

if __name__ == "__main__":  
    main()