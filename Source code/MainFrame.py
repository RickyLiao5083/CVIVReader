from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QPlainTextEdit, QMessageBox, QTextBrowser)
import fetch


class MainFrame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.filePath = []

    def initUI(self):
        self.setWindowTitle('B1500A CSV Reader')
        self.setGeometry(0, 0, 2850, 1650)

        layout = QGridLayout()
        self.setLayout(layout)

        fontTitle = QtGui.QFont()
        fontTitle.setPointSize(12)
        fontTitle.setBold(True)

        fontContent = QtGui.QFont()
        fontContent.setPointSize(12)

        fontProperty = QtGui.QFont()
        fontProperty.setPointSize(10)

        self.fileLabel = QLabel('Choose your CSV files:', self)
        self.fileLabel.setFont(fontTitle)
        layout.addWidget(self.fileLabel, 0, 0)

        self.fileInput = QPlainTextEdit(self)
        self.fileInput.setFont(fontContent)
        layout.addWidget(self.fileInput, 1, 0)

        self.btnOpen = QtWidgets.QPushButton(self)
        self.btnOpen.setText('選擇檔案')
        self.btnOpen.setFont(fontTitle)
        self.btnOpen.clicked.connect(self.open)
        layout.addWidget(self.btnOpen, 1, 7)

        self.XColumnLabel = QLabel('X Data column:', self)
        self.XColumnLabel.setFont(fontTitle)
        layout.addWidget(self.XColumnLabel, 2, 7)

        self.XdataColumnBox = QtWidgets.QComboBox(self)
        self.XcolumnList = [chr(ord('B') + i) for i in range(25)]
        self.XcolumnList[0] = 'B (default)'
        self.XdataColumnBox.addItems(self.XcolumnList)
        self.XdataColumnBox.setCurrentIndex(0)
        self.XdataColumnBox.setFont(fontContent)
        layout.addWidget(self.XdataColumnBox, 2, 8)

        self.YColumnLabel = QLabel('Y Data column:', self)
        self.YColumnLabel.setFont(fontTitle)
        layout.addWidget(self.YColumnLabel, 3, 7)

        self.YdataColumnBox = QtWidgets.QComboBox(self)
        self.YcolumnList = [chr(ord('B') + i) for i in range(25)]
        self.YcolumnList[2] = 'D (default)'
        self.YdataColumnBox.addItems(self.YcolumnList)
        self.YdataColumnBox.setCurrentIndex(2)
        self.YdataColumnBox.setFont(fontContent)
        layout.addWidget(self.YdataColumnBox, 3, 8)

        self.myLabel1 = QLabel('NTU GIEE C-V Lab', self)
        self.myLabel1.setFont(fontProperty)
        layout.addWidget(self.myLabel1, 2, 0)

        self.myLabel2 = QLabel('Developed by Wei-chi, Liao', self)
        self.myLabel2.setFont(fontProperty)
        layout.addWidget(self.myLabel2, 3, 0)

        self.myLabel2 = QLabel(
            'Please visit the the website for more information:', self)
        self.myLabel2.setFont(fontProperty)
        layout.addWidget(self.myLabel2, 4, 0)

        self.text_browser = QLabel()
        self.text_browser.setOpenExternalLinks(True)
        self.text_browser.setText("<a href='https://github.com/RickyLiao5083/B1500AReader/'>https://github.com/RickyLiao5083/B1500AReader</a>")
        self.text_browser.setFont(fontProperty)
        layout.addWidget(self.text_browser, 5, 0)

        self.btnOK = QtWidgets.QPushButton(self)
        self.btnOK.setText('確定')
        self.btnOK.setFont(fontTitle)
        self.btnOK.clicked.connect(self.OK)
        layout.addWidget(self.btnOK, 5, 7)

    def open(self):
        self.filePath, filterType = QtWidgets.QFileDialog.getOpenFileNames(filter='CSV (*.csv)')  # 選擇檔案對話視窗
        print(self.filePath, filterType)
        allFiles = ''
        for fp in self.filePath:
            allFiles += (fp + '\n')
        self.fileInput.setPlainText(allFiles.strip())

    def OK(self):
        if self.filePath:
            err_count = 0
            for file in self.filePath:
                path = file.rsplit('/', 1)[0] + '/'
                name = file.rsplit('/', 1)[-1]
                err = fetch.fetch(path, name, self.XdataColumnBox.currentIndex() + 1, self.YdataColumnBox.currentIndex() + 1)
                if err:
                    err_count += 1
            if err_count:
                QMessageBox.critical(None, 'Error', 'The selected Data column might not match the chosen file(s)!')
            else:
                QMessageBox.information(None, 'Message', 'Successfully generated!')

        else:
            QMessageBox.warning(None, 'Warning', 'Choose at least one CSV file!')