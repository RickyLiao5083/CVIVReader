import sys
from PyQt5.QtWidgets import (QApplication)

from MainFrame import MainFrame

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainFrame()
    w.show()
    sys.exit(app.exec_())