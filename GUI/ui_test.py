import sys
from PyQt5 import QtWidgets, uic

app = QtWidgets.QApplication(sys.argv)
window = uic.loadUi("./GUI/test.ui")
window.show()
sys.exit(app.exec_())