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
        self.mode = self.backend.loadVal()
        self.updateSnapList()
        self.mountPoints = ['@', '@home']
        self.taskList = [self.backend.createRootSnapshot, self.backend.createHomeSnapshot]
        self.iconPath = 'asset/icons/'
        self.actionNameList = [
            "createRootSnapshot",
            "createHomeSnapshot",
            "deleteSnapshot",
            "settings",
            "about",
            "exit",
        ]
        self.tipList = [
            'Create a snapshot of root subvolume',
            'Create a snapshot of home subvolume',
            'Delete selected snapshot',
            'Configurations',
            'Know more about Klone',
            'Exit',
        ]

        self.backThread = BackThread()
        self.logger = LoggerThread()

    def setupUi(self):
        self.setGeometry(self.x, self.y, self.windowWidth, self.windowHeight)
        self.setWindowIcon(QtGui.QIcon('icons/icon.png'))
        self.centralWidget = QtWidgets.QWidget()
        self.gridLayout = QtWidgets.QGridLayout()
        self.pageTab = QtWidgets.QTabWidget()
        self.pageTab.setMinimumSize(QtCore.QSize(self.windowWidth, self.windowHeight * 2 // 3))
        self.textBrowser = QtWidgets.QTextBrowser()
        self.textBrowser.setMinimumSize(QtCore.QSize(self.windowWidth // 3 * 2, self.windowHeight // 3))
        self.gridLayout.addWidget(self.pageTab, 0, 0, 2, 3)
        self.gridLayout.addWidget(self.textBrowser, 2, 0, 3, 2)

        self.tableList = []
        for i in range(self.mode):
            table = QtWidgets.QTableWidget(len(self.snapMatList[i]), len(self.snapMatList[i][0]))
            table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            table.horizontalHeader().setStretchLastSection(True)
            self.pageTab.addTab(table, self.mountPoints[i])
            self.tableList.append(table)

        self.centralWidget.setLayout(self.gridLayout)
        self.setCentralWidget(self.centralWidget)
        self.setStatusBar(QtWidgets.QStatusBar(self))

        self.settingWindow = SettingWindow()

    def getScreenSize(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        return screen.width(), screen.height()

    def createActions(self):
        self.actionList = []
        for actionNum in range(len(self.actionNameList)):
            action = QtWidgets.QAction(QtGui.QIcon(self.iconPath + self.actionNameList[actionNum] + '.png'), self.actionNameList[actionNum], self)
            action.setStatusTip(self.tipList[actionNum])
            self.actionList.append(action)

    def createToolBar(self):
        self.toolBar = QtWidgets.QToolBar(self)
        self.toolBar.setIconSize(QtCore.QSize(32, 32))
        for action in self.actionList:
            self.toolBar.addAction(action)

        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.insertToolBarBreak(self.toolBar)

    def createConnects(self):
        self.connectList = [
            self.createSnapshot,
            self.createSnapshot,
            self.deleteSnapshot,
            self.settingWindow.show,
            self.temp,
            self.close,
        ]
        for actionNum in range(len(self.actionList)):
            self.actionList[actionNum].triggered.connect(self.connectList[actionNum])
        self.backThread.signal.connect(self.taskDone)
        self.logger.signal.connect(self.textBrowser.append)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Klone"))


    '''
    Slots
    '''

    @QtCore.pyqtSlot()
    def updateSnapList(self):
        if self.mode == 2:
            self.snapLabels, self.rootSnapMat, self.homeSnapMat = self.backend.listSnapshot()
            self.snapMatList = [self.rootSnapMat, self.homeSnapMat]
        else:
            self.snapLabels, self.rootSnapMat = self.backend.listSnapshot()
            self.snapMatList = [self.rootSnapMat]

    @QtCore.pyqtSlot()
    def fillTable(self):
        for tableID in range(len(self.tableList)):
            self.tableList[tableID].setHorizontalHeaderLabels(self.snapLabels)
            for i in range(len(self.snapMatList[tableID])):
                for j in range(len(self.snapMatList[tableID][0])):
                    self.tableList[tableID].setItem(i, j, QtWidgets.QTableWidgetItem(self.snapMatList[tableID][i][j]))


    @QtCore.pyqtSlot()
    def createSnapshot(self):
        self.logger.setText('creating snapshot of ' + self.mountPoints[0])
        self.logger.start()
        self.disableAllActions()
        self.backThread.setTask(self.taskList[0], 0)
        self.backThread.start()

    @QtCore.pyqtSlot(int)
    def taskDone(self, tableID):
        if tableID == 3:
            self.logger.setText('complete deleting')
            self.logger.start()
            self.enableAllActions()
            return
        self.tableList[tableID].setRowCount(self.tableList[tableID].rowCount() + 1)
        self.updateSnapList()
        self.fillTable()
        self.tableList[tableID].verticalScrollBar().setSliderPosition(self.tableList[tableID].rowCount())
        self.actionList[tableID].setEnabled(True)
        self.logger.setText('complete creating')
        self.logger.start()
        self.enableAllActions()


    @QtCore.pyqtSlot()
    def deleteSnapshot(self):
        tableID = self.pageTab.currentIndex()
        self.selectedSnap = self.tableList[tableID].currentRow()
        self.disableAllActions()
        self.logger.setText('deleting snapshot ' + self.snapMatList[tableID][self.selectedSnap][-1])
        self.logger.start()
        self.backThread.setTask(lambda x = self.selectedSnap: self.backend.deleteRootSnapshot(x), 3)
        self.backThread.start()
        self.tableList[tableID].removeRow(self.selectedSnap)
        self.fillTable()
        self.updateSnapList()

    @QtCore.pyqtSlot()
    def disableAllActions(self):
        for action in self.actionList:
            action.setDisabled(True)

    @QtCore.pyqtSlot()
    def enableAllActions(self):
        for action in self.actionList:
            action.setEnabled(True)

    @QtCore.pyqtSlot()
    def temp(self):
        pass


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


class BackThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(int)
    def __init__(self):
        super(BackThread, self).__init__()

    def setTask(self, task, processID):
        self.task = task
        self.processID = processID

    def run(self):
        self.task()
        self.signal.emit(self.processID)



class LoggerThread(QtCore.QThread):
    signal = QtCore.pyqtSignal(str)
    def __init__(self):
        super(LoggerThread, self).__init__()

    def setText(self, text):
        import time
        self.text = '\t'.join([time.strftime("%Y-%m-%d %H:%M:%S"), text])

    def run(self):
        self.signal.emit(self.text)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    #stylesheet = QtCore.QFile("stylesheet.qss")
    #stylesheet.open(QtCore.QIODevice.ReadOnly)
    #app.setStyleSheet(stylesheet.readAll().data().decode('utf-8'))

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
