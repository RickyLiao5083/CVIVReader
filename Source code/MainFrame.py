from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QPlainTextEdit, QMessageBox)
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

        self.readColumnLabel = QLabel('Data column:', self)
        self.readColumnLabel.setFont(fontTitle)
        layout.addWidget(self.readColumnLabel, 2, 7)

        self.dataColumnBox = QtWidgets.QComboBox(self)
        self.columnList = [chr(ord('A') + i) for i in range(26)]
        self.columnList[3] = 'D (default)'
        self.dataColumnBox.addItems(self.columnList)
        self.dataColumnBox.setCurrentIndex(3)
        self.dataColumnBox.setFont(fontContent)
        layout.addWidget(self.dataColumnBox, 2, 8)

        self.myLabel1 = QLabel('NTU GIEE', self)
        self.myLabel1.setFont(fontProperty)
        layout.addWidget(self.myLabel1, 2, 0)

        self.myLabel2 = QLabel('C-V Lab', self)
        self.myLabel2.setFont(fontProperty)
        layout.addWidget(self.myLabel2, 3, 0)

        self.myLabel3 = QLabel(
            'Developed by W.C, Liao' + ' ' * 90 +
            'Please visit: \"https://github.com/RickyLiao5083/B1500AReader\" for more information.', self)
        self.myLabel3.setFont(fontProperty)
        layout.addWidget(self.myLabel3, 4, 0)

        self.btnOK = QtWidgets.QPushButton(self)
        self.btnOK.setText('確定')
        self.btnOK.setFont(fontTitle)
        self.btnOK.clicked.connect(self.OK)
        layout.addWidget(self.btnOK, 4, 7)

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
                err = fetch.fetch(path, name, self.dataColumnBox.currentIndex())
                if err:
                    err_count += 1
            if err_count:
                QMessageBox.critical(None, 'Error', 'The selected Data column might not match the chosen file(s)!')
            else:
                QMessageBox.information(None, 'Message', 'Successfully generated!')

        else:
            QMessageBox.warning(None, 'Warning', 'Choose at least one CSV file!')