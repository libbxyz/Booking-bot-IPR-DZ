import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, username):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`, `username`) VALUES (?,?)", (user_id, username,))

    def all_usr(self):
        with self.connection:
            return self.cursor.execute("SELECT Count(*) FROM users").fetchone()[0]

    def start_log(self, user_id, login):
        with self.connection:
            self.cursor.execute("UPDATE users SET login = ? WHERE user_id = ?", (login, user_id,))
            return "Придумайте пароль:"

    def start_log_passw(self, user_id, passw):
        with self.connection:
            self.cursor.execute("UPDATE users SET passw = ? WHERE user_id = ?", (passw, user_id,))
            return "Вы зарегистрированы!"

    def check_log(self, user_id, login):
        with self.connection:
            x = self.cursor.execute("SELECT `login` FROM users WHERE user_id = ?", (user_id,)).fetchall()
            if str(x).split("'")[1] == login:
                return "Введите пароль"
            else:
                return "Такого логина не существует!"

    def check_passw(self, user_id, passw):
        with self.connection:
            x = self.cursor.execute("SELECT `passw` FROM users WHERE user_id = ?", (user_id,)).fetchall()
            print(x)
            if str(x).split("'")[1] == passw:
                return "Вы вошли!"
            else:
                return "Непрвильный пароль!"

    def new_bron(self, user_id, text):
        with self.connection:
            self.cursor.execute("UPDATE users SET bronned = ? WHERE user_id = ?", (text, user_id,))
            return "Успешно добавлено!"

    def check_bron(self, user_id):
        with self.connection:
            x = \
                str(self.cursor.execute("SELECT bronned FROM users WHERE user_id = ?", (user_id,)).fetchall()).split(
                    "'")[1]
            return x.replace("\\n", "\n")

