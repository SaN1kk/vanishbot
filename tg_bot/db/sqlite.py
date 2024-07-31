import sqlite3


def logger(statement):
    print(f"""
--------------------------------------------------
Executing:
{statement}
--------------------------------------------------
""")


class DataBase:

    def __init__(self, path_to_db='users.db'):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self,
                sql: str,
                parameters: tuple = (),
                fetchone: bool = False,
                fetchall: bool = False,
                commit=False
                ):
        conn = self.connection  # открываем соединение
        conn.set_trace_callback(logger)
        cursor = conn.cursor()  # устанавливаем курсор
        data = None

        cursor.execute(sql, parameters)  # Вызываем полученные SQL - команду

        if commit:
            conn.commit()  # сохранить изменения в БД
        if fetchone:  # выгрузить одно значение (например только id) из БД в Python
            data = cursor.fetchone()
        if fetchall:  # выгрузить все данные из БД в Python
            data = cursor.fetchall()
        conn.close()
        return data

    def create_table_users(self):
        sql_query = """
        CREATE TABLE IF NOT EXISTS users (
        id BIGINT NOT NULL, 
        username VARCHAR(255),
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        language_code VARCHAR(10),
        is_bot BOOLEAN,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_interaction_date TIMESTAMP,
        PRIMARY KEY (id)
        );
        """
        self.execute(sql=sql_query, commit=True)

    def add_user(self, id: int, username: str = None, first_name: str = None, last_name: str = None,
                 language_code: str = None, is_bot: bool = False):
        sql_query = """
        INSERT INTO users (
        id, username, first_name, last_name, language_code, is_bot, registration_date)
        VALUES (?, ?, ?, ?, ?, ?, DATETIME(CURRENT_TIMESTAMP, '+3 hours'));
        """
        params = (id, username, first_name, last_name, language_code, is_bot)
        self.execute(sql=sql_query, commit=True, parameters=params)

    def select_all_users(self):
        sql_query = "SELECT * FROM users"
        return self.execute(sql=sql_query, fetchall=True)

    def format_args(self, sql, parametrs: dict):
        sql += ' AND '.join([f"{item} = ?" for item in parametrs.keys()])
        return sql, tuple(parametrs.values())

    def select_user(self, **kwargs):
        sql_query = "SELECT * FROM users WHERE "
        sql_query, params = self.format_args(sql=sql_query, parametrs=kwargs)
        return self.execute(sql=sql_query, parameters=params, fetchone=True)

    def count_users(self):
        return self.execute(sql="SELECT COUNT(*) FROM users;", fetchone=True)[0]

    def delete_all_users(self):
        self.execute(sql="DELETE FROM users;", commit=True)

    def delete_user(self, id):
        self.execute(sql="DELETE FROM users WHERE id=?;", parameters=(id,), commit=True)

    def update_user(self, id: int, username: str = None, first_name: str = None, last_name: str = None,
                    language_code: str = None, is_bot: bool = False):
        sql_query = """
        UPDATE users SET
            username = ?,
            first_name = ?,
            last_name = ?,
            language_code = ?,
            is_bot = ?,
            last_interaction_date = DATETIME(CURRENT_TIMESTAMP, '+3 hours')
        WHERE id = ?;
        """
        params = (username, first_name, last_name, language_code, is_bot, id)
        self.execute(sql=sql_query, commit=True, parameters=params)

    def update_last_interaction(self, id: int):
        sql_query = """
        UPDATE users SET
            last_interaction_date = DATETIME(CURRENT_TIMESTAMP, '+3 hours')
        WHERE id = ?;
        """
        params = (id,)
        self.execute(sql=sql_query, commit=True, parameters=params)

    # ToDo ----------------------------------------------

    def create_table_applications(self):
        sql_query = """
        CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id BIGINT NOT NULL, 
        username VARCHAR(255),
        first_name VARCHAR(255),
        last_name VARCHAR(255),
        language_code VARCHAR(10),
        status TEXT DEFAULT 'open',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.execute(sql=sql_query, commit=True)

    def add_application(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None,
                        language_code: str = None):
        sql_query = """
        INSERT INTO applications (
        user_id, username, first_name, last_name, language_code, created_at)
        VALUES (?, ?, ?, ?, ?, DATETIME(CURRENT_TIMESTAMP, '+3 hours'));
        """
        params = (user_id, username, first_name, last_name, language_code)
        self.execute(sql=sql_query, commit=True, parameters=params)

    def close_application(self, application_id: int):
        sql = "UPDATE applications SET status='closed' WHERE id=?;"
        self.execute(sql, parameters=(application_id,), commit=True)

    def get_open_application_id(self, user_id: int):
        sql = "SELECT id FROM applications WHERE user_id=? AND status='open';"
        result = self.execute(sql, parameters=(user_id,), fetchone=True)
        return result[0] if result else None

    def get_all_open_applications(self):
        try:
            sql_query = """
            SELECT id, user_id, username, first_name, last_name, language_code, created_at
            FROM applications
            WHERE status = 'open';
            """
            open_applications = self.execute(sql=sql_query, fetchall=True)
            return open_applications
        except Exception as e:
            print(f"Error fetching open applications: {e}")
            return []

    def count_application(self):
        return self.execute(sql="SELECT COUNT(*) FROM applications;", fetchone=True)[0]

    def count_open_applications(self):
        return self.execute(sql="SELECT COUNT(*) FROM applications WHERE status = 'open';", fetchone=True)[0]

    # ToDo ----------------------------------------------

    def create_table_exchange_applications(self):
        sql_query = """
        CREATE TABLE IF NOT EXISTS exchange_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id BIGINT NOT NULL,
            username VARCHAR(255),
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            language_code VARCHAR(10),
            amount FLOAT NOT NULL,
            rate FLOAT NOT NULL,
            total FLOAT NOT NULL,
            status TEXT DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.execute(sql=sql_query, commit=True)

    def add_exchange_application(self, user_id: int, username: str = None, first_name: str = None,
                                 last_name: str = None,
                                 language_code: str = None, amount: float = 0, rate: float = 0, total: float = 0):
        sql_query = """
        INSERT INTO exchange_applications (
            user_id, username, first_name, last_name, language_code, amount, rate, total, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'open', DATETIME(CURRENT_TIMESTAMP, '+3 hours'));
        """
        params = (user_id, username, first_name, last_name, language_code, amount, rate, total)
        self.execute(sql=sql_query, commit=True, parameters=params)

    def get_open_exchange_applications(self):
        sql_query = "SELECT * FROM exchange_applications WHERE status = 'open';"
        return self.execute(sql=sql_query, fetchall=True)

    def count_open_exchange_applications(self):
        sql_query = "SELECT COUNT(*) FROM exchange_applications WHERE status = 'open';"
        return self.execute(sql=sql_query, fetchone=True)[0]

    def count_all_exchange_applications(self):
        sql_query = "SELECT COUNT(*) FROM exchange_applications;"
        return self.execute(sql=sql_query, fetchone=True)[0]

    def get_open_exchange_application_id(self, user_id: int):
        sql = "SELECT id FROM exchange_applications WHERE user_id=? AND status='open';"
        result = self.execute(sql, parameters=(user_id,), fetchone=True)
        return result[0] if result else None

    def close_exchange_application(self, application_id: int):
        sql = "UPDATE exchange_applications SET status='closed' WHERE id=?;"
        self.execute(sql, parameters=(application_id,), commit=True)

    # ToDo ----------------------------------------------

    def create_table_exchange_rate(self):
        sql_query = """
        CREATE TABLE IF NOT EXISTS exchange_rate (
            id INTEGER PRIMARY KEY,
            rate REAL NOT NULL
        );
        """
        self.execute(sql=sql_query, commit=True)

        # Инициализируем таблицу с начальным значением, если таблица пустая
        if not self.execute("SELECT COUNT(*) FROM exchange_rate", fetchone=True)[0]:
            self.execute("INSERT INTO exchange_rate (id, rate) VALUES (1, 0.0)", commit=True)

    def get_exchange_rate(self):
        sql_query = "SELECT rate FROM exchange_rate WHERE id = 1"
        result = self.execute(sql=sql_query, fetchone=True)
        if result:
            return result[0]
        return None

    def update_exchange_rate(self, new_rate: float):
        sql_query = "UPDATE exchange_rate SET rate = ? WHERE id = 1"
        self.execute(sql=sql_query, parameters=(new_rate,), commit=True)