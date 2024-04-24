def pyqt_sec_win():
    """
#ТУТ ИНИЦИАЛИЗАЦИЯ ИНТЕРФЕЙСА ИЗ ДИЗАЙНЕРА И СОЗДАНИЕ ВТОРОГО ОКНА

# Импорт необходимых модулей и классов из библиотеки PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
# Импорт сгенерированных классов пользовательского интерфейса из файлов mainwin.py и second_window.py
from mainwin import Ui_MainWindow
from second_window import Ui_Form
# Импорт модуля sys для работы с системными параметрами и выхода из приложения
import sys

# Определение класса MainWindow, который является наследником класса QMainWindow
class MainWindow(QMainWindow):
    # Метод инициализации класса MainWindow
    def __init__(self):
        super().__init__()  # Вызов метода инициализации родительского класса
        self.ui = Ui_MainWindow()  # Создание экземпляра класса, представляющего основное окно
        self.ui.setupUi(self)  # Настройка пользовательского интерфейса основного окна
        self.init_ui()  # Вызов метода инициализации пользовательского интерфейса

    # Метод для инициализации пользовательского интерфейса
    def init_ui(self):
        # Привязка сигнала "clicked" кнопки go_but к методу show_sum
        self.ui.go_but.clicked.connect(self.show_sum)

    # Метод для вычисления суммы значений, введенных в поля lineEdit, и вывода результата
    def sum(self):
        try:
            item1 = int(self.ui.lineEdit.text())  # Получение значения из первого поля
            item2 = int(self.ui.lineEdit_2.text())  # Получение значения из второго поля
            item3 = int(self.ui.lineEdit_3.text())  # Получение значения из третьего поля
            return item2 + item1 + item3  # Возвращение суммы трех значений
        except Exception:
            return 'Вы ввели не числа'  # Вывод сообщения об ошибке, если введены не числа

    # Метод для отображения дополнительного окна с результатом вычислений
    def show_sum(self):
        self.dialog_win = QWidget()  # Создание экземпляра класса, представляющего дополнительное окно
        self.ui_dialog = Ui_Form()  # Создание экземпляра класса, представляющего интерфейс дополнительного окна
        self.ui_dialog.setupUi(self.dialog_win)  # Настройка пользовательского интерфейса дополнительного окна
        self.dialog_win.setWindowTitle('SUMMA')  # Установка заголовка для дополнительного окна
        self.dialog_win.show()  # Отображение дополнительного окна
        result = self.sum()  # Вызов метода для вычисления суммы
        self.ui_dialog.result.setText(str(result))  # Вывод результата вычислений в соответствующее поле текстового виджета

# Проверка, является ли данный скрипт главным модулем
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Создание объекта приложения
    window = MainWindow()  # Создание объекта основного окна
    window.show()  # Отображение основного окна
    sys.exit(app.exec())  # Запуск основного цикла обработки событий приложения
    """

def pyqt_sqlite():
    """
#ТУТ СОЗДАНИЕ ИНТЕРФЕЙСА ЧЕРЕЗ КОД И ПОДКЛЮЧЕНИЕ К БД

# Импорт модулей sys и sqlite3 для работы с системными параметрами и базой данных SQLite соответственно
import sys
import sqlite3
# Импорт необходимых классов и виджетов из библиотеки PyQt6
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, \
    QTableWidget, QTableWidgetItem

# Определение класса DatabaseViewer, который является наследником класса QMainWindow
class DatabaseViewer(QMainWindow):
    # Метод инициализации класса DatabaseViewer
    def __init__(self):
        super().__init__()  # Вызов метода инициализации родительского класса

        self.setWindowTitle("Просмотр БД")  # Установка заголовка для главного окна

        self.central_widget = QWidget()  # Создание виджета для размещения элементов интерфейса
        self.setCentralWidget(self.central_widget)  # Установка центрального виджета для главного окна

        layout = QVBoxLayout()  # Создание вертикального макета

        self.table_widget = QTableWidget()  # Создание виджета таблицы
        layout.addWidget(self.table_widget)  # Добавление виджета таблицы в макет

        # Создание кнопок для загрузки данных из различных таблиц
        self.load_button1 = QPushButton("Users")
        layout.addWidget(self.load_button1)
        self.load_button2 = QPushButton("Posts")
        layout.addWidget(self.load_button2)

        self.central_widget.setLayout(layout)  # Установка макета для центрального виджета

        # Привязка сигналов "clicked" кнопок к соответствующим методам
        self.load_button1.clicked.connect(self.select_users)
        self.load_button2.clicked.connect(self.select_posts)

    # Метод для загрузки данных из таблицы "users"
    def select_users(self):
        self.load_data("users")

    # Метод для загрузки данных из таблицы "posts"
    def select_posts(self):
        self.load_data("posts")

    # Метод для загрузки данных из указанной таблицы базы данных
    def load_data(self, table):
        connection = sqlite3.connect("mydatabase.db")  # Установка соединения с базой данных
        cursor = connection.cursor()  # Создание курсора для выполнения SQL-запросов

        cursor.execute(f"SELECT * FROM {table}")  # Выполнение SQL-запроса для выборки данных из таблицы
        result = cursor.fetchall()  # Получение результатов выполнения запроса

        # Установка количества строк и столбцов таблицы
        self.table_widget.setRowCount(len(result))
        self.table_widget.setColumnCount(len(result[0]))

        # Задание заголовков столбцов таблицы
        column_headers = [description[0] for description in cursor.description]
        self.table_widget.setHorizontalHeaderLabels(column_headers)

        # Заполнение таблицы данными
        for row_index, row_data in enumerate(result):
            for column_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.table_widget.setItem(row_index, column_index, item)

        connection.close()  # Закрытие соединения с базой данных

# Основная функция, запускающая приложение
def main():
    app = QApplication(sys.argv)  # Создание объекта приложения
    window = DatabaseViewer()  # Создание объекта главного окна
    window.show()  # Отображение главного окна
    sys.exit(app.exec())  # Запуск основного цикла обработки событий приложения

# Проверка, является ли данный скрипт главным модулем
if __name__ == "__main__":
    main()

    """
    pass

