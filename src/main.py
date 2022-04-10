import sys
import traceback

from MainWindow import MainWindow

from PyQt5.QtWidgets import QApplication, QMessageBox


def main():
    app = QApplication(sys.argv)
    mw = MainWindow()

    def exception_hook(type_, value, tb):
        msg = '\n'.join(traceback.format_exception(type_, value, tb))
        # print(msg)
        QMessageBox.critical(mw, 'Unhandled top level exception', msg)

    sys.excepthook = exception_hook

    mw.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
