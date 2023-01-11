import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QPushButton

def on_click():
    subprocess.run(["python", "mon_script.py"])

app = QApplication(sys.argv)
button = QPushButton("Lancer le script")
button.clicked.connect(on_click)
button.show()

sys.exit(app.exec_())