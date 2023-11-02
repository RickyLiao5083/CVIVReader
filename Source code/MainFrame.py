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
        self.setWindowTitle('C-V & I-V Reader')
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

        self.CVIVLabel = QLabel('C-V / I-V:', self)
        self.CVIVLabel.setFont(fontTitle)
        layout.addWidget(self.CVIVLabel, 2, 7)

        self.rb_CV = QRadioButton(self)
        self.rb_CV.setText('C-V')
        self.rb_CV.setFont(fontContent)
        layout.addWidget(self.rb_CV, 2, 8)
        self.rb_IV = QRadioButton(self)
        self.rb_IV.setText('I-V')
        self.rb_IV.setFont(fontContent)
        self.rb_IV.clicked.connect(self.IVClicked)
        self.rb_CV.clicked.connect(self.CVClicked)
        layout.addWidget(self.rb_IV, 2, 9)

        self.groupCVIV = QButtonGroup(self)
        self.groupCVIV.addButton(self.rb_CV, 1)
        self.groupCVIV.addButton(self.rb_IV, 0)

        self.directionLabel = QLabel('Direction:', self)
        self.directionLabel.setFont(fontTitle)
        layout.addWidget(self.directionLabel, 3, 7)

        self.rb_single = QRadioButton(self)
        self.rb_single.setText('single')
        self.rb_single.setFont(fontContent)
        self.rb_single.setChecked(True)
        layout.addWidget(self.rb_single, 3, 8)
        self.rb_double = QRadioButton(self)
        self.rb_double.setText('double')
        self.rb_double.setFont(fontContent)
        layout.addWidget(self.rb_double, 3, 9)

        self.groupDirection = QButtonGroup(self)
        self.groupDirection.addButton(self.rb_single, 0)
        self.groupDirection.addButton(self.rb_double, 1)


        self.myLabel1 = QLabel('NTU GIEE', self)
        self.myLabel1.setFont(fontProperty)
        layout.addWidget(self.myLabel1, 2, 0)

        self.myLabel2 = QLabel('C-V Lab', self)
        self.myLabel2.setFont(fontProperty)
        layout.addWidget(self.myLabel2, 3, 0)

        self.myLabel3 = QLabel('Developed by W.C, Liao                                                                          '
                               '                   Please visit: \"https://github.com/RickyLiao5083/CVIVReader\" for more information.', self)
        self.myLabel3.setFont(fontProperty)
        layout.addWidget(self.myLabel3, 4, 0)


        self.btnOK = QtWidgets.QPushButton(self)  # 加入按鈕
        self.btnOK.setText('確定')
        self.btnOK.setFont(fontTitle)
        self.btnOK.clicked.connect(self.OK)
        layout.addWidget(self.btnOK, 4, 7)

    def IVClicked(self):
        self.rb_double.setChecked(True)
        self.rb_single.setDisabled(True)

    def CVClicked(self):
        self.rb_single.setDisabled(False)

    def open(self):
        self.filePath, filterType = QtWidgets.QFileDialog.getOpenFileNames(filter='CSV (*.csv)')  # 選擇檔案對話視窗
        print(self.filePath, filterType)
        allFiles = ''
        for fp in self.filePath:
            allFiles += (fp + '\n')
        self.fileInput.setPlainText(allFiles.strip())

    def OK(self):
        if self.filePath and (self.rb_CV.isChecked() or self.rb_IV.isChecked()):
            err_count = 0
            for file in self.filePath:
                path = file.rsplit('/', 1)[0] + '/'
                name = file.rsplit('/', 1)[-1]
                err = fetch.fetch(path, name, self.groupCVIV.checkedId(), self.groupDirection.checkedId())
                if err:
                    err_count += 1
            if err_count:
                QMessageBox.warning(None, 'Error', 'The selection of C-V / I-V or Direction might not match the choosen file(s)!')
            else:
                QMessageBox.information(None, 'Message', 'Successfully generated!')

        elif not self.filePath:
            QMessageBox.warning(None, 'Error', 'Choose at least one C-V or I-V file!')
        else:
            QMessageBox.warning(None, 'Error', 'Choose C-V or I-V!')