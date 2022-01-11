import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPoint
import random
from PIL.ImageQt import ImageQt, QPixmap
from PIL import Image
from PIL import ImageFilter
import tkinter as tk
import datetime as dt
import sqlite3
import ui


def resize_image(input_image_path, output_image_path, size):
    original_image = Image.open(input_image_path)
    width, height = original_image.size
    resized_image = original_image.resize(size)
    width, height = resized_image.size
    resized_image.save(output_image_path)


COLORS = ['#000000',
          '#141923',
          '#414168',
          '#000080',
          '#3a7fa7',
          '#35e3e3',
          '#00FF00',
          '#8fd970',
          '#5ebb49',
          '#458352',
          '#dcd37b',
          '#fffee5',
          '#ffd035',
          '#cc9245',
          '#a15c3e',
          '#a42f3b',
          '#FF0000',
          '#f45b7a',
          '#c24998',
          '#81588d',
          '#bcb0c2',
          '#696969',
          '#ffffff'
          ]

SPRAY_PARTICLES = 100
SPRAY_DIAMETER = 10


class AppendFriend(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("timeTable.ui", self)
        finder = 'SELECT moment FROM time'
        con = sqlite3.connect("dates_1.sqlite")
        res = con.cursor().execute(finder).fetchall()
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    # def app(self):
    #     name = self.lineEdit_name.text()
    #     attitude = self.dial.value()
    #     contact = self.lineEdit_number.text()
    #     org = self.lineEdit_orgi.text()
    #     date = self.dateTimeEdit.date()
    #     date = f'{str(date.day())}.{str(date.month())}.{str(date.year())}'
    #
    #     con = sqlite3.connect("dates.sqlite")
    #     cur = con.cursor()
    #     cur.execute(f" INSERT INTO (time) VALUES ('{})
    #                     ")
    #     con.commit()
    #     con.close()
    #     self.close()


class PaletteButton(QtWidgets.QPushButton):

    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QtCore.QSize(34, 34))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)


