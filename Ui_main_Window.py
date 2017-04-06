# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cycoe/github/btrfs-machine/main_Window.ui'
#
# Created by: PyQt5 UI code generator 5.8
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtWidgets.QListView(self.centralWidget)
        self.listWidget.setMinimumSize(QtCore.QSize(0, 265))
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralWidget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menuBar.setObjectName("menuBar")
        self.menuTools = QtWidgets.QMenu(self.menuBar)
        self.menuTools.setObjectName("menuTools")
        self.menuSetting = QtWidgets.QMenu(self.menuBar)
        self.menuSetting.setObjectName("menuSetting")
        MainWindow.setMenuBar(self.menuBar)
        self.createSnapshotAct = QtWidgets.QAction(QtGui.QIcon("icons/create.png"), "createSnapshot", MainWindow)
        self.deleteSnapshotAct = QtWidgets.QAction(QtGui.QIcon("icons/delete.png"), "createSnapshot", MainWindow)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        self.toolBar.addAction(self.createSnapshotAct)
        self.toolBar.addAction(self.deleteSnapshotAct)
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        MainWindow.insertToolBarBreak(self.toolBar)
        
        self.buttonCreate = QtWidgets.QAction(self.createSnapshotAct)
        self.buttonCreate.setObjectName("buttonCreate")
        self.buttonExit = QtWidgets.QAction(MainWindow)
        self.buttonExit.setObjectName("buttonExit")
        self.buttonSetting = QtWidgets.QAction(MainWindow)
        self.buttonSetting.setObjectName("buttonSetting")
        self.buttonAbout = QtWidgets.QAction(MainWindow)
        self.buttonAbout.setObjectName("buttonAbout")
        self.menuTools.addAction(self.buttonCreate)
        self.menuTools.addAction(self.buttonExit)
        self.menuSetting.addAction(self.buttonSetting)
        self.menuSetting.addAction(self.buttonAbout)
        self.menuBar.addAction(self.menuTools.menuAction())
        self.menuBar.addAction(self.menuSetting.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Klone"))
        self.menuTools.setTitle(_translate("MainWindow", "工具"))
        self.menuSetting.setTitle(_translate("MainWindow", "设置"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.buttonCreate.setText(_translate("MainWindow", "创建备份"))
        self.buttonExit.setText(_translate("MainWindow", "退出"))
        self.buttonSetting.setText(_translate("MainWindow", "设置"))
        self.buttonAbout.setText(_translate("MainWindow", "关于"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

