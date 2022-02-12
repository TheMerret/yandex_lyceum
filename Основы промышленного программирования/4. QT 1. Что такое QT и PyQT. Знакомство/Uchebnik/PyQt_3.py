import sys

# Импортируем из PyQt5.QtWidgets классы для создания приложения и виджета
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton


# Унаследуем наш класс от простейшего графического примитива QWidget
class Example(QWidget):
    def __init__(self):
        # Надо не забыть вызвать инициализатор базового класса
        super().__init__()
        # В метод initUI() будем выносить всю настройку интерфейса,
        # чтобы не перегружать инициализатор
        self.initUI()

    def initUI(self):
        # Зададим размер и положение нашего виджета,
        self.setGeometry(300, 300, 300, 300)
        # А также его заголовок
        self.setWindowTitle('Третья программа')
        # Создаем кнопку.
        # Передаем 2 параметра:
        # надпись и виджет, на котором будет размещена кнопка
        self.btn = QPushButton('Кнопка', self)
        # Изменяем размер кнопки. Теперь он 100 на 100 пикселей
        self.btn.resize(100, 100)
        # Размещаем кнопку на родительском виджете
        # по координатам (100, 100)
        self.btn.move(100, 100)
        # присоединим к событию нажатия на кнопку обработчик self.hello()
        self.btn.clicked.connect(self.hello)

    def hello(self):
        # метод setText() используется для задания надписи на кпопке
        self.btn.setText('Привет')


if __name__ == '__main__':
    # Создадим класс приложения PyQT
    app = QApplication(sys.argv)
    # А теперь создадим и покажем пользователю экземпляр
    # нашего виджета класса Example
    ex = Example()
    ex.show()
    # Будем ждать, пока пользователь не завершил исполнение QApplication,
    # а потом завершим и нашу программу
    sys.exit(app.exec())