def mysql_pyqt_con():
    """
pip install MySQLdb`
pip install mysql.connector


import mysql.connector
from typing import List, Tuple
from datetime import datetime

config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'test_db',
    'raise_on_warnings': True
}

class Database:
    def __init__(self):
        self.connection = self.__get_connect_to_db()
        self.cursor = self.connection.cursor()

    def __get_connect_to_db(self):
        try:
            connection = mysql.connector.connect(**config)
            print("Подключение успешно!")
            return connection
        except mysql.connector.Error as err:
            print(f"Ошибка подключения: {err}")
            exit(1)

    def get_position(self) -> List[tuple]:
        self.cursor.execute("SELECT * from positions")
        rows = self.cursor.fetchall()
        return rows


    def reg_new_user(self, login, password, mail='', phone='') -> bool:
        date = datetime.now()
        self.cursor.execute("select check_password(%s)", (password, ))
        result = self.cursor.fetchone()[0]
        if result:
            try:
                self.cursor.execute("INSERT INTO users (login, hash_password, last_visit, mail, phone) VALUES (%s, sha2(%s, 256), %s, %s, %s)",
                                    (login, password, date, mail, phone))
                self.connection.commit()
                return True
            except Exception as e:
                print(e)
        return False

    def auth_user(self, login, password) -> Tuple[str, bool]:
        result = ''
        is_valid = False
        result = self.cursor.callproc('auth_user', (login, password, result, is_valid))
        return (result[2], result[3])

# a = Database()
# a.auth_user('alex','admin123')

# a.cursor.callproc("GetPos", )
# result = a.cursor.stored_results()
# print(next(result).fetchall())
    """
    pass