class Canvas(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        pixmap = QtGui.QPixmap(2500, 1500)
        self.setPixmap(pixmap)

        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor('#ffffff')

        self.spray = False
        self.width = 1

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)

    def mouseMoveEvent(self, e):
        if self.last_x is None:
            self.last_x = e.x()
            self.last_y = e.y()
            return

        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.width)
        p.setColor(self.pen_color)
        painter.setPen(p)
        if not self.spray:
            painter.drawLine(self.last_x,
                             self.last_y,
                             e.x(), e.y())
            painter.end()
        else:
            for i in range(SPRAY_PARTICLES):
                x0 = random.gauss(0,
                                  SPRAY_DIAMETER)
                y0 = random.gauss(0,
                                  SPRAY_DIAMETER)
                painter.drawPoint(e.x() + x0,
                                  e.y() + y0)

        self.update()

        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

    def Rectangle(self, params):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.width)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawRect(params[0],
                         params[1],
                         params[2],
                         params[3])
        painter.end()


    def RoundRectangle(self, params):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.width)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawRoundedRect(params[0],
                                params[1],
                                params[2],
                                params[3],
                                params[4],
                                params[5])
        painter.end()

    def Ellipse(self, params):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.width)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawEllipse(params[0],
                            params[1],
                            params[2],
                            params[3])
        painter.end()

    def Line(self, params):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.width)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawLine(params[0],
                         params[1],
                         params[2],
                         params[3])
        painter.end()

    def Point(self, params):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.width)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawPoint(params[0], params[1])
        painter.end()

    def Text(self, intparams, strparam):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.width)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawText(intparams[0],
                         intparams[1],
                         strparam)
        painter.end()

    def Pie(self, params):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.width)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawPie(params[0],
                        params[1],
                        params[2],
                        params[3],
                        params[4],
                        params[5])
        painter.end()

    def Arc(self, params):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.width)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawArc(params[0],
                        params[1],
                        params[2],
                        params[3],
                        params[4],
                        params[5])
        painter.end()

    def Chord(self, params):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.width)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawChord(params[0],
                          params[1],
                          params[2],
                          params[3],
                          params[4],
                          params[5])
        painter.end()

    def Polygon(self, params):
        painter = QtGui.QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.width)
        p.setColor(self.pen_color)
        painter.setPen(p)
        params = list(map(lambda x: QPoint(x[0],
                                           x[1]),
                          params))
        painter.drawPolygon(QtGui.QPolygon(params))
        painter.end()

    def setImage(self, image):
        painter = QtGui.QPainter(self.pixmap())
        painter.drawImage(0, 0, image)
        painter.end()

    def reImage(self):
        pixmap = QtGui.QPixmap(2500, 1500)
        self.setPixmap(pixmap)

    def saveImage(self, fname):
        i, okBtnPressed = QtWidgets.QInputDialog.getText(self, "Размер",
                                                         "Введите размеры картинки(через пробел)")
        if okBtnPressed:
            i = list(map(lambda x: int(x), i.split()))
            if len(i) == 2:
                pixmap = self.pixmap()
                pixmap.save(fname)
                resize_image(fname,
                             fname,
                             (i[0],
                              i[1]))



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Рисовалка для людей с такими прямыми руками как у меня")
        self.canvas = Canvas()

        w = QtWidgets.QWidget()
        o = QtWidgets.QVBoxLayout()
        w.setLayout(o)
        o.addWidget(self.canvas)

        palette = QtWidgets.QHBoxLayout()
        self.add_palette_buttons(palette)
        o.addLayout(palette)

        self.setCentralWidget(w)

        self.setRadioButtons()
        o.addWidget(self.groupBox)
        self.setFixedSize(250*5, 160*5)

    def add_palette_buttons(self, layout):
        for c in COLORS:
            b = PaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.set_pen_color(c))
            layout.addWidget(b)

    def setRadioButtons(self):
        self.groupBox = QtWidgets.QGroupBox("Функции")

        hboxLayout = QtWidgets.QHBoxLayout()

        self.radiobtn1 = QtWidgets.QRadioButton("Прямоугольник")
        hboxLayout.addWidget(self.radiobtn1)
        self.radiobtn1.clicked.connect(self.setparamsRectangle)

        self.radiobtn2 = QtWidgets.QRadioButton("Перекруг-недоквадрат")
        hboxLayout.addWidget(self.radiobtn2)
        self.radiobtn2.clicked.connect(self.setparamsRoundRectangle)

        self.radiobtn3 = QtWidgets.QRadioButton("Овал (Или аврал)")
        hboxLayout.addWidget(self.radiobtn3)
        self.radiobtn3.clicked.connect(self.setparamsEllipse)

        self.radiobtn4 = QtWidgets.QRadioButton("Ручка")
        self.radiobtn4.setChecked(True)
        hboxLayout.addWidget(self.radiobtn4)
        self.radiobtn4.clicked.connect(self.setparamsPen)

        self.radiobtn5 = QtWidgets.QRadioButton("Пыль")
        hboxLayout.addWidget(self.radiobtn5)
        self.radiobtn5.clicked.connect(self.setparamsSpray)

        self.radiobtn6 = QtWidgets.QRadioButton("Ширина")
        hboxLayout.addWidget(self.radiobtn6)
        self.radiobtn6.clicked.connect(self.setwidth)

        self.radiobtn7 = QtWidgets.QRadioButton("Линия")
        hboxLayout.addWidget(self.radiobtn7)
        self.radiobtn7.clicked.connect(self.setparamsLine)

        self.radiobtn8 = QtWidgets.QRadioButton("Точека")
        hboxLayout.addWidget(self.radiobtn8)
        self.radiobtn8.clicked.connect(self.setparamsPoint)

        self.radiobtn9 = QtWidgets.QRadioButton("Text")
        hboxLayout.addWidget(self.radiobtn9)
        self.radiobtn9.clicked.connect(self.setparamsText)

        self.radiobtn10 = QtWidgets.QRadioButton("Угол")
        hboxLayout.addWidget(self.radiobtn10)
        self.radiobtn10.clicked.connect(self.setparamsPie)

        self.radiobtn11 = QtWidgets.QRadioButton("Дуга")
        hboxLayout.addWidget(self.radiobtn11)
        self.radiobtn11.clicked.connect(self.setparamsArc)

        self.radiobtn12 = QtWidgets.QRadioButton("Хорда")
        hboxLayout.addWidget(self.radiobtn12)
        self.radiobtn12.clicked.connect(self.setparamsChord)

        self.radiobtn13 = QtWidgets.QRadioButton("Многоугольник")
        hboxLayout.addWidget(self.radiobtn13)
        self.radiobtn13.clicked.connect(self.setparamsPolygon)

        self.radiobtn14 = QtWidgets.QRadioButton("Image")
        hboxLayout.addWidget(self.radiobtn14)
        self.radiobtn14.clicked.connect(self.setparamsImage)

        self.radiobtn15 = QtWidgets.QRadioButton("Очистить")
        hboxLayout.addWidget(self.radiobtn15)
        self.radiobtn15.clicked.connect(self.setparamsReImage)

        self.radiobtn16 = QtWidgets.QRadioButton("Save")
        hboxLayout.addWidget(self.radiobtn16)
        self.radiobtn16.clicked.connect(self.setsaveImage)

        self.radiobtn17 = QtWidgets.QRadioButton("Посмотреть даты")
        hboxLayout.addWidget(self.radiobtn17)
        self.radiobtn17.clicked.connect(self.showDates)



        self.groupBox.setLayout(hboxLayout)

    def change(delay, frame, sequence, index):
        index = (index + 1) % len(sequence)
        frame.configure(background=sequence[index])
        # frame.after(delay, lambda: change(delay, frame, sequence, index))

    def main(self):
        sequence = ['black', 'grey40', 'grey60', 'grey80', 'white', 'grey80', 'grey60', 'grey40']
        root = tk.Tk()
        frame = tk.Frame(root, width=2000, height=1500, background="red")
        frame.pack(fill=tk.BOTH, expand=True)
        self.cange(100, frame, sequence, -1)
        root.mainloop()
        return 0

    def setparamsRectangle(self):
        i, okBtnPressed = QtWidgets.QInputDialog.getText(self, "Параметры прямоугольника",
                                                         "Координаты левого верхнего угла," +
                                                         " ширина," +
                                                         " высота(через пробел)")
        if okBtnPressed:
            i = list(map(lambda x: int(x), i.split()))
            if len(i) == 4:
                self.canvas.Rectangle(i)


    def setparamsRoundRectangle(self):
        i, okBtnPressed = QtWidgets.QInputDialog.getText(self,
                                                         "Параметры прямоугольника",
                                                         "Координаты левого верхнего угла," +
                                                         " ширина, высота," +
                                                         " координаты радиуса кривизны(через пробел)")

        if okBtnPressed:
            i = list(map(lambda x: int(x), i.split()))
            if len(i) == 6:
                self.canvas.RoundRectangle(i)

    def setparamsEllipse(self):
        i, okBtnPressed = QtWidgets.QInputDialog.getText(self,
                                                         "Параметры эллипса",
                                                         "Координаты левого верхнего угла," +
                                                         " ширина," +
                                                         " высота(через пробел)")

        if okBtnPressed:
            i = list(map(lambda x: int(x), i.split()))
            if len(i) == 4:
                self.canvas.Ellipse(i)

    def setparamsPen(self):
        self.canvas.spray = False

    def setparamsSpray(self):
        self.canvas.spray = True

    def setwidth(self):
        i, okBtnPressed = QtWidgets.QInputDialog.getText(self, "Ширина кисти",
                                                         "Введите ширину кисти")
        i = int(i)

        if i > 0:
            self.canvas.width = i

    def setparamsLine(self):
        i, okBtnPressed = QtWidgets.QInputDialog.getText(self, "Параметры линии",
                                                         "Координаты первой и второй" +
                                                         " точек(через пробел)")

        if okBtnPressed:
            i = list(map(lambda x: int(x), i.split()))

            if len(i) == 4:
                self.canvas.Line(i)

    def setparamsPoint(self):
        i, okBtnPressed = QtWidgets.QInputDialog.getText(self, "Параметры точки",
                                                         "Координаты точки")

        if okBtnPressed:
            i = list(map(lambda x: int(x), i.split()))
            if len(i) == 2:
                self.canvas.Point(i)

    def setparamsText(self):
        i, okBtnPressed = QtWidgets.QInputDialog.getText(self, "Параметры текста",
                                                         "Координаты начала строки и" +
                                                         " сама строка(через пробел)")

        if okBtnPressed:
            int_i = list(map(lambda x: int(x), i.split()[:2]))
            str_i = ' '.join(i.split(' ')[2:])

            if len(int_i) == 2 and len(str_i) != 0:
                self.canvas.Text(int_i, str_i)

    def setparamsPie(self):
        i, okBtnPressed = QtWidgets.QInputDialog.getText(self, "Параметры сектора",
                                                         "Координаты левого верхнего угла," +
                                                         " ширина, высота, стартовый угол," +
                                                         " конечный угол(через пробел)")

        if okBtnPressed:
            i = list(map(lambda x: int(x), i.split()))

            if len(i) == 6:
                self.canvas.Pie(i)

    def setparamsArc(self):
        i, okBtnPressed = QtWidgets.QInputDialog.getText(self, "Параметры дуги",
                                                         "Координаты левого верхнего угла," +
                                                         " ширина, высота, стартовый угол," +
                                                         " конечный угол(через пробел)")

        if okBtnPressed:
            i = list(map(lambda x: int(x), i.split()))

            if len(i) == 6:
                self.canvas.Arc(i)

    def setparamsChord(self):
        i, okBtnPressed = QtWidgets.QInputDialog.getText(self, "Параметры кругового сегмента",
                                                         "Координаты левого верхнего " +
                                                         "угла, ширина, высота, стартовый угол," +
                                                         " конечный угол(через пробел)")

        if okBtnPressed:
            i = list(map(lambda x: int(x), i.split()))

            if len(i) == 6:
                self.canvas.Chord(i)

    def setparamsPolygon(self):
        i, okBtnPressed = QtWidgets.QInputDialog.getText(self, "Параметры многоугольника",
                                                         "Координаты каждой вершины многоугольника" +
                                                         "(координаты - через запятые," +
                                                         " точки - через пробел)")

        if okBtnPressed:
            i = list(map(lambda x: (int(x.split(',')[0]),
                                    int(x.split(',')[1])),
                         i.split()))

            if len(i) >= 3:
                self.canvas.Polygon(i)

    def setparamsImage(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self,
                                                      "Выбрать картинку",
                                                      '')[0]



        if fname != '':
            resize_image(fname, fname, (2200, 1500))
            image = QtGui.QImage()
            image.load(fname)
            self.canvas.setImage(image)
            i, text = QtWidgets.QInputDialog.getText(self, "Блюр и поворот", "Блюр и поворот")
            a = Image.open(fname)
            a = a.filter(ImageFilter.GaussianBlur(float(i)))
            b = ImageQt(a)
            pixmap = QPixmap.fromImage(b)
            self.canvas.setPixmap(pixmap)

    # def setpaeametrImage(self, setparamsImage):
    #     i = QtWidgets.QInputDialog.getText(self, "Поворот, Размытие")
    # #
    # #     if i != '':
    # #         a = Image.open(fname)
    # #         a = a.transpose(Image.ROTATE_270)
    # #         a = a.filter(ImageFilter.GaussianBlur(i))
    # #         b = ImageQt(a)
    # #         pixmap = QPixmap.fromImage(b)
    # #         self.canvas.setPixmap(pixmap)


    def setparamsReImage(self):
        self.canvas.reImage()

    def setsaveImage(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(self,
                                                      "Сохранить",
                                                      '',
                                                      "*.png")
        self.canvas.saveImage(fname[0])

        dt_now = dt.datetime.now()
        time = []
        time.append(dt_now.day)
        time.append(dt_now.month)
        time.append(dt_now.year)
        time.append(dt_now.hour)
        time.append(dt_now.minute)
        for i in range(len(time)):
            if time[i] < 10:
                time[i] = "0" + str(time[i])
            else:
                time[i] = str(time[i])
        print(f'{time[2]}-{time[1]}-{time[0]} {time[3]}:{time[4]}')

        timeee = f'{time[2]}-{time[1]}-{time[0]} {time[3]}:{time[4]}'

        con = sqlite3.connect('dates_1.sqlite')
        cur = con.cursor()
        cur.execute(f"""
                    INSERT INTO time(moment)
                    VALUES ("{timeee}")
                    """)
        con.commit()
        con.close()
        print(1)

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("SELECT * FROM films WHERE id=?",
                             (item_id := self.spinBox.text(),)).fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с id = {item_id}")
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

    def showDates(self):
        self.sh_dates = AppendFriend()
        self.sh_dates.show()
        print(10)

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.excepthook = except_hook
sys.exit(app.exec())