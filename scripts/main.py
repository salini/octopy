
import os
import sys

from PyQt4 import QtGui

from myProject.widgets import SimpleWidget


def main():
    app = QtGui.QApplication(sys.argv)

    widget = SimpleWidget()
    widget.show()

    app.exec_()


if __name__ == "__main__":
    main()