def mysql_syntax():
    """
    ------------------- POSTGRESQL -------------------------------------------------------------------------------------------------------------
CREATE TRIGGER update_done_time_trigger
BEFORE INSERT ON client
FOR EACH ROW
EXECUTE FUNCTION update_done_time();

CREATE OR REPLACE FUNCTION update_done_time()
    RETURNS TRIGGER AS $$
BEGIN
    IF NEW.name = 'timur' THEN
        NEW.age := 17;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

create or replace procedure transfer() language plpgsql
as $$
begin
    select *
    from client;

    commit;
end;$$;

------------------------------------------------------------------------------------------------------------------------------------------




----------------------------MYSQL----------------------------------------------------------------------------------------------------------

use mosoblgas;
select  from contracts;
select  from customers;
select  from contract_logs;
drop table contract_logs;
-- Создаём таблицу с логами операций
CREATE TABLE contract_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    contract_id INT,
    operation VARCHAR(10),
    operation_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
DELIMITER
-- Создаём триггера, срабатывающий на добавление данных в таблицу contracts
CREATE TRIGGER after_contract_insert
AFTER INSERT ON contracts
FOR EACH ROW
BEGIN
    INSERT INTO contract_logs (contract_id, operation, operation_time)
    VALUES (NEW.id, 'INSERT', NOW());
END;


-- Создаём триггера, срабатывающий на обновление данных в таблицу contracts
CREATE TRIGGER after_contract_update
AFTER UPDATE ON contracts
FOR EACH ROW
BEGIN
    INSERT INTO contract_logs (contract_id, operation, operation_time)
    VALUES (NEW.id, 'UPDATE', NOW());
END;


-- Создаём триггера, срабатывающий на удаление данных в таблицу contracts
CREATE TRIGGER after_contract_delete
AFTER DELETE ON contracts
FOR EACH ROW
BEGIN
    INSERT INTO contract_logs (contract_id, operation, operation_time)
    VALUES (OLD.id, 'DELETE', NOW());
END;


DELIMITER ;

-- Заполнение таблиц тестовыми данными
INSERT INTO customer_categories (id, category)
VALUES (1, 'Корпоративный клиент');

INSERT INTO customer_categories (id, category)
VALUES (2, 'Частный клиент');


INSERT INTO customers (id, firstname, lastname, address, phone, email, is_corporate_body, customer_category_id)
VALUES (1, 'Иван', 'Иванов', 'ул. Пушкина, д. 10', '1234567890', 'ivan@example.com', 1, 1);

INSERT INTO customers (id, firstname, lastname, address, phone, email, is_corporate_body, customer_category_id)
VALUES (2, 'Петр', 'Петров', 'ул. Лермонтова, д. 5', '0987654321', 'petr@example.com', 0, 2);



-- Добавление данных в таблицу contracts для проверки работы триггера after_contract_insert
INSERT INTO contracts
VALUES (1, 1, '2023-01-01', '2023-12-31', 'Контракт с Ивановым');

INSERT INTO contracts (id, customer_id, contract_date, expiration_date, contract_text)
VALUES (2, 2, '2023-02-01', '2023-12-31', 'Контракт с Петровым');


-- Обновление данных в таблице contracts для проверки работы триггера after_contract_update
UPDATE contracts SET contract_text = 'Updated contract text' WHERE id = 1;

--  Удаление данных из таблицы contracts для проверки работы триггера after_contract_delete
DELETE FROM contracts WHERE id = 1;


SELECT  FROM contract_logs;



CREATE FUNCTION `calculate_average_salary_by_department`(department_name VARCHAR(50)) RETURNS decimal(10,2)
    READS SQL DATA
BEGIN
    DECLARE avg_salary DECIMAL(10, 2);

    SELECT AVG(salary) INTO avg_salary
    FROM employees
    WHERE department = department_name;

    RETURN avg_salary;
END


CREATE FUNCTION `calculate_total_payments_by_customer`(customer_id INT) RETURNS decimal(10,2)
    READS SQL DATA
BEGIN
    DECLARE total_amount DECIMAL(10, 2);

    SELECT SUM(amount) INTO total_amount
    FROM customer_payments
    WHERE customer_id = customer_id;

    RETURN total_amount;
END

CREATE FUNCTION `calculate_total_revenue_by_service_type`(service_type_id INT) RETURNS decimal(10,2)
    READS SQL DATA
BEGIN
    DECLARE total_revenue DECIMAL(10, 2);

    SELECT SUM(amount) INTO total_revenue
    FROM invoices
    WHERE service_id IN (
        SELECT service_id
        FROM services_services_types
        WHERE service_type_id = service_type_id
    );

    RETURN total_revenue;
END


CREATE PROCEDURE `AddFoodInBasket`(in food_name varchar(16))
begin
    declare food_id bigint;
    declare session_id bigint default rand() * 100 * time(current_timestamp());
    select id into food_id from food where name=food_name;
    insert into basket (session_id, food_id) values(session_id, food_id);
    update food set amount = amount - 1, reserve = reserve + 1 where id = food_id;
    SELECT * from basket;
end;

CREATE PROCEDURE `GetBasketFood`()
begin
    SELECT food.name AS food_name, types.name AS type_name, sum(basket.amount) amount, sum(price) price
    FROM basket
    JOIN food ON basket.food_id = food.id
    JOIN types ON food.type_id = types.id
    group by food_name, type_name;
end;

CREATE PROCEDURE `GetFoodWithType`(in type_name varchar(16))
begin
    select food.*, types.name type from food join types on food.type_id = types.id where types.name = type_name;
end;

------------------------------------------------------------------------------------------------------------------------------------------
    """
    pass

def postgres_con():
    """
import psycopg2

DB_HOST = "0.0.0.0"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "admin"

conn_string = f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}"

try:
    conn = psycopg2.connect(conn_string)

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM client")

    records = cursor.fetchall()
    for record in records:
        print(record)

except (Exception, psycopg2.Error) as error:
    print("Ошибка при работе с PostgreSQL:", error)

finally:
    if conn:
        cursor.close()
        conn.close()

    """
    pass