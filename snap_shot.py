from PyQt5 import QtWidgets, QtCore, QtGui
from tkinter import  Tk
from PIL import ImageGrab,Image
import cv2
import numpy as np
import sys
from os import path
from PyQt5.QtWidgets import QApplication
from sqlite3 import connect,Binary
from io import BytesIO


class MyWidget(QtWidgets.QWidget):
    def __init__(self, crr_page):
        super().__init__()
        root = Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.withdraw()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setWindowTitle(' ')
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(
            QtGui.QCursor(QtCore.Qt.CrossCursor)
        )
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.crr_page = crr_page
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor('black'), 3))
        qp.setBrush(QtGui.QColor(128, 128, 255, 128))
        qp.drawRect(QtCore.QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.close()

        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())

        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        save_to_database(img)

        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        cv2.imshow('Captured Image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def save_to_database(image):
    conn = connect("image_database.db")
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY AUTOINCREMENT, data BLOB)''')

    image_bytes = BytesIO()
    image.save(image_bytes, format='PNG')
    image_data = image_bytes.getvalue()

    cursor.execute('''INSERT INTO images (data) VALUES (?)''', (Binary(image_data),))

    conn.commit()
    conn.close()

def retrieve_images():
    conn = connect("image_database.db")
    cursor = conn.cursor()

    cursor.execute('''SELECT data FROM images ORDER BY id DESC''')
    results = cursor.fetchall()

    image_list = []
    for result in results:
        image_data = result[0]
        image = Image.open(BytesIO(image_data))
        image_list.append(image)

    conn.close()
    return image_list
    
def clear_database():
    conn = connect("image_database.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute('''DELETE FROM images''')
    except Exception as e:
        return
    conn.commit()
    conn.close()

def snap(counter_index):
    app = QApplication(sys.argv)
    window = MyWidget(counter_index)
    app.exec_()