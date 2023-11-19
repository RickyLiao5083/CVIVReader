from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QPlainTextEdit, QRadioButton, QButtonGroup,
                             QMessageBox)
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

        self.btnOpen = QtWidgets.QPushButton(self)  # 加入按鈕
        self.btnOpen.setText('選擇檔案')
        self.btnOpen.setFont(fontTitle)
        self.btnOpen.clicked.connect(self.open)
        layout.addWidget(self.btnOpen, 1, 7)

        self.directionLabel = QLabel('Direction:', self)
        self.directionLabel.setFont(fontTitle)
        layout.addWidget(self.directionLabel, 2, 7)

        self.rb_single = QRadioButton(self)
        self.rb_single.setText('single')
        self.rb_single.setFont(fontContent)
        layout.addWidget(self.rb_single, 2, 8)
        self.rb_double = QRadioButton(self)
        self.rb_double.setText('double')
        self.rb_double.setFont(fontContent)
        layout.addWidget(self.rb_double, 2, 9)

        self.groupDirection = QButtonGroup(self)
        self.groupDirection.addButton(self.rb_single, 0)
        self.groupDirection.addButton(self.rb_double, 1)

        self.readColumnLabel = QLabel('Data column:', self)
        self.readColumnLabel.setFont(fontTitle)
        layout.addWidget(self.readColumnLabel, 3, 7)

        self.dataColumnBox = QtWidgets.QComboBox(self)
        self.columnList = ['A', 'B', 'C', 'D (default)', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.dataColumnBox.addItems(self.columnList)
        self.dataColumnBox.setCurrentIndex(3)
        self.dataColumnBox.setFont(fontContent)
        layout.addWidget(self.dataColumnBox, 3, 8)

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

        self.btnOK = QtWidgets.QPushButton(self)  # 加入按鈕
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
        if self.filePath and (self.rb_single.isChecked() or self.rb_double.isChecked()):
            err_count = 0
            for file in self.filePath:
                path = file.rsplit('/', 1)[0] + '/'
                name = file.rsplit('/', 1)[-1]
                err = fetch.fetch(path, name, self.groupDirection.checkedId(), self.dataColumnBox.currentIndex())
                if err:
                    err_count += 1
            if err_count:
                QMessageBox.critical(None, 'Error', 'The selected Direction or Data column might not match the choosen file(s)!')
            else:
                QMessageBox.information(None, 'Message', 'Successfully generated!')

        elif not self.filePath:
            QMessageBox.warning(None, 'Warning', 'Choose at least one CSV file!')
        else:
            QMessageBox.warning(None, 'Warning', 'Choose Direction!')