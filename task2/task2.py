import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from sqlite3 import Error


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('task2.ui', self)
        self.setFixedSize(800, 640)
        self.db = Repository('films_db.sqlite')

        self.loadButton.clicked.connect(self.fillTableWidget)
        self.saveButton.clicked.connect(self.updateDatabase)

    def fillTableWidget(self):
        films = self.db.getFilms()
        self.tableWidget.clear()
        num_columns = len(films[0])
        num_rows = len(films)
        self.tableWidget.setColumnCount(num_columns)
        self.tableWidget.setRowCount(num_rows)
        for i, film in enumerate(films):
            for j, field in enumerate(film):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(field)))

    def updateDatabase(self):
        for row in range(self.tableWidget.rowCount()):
            film = Film(
                self.tableWidget.item(row, 0).text(),
                self.tableWidget.item(row, 1).text(),
                self.tableWidget.item(row, 2).text(),
                self.tableWidget.item(row, 3).text(),
                self.tableWidget.item(row, 4).text()
            )
            self.db.updateFilm(film)


class Film:
   def __init__(self, id, title, year, genre, duration):
       self.id = id
       self.title = title
       self.year = year
       self.genre = genre
       self.duration = duration


class Repository:
   def __init__(self, database_name):
       self.database = database_name

   def getConnection(self):
       connection = None
       try:
           connection = sqlite3.connect(self.database)
           return connection
       except Error as e:
           print(e)

       return connection

   def getFilms(self):
       conn = self.getConnection()
       cursor = conn.cursor()
       cursor.execute("SELECT * FROM films")
       films = cursor.fetchall()

       return films

   def updateFilm(self, film):
       conn = self.getConnection()
       cursor = conn.cursor()
       cursor.execute("UPDATE films SET title = ?, year = ?, genre = ?, duration = ? WHERE id = ?",
                     (film.title, film.year, film.genre, film.duration, film.id))
       conn.commit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
