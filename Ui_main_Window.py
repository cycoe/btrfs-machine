# /usr/bin/python
# -*- coding: utf-8 -*-

# run with kdesu

from PyQt5 import QtCore, QtGui, QtWidgets
from backend import Backend

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initVar()
        self.createActions()
        self.createMenuBar()
        self.createToolBar()
        self.setupUi()
        self.retranslateUi()
        self.createConnects()
        self.fillTable()


    def initVar(self):
        self.screenWidth, self.screenHeight = self.getScreenSize()
        self.windowWidth = 800
        self.windowHeight = 400
        self.x = (self.screenWidth - self.windowWidth) // 2
        self.y = (self.screenHeight - self.windowHeight) // 2
        self.readConfig = True
        self.selectedSnap = -1

        self.backend = Backend()
        self.backend.loadVal()
        self.snapLabels, self.snapMat = self.backend.listSnapshot()
        print(self.snapMat)
        self.tableWidth = len(self.snapMat[0])
        self.tableHeight = len(self.snapMat)

    def setupUi(self):
        self.setGeometry(self.x, self.y, self.windowWidth, self.windowHeight)
        self.centralWidget = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout()
        self.table = QtWidgets.QTableWidget(self.tableHeight, self.tableWidth)
        self.table.setMinimumSize(QtCore.QSize(self.windowWidth, self.windowHeight * 2 // 3))
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.gridLayout.addWidget(self.table, 0, 0)
        self.textBrowser = QtWidgets.QTextBrowser()
        self.textBrowser.setMinimumSize(QtCore.QSize(self.windowWidth, self.windowHeight // 3))
        self.gridLayout.addWidget(self.textBrowser, 2, 0, 3, 0)
        self.centralWidget.setLayout(self.gridLayout)
        self.setCentralWidget(self.centralWidget)

        self.settingWindow = SettingWindow()

    def getScreenSize(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        return screen.width(), screen.height()

    def createActions(self):
        self.createAction = QtWidgets.QAction(QtGui.QIcon("icons/create.png"), "createSnapshot", self)
        self.deleteAction = QtWidgets.QAction(QtGui.QIcon("icons/delete.png"), "deleteSnapshot", self)
        self.exitAction = QtWidgets.QAction("exit", self)
        self.aboutAction = QtWidgets.QAction("about", self)
        self.settingAction = QtWidgets.QAction("setting", self)

    def createMenuBar(self):
        self.menuBar = QtWidgets.QMenuBar()
        #self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menuTools = QtWidgets.QMenu(self.menuBar)
        self.menuSetting = QtWidgets.QMenu(self.menuBar)
        self.setMenuBar(self.menuBar)

        self.menuTools.addAction(self.createAction)
        self.menuTools.addAction(self.exitAction)
        self.menuTools.addAction(self.exitAction)
        self.menuSetting.addAction(self.settingAction)
        self.menuSetting.addAction(self.aboutAction)
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuSetting.menuAction())

    def createToolBar(self):
        self.toolBar = QtWidgets.QToolBar(self)
        self.toolBar.addAction(self.createAction)
        self.toolBar.addAction(self.deleteAction)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.insertToolBarBreak(self.toolBar)

    def createConnects(self):
        self.exitAction.triggered.connect(self.close)
        self.settingAction.triggered.connect(self.settingWindow.show)
        self.deleteAction.triggered.connect(self.deleteSnapshot)
        self.createAction.triggered.connect(self.createSnapshot)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Klone"))
        self.menuTools.setTitle(_translate("MainWindow", "tools"))
        self.menuSetting.setTitle(_translate("MainWindow", "setting"))

    '''
    Slots
    '''

    @QtCore.pyqtSlot()
    def fillTable(self):
        self.table.setHorizontalHeaderLabels(self.snapLabels)
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        #self.table.resizeColumnsToContents()
        self.table.setColumnWidth(3, 400)
        for i in range(len(self.snapMat)):
            for j in range(len(self.snapMat[0])):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(self.snapMat[i][j]))

    @QtCore.pyqtSlot()
    def deleteSnapshot(self):
        self.selectedSnap = self.table.currentRow()
        self.backend.deleteSnapshot(self.selectedSnap)
        self.table.removeRow(self.selectedSnap)

    @QtCore.pyqtSlot()
    def createSnapshot(self):
        self.snapLabels, self.snapMat = self.backend.createSnapshot()
        self.table.setRowCount(self.table.rowCount() + 1)
        self.fillTable()


    '''
    Signals
    '''

    def closeEvent(self, event):
        self.backend.release()



class SettingWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(SettingWindow, self).__init__()
        self.setupUi()
        self.createButtons()
        self.retranslateUi()

    def setupUi(self):
        self.resize(QtCore.QSize(600, 400))

    def createButtons(self):
        pass

    def retranslateUi(self):
        self.setWindowTitle("Setting")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
