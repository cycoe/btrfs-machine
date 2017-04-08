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
        self.homeMode = self.backend.loadVal()
        self.updateSnapList()

    def setupUi(self):
        self.setGeometry(self.x, self.y, self.windowWidth, self.windowHeight)
        self.centralWidget = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout()

        self.pageStack = QtWidgets.QStackedWidget()
        self.textBrowser = QtWidgets.QTextBrowser()
        self.textBrowser.setMinimumSize(QtCore.QSize(self.windowWidth, self.windowHeight // 3))
        self.gridLayout.addWidget(self.pageStack, 0, 0, 2, 1)
        self.gridLayout.addWidget(self.textBrowser, 2, 0, 3, 1)

        self.rootTable = QtWidgets.QTableWidget(len(self.rootSnapMat), len(self.rootSnapMat[0]))
        self.rootTable.setMinimumSize(QtCore.QSize(self.windowWidth, self.windowHeight * 2 // 3))
        self.rootTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.rootTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.homeTable = QtWidgets.QTableWidget(len(self.homeSnapMat), len(self.homeSnapMat[0]))
        self.homeTable.setMinimumSize(QtCore.QSize(self.windowWidth, self.windowHeight * 2 // 3))
        self.homeTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.homeTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.pageStack.addWidget(self.rootTable)
        self.pageStack.addWidget(self.homeTable)

        self.centralWidget.setLayout(self.gridLayout)
        self.setCentralWidget(self.centralWidget)
        self.setStatusBar(QtWidgets.QStatusBar(self))

        self.settingWindow = SettingWindow()

    def getScreenSize(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        return screen.width(), screen.height()

    def createActions(self):
        self.createRootAction = QtWidgets.QAction(QtGui.QIcon("icons/createRoot.png"), "createRootSnapshot", self)
        self.createHomeAction = QtWidgets.QAction(QtGui.QIcon("icons/createHome.png"), "createHomeSnapshot", self)
        self.deleteAction = QtWidgets.QAction(QtGui.QIcon("icons/delete.png"), "deleteSnapshot", self)
        self.exitAction = QtWidgets.QAction(QtGui.QIcon("icons/exit.png"), "exit", self)
        self.settingAction = QtWidgets.QAction(QtGui.QIcon("icons/settings.png"), "setting", self)
        self.aboutAction = QtWidgets.QAction("about", self)

        self.createRootAction.setStatusTip('Create a snapshot of root subvolume')
        self.createHomeAction.setStatusTip('Create a snapshot of home subvolume')
        self.deleteAction.setStatusTip('Delete selected snapshot')
        self.exitAction.setStatusTip('Exit')
        self.aboutAction.setStatusTip('Know more about Klone')
        self.settingAction.setStatusTip('Configuration')

    def createMenuBar(self):
        self.menuBar = QtWidgets.QMenuBar()
        #self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menuTools = QtWidgets.QMenu(self.menuBar)
        self.menuSetting = QtWidgets.QMenu(self.menuBar)
        self.setMenuBar(self.menuBar)

        self.menuTools.addAction(self.createRootAction)
        self.menuTools.addAction(self.createHomeAction)
        self.menuTools.addAction(self.exitAction)
        self.menuSetting.addAction(self.settingAction)
        self.menuSetting.addAction(self.aboutAction)
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuSetting.menuAction())

    def createToolBar(self):
        self.toolBar = QtWidgets.QToolBar(self)
        self.toolBar.setIconSize(QtCore.QSize(32, 32))
        self.switchBox = QtWidgets.QComboBox()
        self.switchBox.addItems(['/', '/home'])
        self.toolBar.addWidget(self.switchBox)
        self.toolBar.addAction(self.createRootAction)
        self.toolBar.addAction(self.createHomeAction)
        self.toolBar.addAction(self.deleteAction)
        self.toolBar.addAction(self.exitAction)


        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.insertToolBarBreak(self.toolBar)

    def createConnects(self):
        self.exitAction.triggered.connect(self.close)
        self.settingAction.triggered.connect(self.settingWindow.show)
        self.deleteAction.triggered.connect(self.deleteSnapshot)
        self.createRootAction.triggered.connect(self.createRootSnapshot)
        self.createHomeAction.triggered.connect(self.createHomeSnapshot)
        self.switchBox.activated.connect(self.changePage)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Klone"))
        self.menuTools.setTitle(_translate("MainWindow", "tools"))
        self.menuSetting.setTitle(_translate("MainWindow", "setting"))

    '''
    Slots
    '''

    @QtCore.pyqtSlot()
    def updateSnapList(self):
        if self.homeMode:
            self.snapLabels, self.rootSnapMat, self.homeSnapMat = self.backend.listSnapshot()
        else:
            self.snapLabels, self.rootSnapMat = self.backend.listSnapshot()

    @QtCore.pyqtSlot()
    def fillTable(self):
        self.rootTable.setHorizontalHeaderLabels(self.snapLabels)
        self.rootTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        #self.table.resizeColumnsToContents()
        self.rootTable.setColumnWidth(3, 400)
        for i in range(len(self.rootSnapMat)):
            for j in range(len(self.rootSnapMat[0])):
                self.rootTable.setItem(i, j, QtWidgets.QTableWidgetItem(self.rootSnapMat[i][j]))
        if self.homeMode:
            self.homeTable.setHorizontalHeaderLabels(self.snapLabels)
            self.homeTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            #self.table.resizeColumnsToContents()
            self.homeTable.setColumnWidth(3, 400)
            for i in range(len(self.homeSnapMat)):
                for j in range(len(self.homeSnapMat[0])):
                    self.homeTable.setItem(i, j, QtWidgets.QTableWidgetItem(self.homeSnapMat[i][j]))


    @QtCore.pyqtSlot()
    def deleteSnapshot(self):
        self.selectedSnap = self.table.currentRow()
        self.backend.deleteSnapshot(self.selectedSnap)
        self.rootTable.removeRow(self.selectedSnap)
        self.snapLabels, self.snapMat = self.backend.listSnapshot()
        self.fillTable()

    @QtCore.pyqtSlot()
    def createRootSnapshot(self):
        self.updateSnapList()
        self.rootTable.setRowCount(self.rootTable.rowCount() + 1)
        self.backend.createRootSnapshot()
        self.fillTable()

    @QtCore.pyqtSlot()
    def createHomeSnapshot(self):
        self.updateSnapList()
        self.homeTable.setRowCount(self.homeTable.rowCount() + 1)
        self.backend.createHomeSnapshot()
        self.fillTable()

    @QtCore.pyqtSlot(int)
    def changePage(self, pageNum):
        self.pageStack.setCurrentIndex(pageNum)


    '''
    Signals
    '''

    def closeEvent(self, event):
        self.backend.release()



class SettingWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(SettingWindow, self).__init__()
        self.createButtons()
        self.createTable()
        self.setupUi()
        self.retranslateUi()

    def setupUi(self):
        self.resize(QtCore.QSize(600, 400))
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.addWidget(self.table, 0, 0)
        self.gridLayout.addWidget(self.acceptButton, 3, 1)
        self.gridLayout.addWidget(self.applyButton, 3, 2)
        self.gridLayout.addWidget(self.cancelButton, 3, 3)

        self.centralWidget = QtWidgets.QWidget()
        self.centralWidget.setLayout(self.gridLayout)
        self.setCentralWidget(self.centralWidget)

    def createTable(self):
        self.table = QtWidgets.QTableWidget(2, 2)

    def createButtons(self):
        self.acceptButton = QtWidgets.QPushButton('Accept')
        self.applyButton = QtWidgets.QPushButton('Apply')
        self.cancelButton = QtWidgets.QPushButton('Cancel')
        self.acceptButton.setStyleSheet("QPushButton{color: red}")

    def retranslateUi(self):
        self.setWindowTitle("Setting")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
