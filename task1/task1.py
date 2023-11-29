import csv
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtGui import QColor


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('task1.ui', self)
        self.setFixedSize(800, 640)
        self.loadTable('rez.csv')

        self.filterData("", "")
        self.filterButton.clicked.connect(self.applyFilter)

    def loadTable(self, table_name):
        with open(table_name, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            self.data = list(reader)
            title = self.data[0]
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            self.tableWidget.setRowCount(len(self.data) - 1)

            for i, row in enumerate(self.data[1:]):
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(elem))

            self.tableWidget.resizeColumnsToContents()

            schools = set()
            clss = set()

            self.schoolComboBox.addItem(None)
            self.classComboBox.addItem(None)

            for row in range(self.tableWidget.rowCount()):
                school, cls = self.getSchoolAndClass(row)

                schools.add(school)
                clss.add(cls)

            schools = sorted(schools)
            clss = sorted(clss)

            for school in schools:
                self.schoolComboBox.addItem(school)
            for cls in clss:
                self.classComboBox.addItem(cls)

    def applyFilter(self):
        school_number = self.schoolComboBox.currentText()
        class_number = self.classComboBox.currentText()

        if not school_number and not class_number:
            for row in range(self.tableWidget.rowCount()):
                self.tableWidget.setRowHidden(row, False)
        else:
            self.filterData(school_number, class_number)

    def filterData(self, school_filter, class_filter):
        for row in range(self.tableWidget.rowCount()):
            school, cls = self.getSchoolAndClass(row)

            if (not school_filter or school_filter == school) and (not class_filter or class_filter == cls):
                self.tableWidget.setRowHidden(row, False)
            else:
                self.tableWidget.setRowHidden(row, True)

        self.colorRows()

    def colorRows(self):
        scores = {}
        unique_scores = []

        for row in range(self.tableWidget.rowCount()):
            login = self.tableWidget.item(row, 2).text()
            score = int(self.tableWidget.item(row, 7).text())

            if score not in scores:
                scores[score] = []
                unique_scores.append(score)

            scores[score].append((row, login, score))

        unique_scores.sort(reverse=True)

        for i, score in enumerate(unique_scores[:3]):
            for row, login, _ in scores[score]:
                for col in range(self.tableWidget.columnCount()):
                    item = self.tableWidget.item(row, col)
                    if item:
                        if i == 0:
                            item.setBackground(QColor(255, 215, 0))
                        elif i == 1:
                            item.setBackground(QColor(192, 192, 192))
                        elif i == 2:
                            item.setBackground(QColor(205, 127, 50))
                        else:
                            item.setBackground(QColor(255, 255, 255))

    def getSchoolAndClass(self, row):
        login = self.tableWidget.item(row, 2).text()
        school, cls = login.split('-')[2:4]
        return school, cls


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
