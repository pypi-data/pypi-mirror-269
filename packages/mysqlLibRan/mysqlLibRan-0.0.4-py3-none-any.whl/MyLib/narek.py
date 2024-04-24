def pyqt_sec_win():
    """
ТУТ ИНИЦИАЛИЗАЦИЯ ИНТЕРФЕЙСА ИЗ ДИЗАЙНЕРА И СОЗДАНИЕ ВТОРОГО ОКНА

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

def pyqt_sql():
    """
ТУТ СОЗДАНИЕ ИНТЕРФЕЙСА ЧЕРЕЗ КОД И ПОДКЛЮЧЕНИЕ К БД

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