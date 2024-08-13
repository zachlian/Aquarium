import sys
from PyQt5.QtWidgets import QApplication
from window import MyWindow

def main():
    app = QApplication(sys.argv)
    ex = MyWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()