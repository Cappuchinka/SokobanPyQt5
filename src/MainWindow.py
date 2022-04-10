import os

from PyQt5.QtCore import QModelIndex, QRectF

from MainWindowUI import Ui_MainWindow as MainWindowUI
from SokobanGame import *

from PyQt5 import QtSvg, Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QItemDelegate, QStyleOptionViewItem, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QPainter
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow, MainWindowUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Задание заголовка игры
        self.setWindowTitle("SokobanPyQt5")

        self._desktop = QApplication.desktop()
        self._screenRect = self._desktop.screenGeometry()
        self._height = self._screenRect.height()
        self._width = self._screenRect.width()
        # Задание размера окна игры.
        self.setGeometry(self._width / 4, self._height / 4, self.frameSize().width(), self.frameSize().height())
        self._levels = ['./resources/levels/level1.txt', './resources/levels/level2.txt',
                        './resources/levels/level3.txt', './resources/levels/level4.txt',
                        './resources/levels/level5.txt', './resources/levels/level6.txt',
                        './resources/levels/level7.txt', './resources/levels/level8.txt',
                        './resources/levels/level9.txt', './resources/levels/level10.txt'] # уровни игры

        images_dir = os.path.join(os.path.dirname(__file__), "./resources/textures")
        self._images = {
            os.path.splitext(f)[0]: QtSvg.QSvgRenderer(os.path.join(images_dir, f))
            for f in os.listdir(images_dir)
        }

        self._current_id_level = 0 # ID пути текущего уровня из списка уровней.
        self._current_level = self._levels[self._current_id_level] # Путь текущего уровня.

        self._game = SokobanGame()
        self._game.new_game(self._current_level)

        self.game_resize(self._game)

        class MyDelegate(QItemDelegate):
            def __init__(self, prnt=None, *args):
                QItemDelegate.__init__(self, prnt, *args)

            def paint(self, painter: QPainter, option: QStyleOptionViewItem, idx: QModelIndex):
                painter.save()
                self.parent().on_item_paint(idx, painter, option)
                painter.restore()

        self.tableView.setItemDelegate(MyDelegate(self))
        self.buttonPlayAgain.clicked.connect(self.on_new_game) # Обработчик событий кнопки "Play Again".


    """ Меняем размер окна в зависимости от размера уровня """
    def game_resize(self, game: SokobanGame) -> None:
        h = game.get_height()
        w = game.get_width()
        model = QStandardItemModel(h, w)
        self.tableView.setModel(model)
        self.tableView.setGeometry(10, 10, w * 81, h * 81)
        tvw = self.tableView.width()
        tvh = self.tableView.height()
        self.setGeometry(self._screenRect.width() / 4 + tvw / 2, self._screenRect.height() / 4, tvw + 15,
                         tvh + 90)
        self.horizontalLayoutWidget.setGeometry(10, self.tableView.height() + 15, self.horizontalLayoutWidget.width(),
                                                self.horizontalLayoutWidget.height())
        self.update_view()


    """ Запуск новой игры. """
    def on_new_game(self):
        self._game = SokobanGame()
        self._game.new_game(self._current_level)
        self.game_resize(self._game)
        self.update_view()


    """ Обновление экрана. """
    def update_view(self):
        self.tableView.viewport().update()


    """ Обработчик событий кнопок """
    def keyPressEvent(self, e):
        keyCode = e.key()
        ret = False
        if keyCode == Qt.Key_Left or keyCode == Qt.Key_A:
            ret = self._game.move(0, -1)
        elif keyCode == Qt.Key_Right or keyCode == Qt.Key_D:
            ret = self._game.move(0, 1)
        elif keyCode == Qt.Key_Up or keyCode == Qt.Key_W:
            ret = self._game.move(-1, 0)
        elif keyCode == Qt.Key_Down or keyCode == Qt.Key_S:
            ret = self._game.move(1, 0)
        else:
            pass

        if ret:
            self.on_item_paint(e)

        if self._game.is_win():
            button = QMessageBox.warning(self, "Предупреждение", u"Хотите перейти на следующий уровень??",
                                         QMessageBox.Ok | QMessageBox.No,
                                         QMessageBox.Ok)

            if button == QMessageBox.Ok:
                self._current_id_level += 1
                if self._current_id_level == len(self._levels):
                    msg = QMessageBox().warning(self, "Congratulations!", u"Вы прошли игру!",
                                                QMessageBox.Ok, QMessageBox.Ok)
                    if msg == QMessageBox.Ok:
                        exit(0)
                self._current_level = self._levels[self._current_id_level]
                self._game = SokobanGame()
                self._game.new_game(self._current_level)
                self.game_resize(self._game)
            else:
                self.on_new_game()


    """ Отрисовка элементов игры """
    def on_item_paint(self, e: QModelIndex, painter: QPainter, option: QStyleOptionViewItem) -> None:
        item = self._game.get_field(e.row(), e.column())
        if item == Field.WALL:
            img = self._images['wall']
        elif item == Field.BOX:
            img = self._images['box']
        else:
            img = self._images['floor']

        ep = Point(e.row(), e.column())
        np = self._game.now_point
        for i in range(len(self._game.finish_points)):
            fp = self._game.finish_points[i]
            if item == Field.VOID and (fp.equals(ep) and not fp.equals(np)):
                img = self._images['finish']

            elif item == Field.BOX and fp.equals(ep):
                img = self._images['box_finish']

            elif item == Field.VOID and (np.equals(ep) and not fp.equals(ep)):
                img = self._images['smile']

        if self._game.is_win() and np.equals(ep):
            img = self._images['win_smile']
        img.render(painter, QRectF(option.rect))
        self.update_view()