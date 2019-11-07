import sys
import os
from PyQt4 import QtCore, QtGui


class main_list_widget(QtGui.QListWidget):
    def __init__(self,type,parent=None):
        super(main_list_widget,self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self,event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self,event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self,event):

        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links=[]
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.emit(QtCore.SIGNAL("dropped"),links)
        else:
            event.ignore()


class MainForm(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(MainForm,self).__init__(parent)

        wid = QtGui.QWidget(self)
        self.setCentralWidget(wid)
        layout = QtGui.QVBoxLayout()
        wid.setLayout(layout)
        #
        self.label1 = QtGui.QLabel("Drag drop folder to below (new file will replace old one) :")
        #
        self.folder_list_widget=main_list_widget(self)
        self.connect(self.folder_list_widget,QtCore.SIGNAL("dropped"),self.object_dropped)
        #
        self.resize_button = QtGui.QPushButton(self)
        self.resize_button.setText("Resize images (on it's own folder)")
        self.connect(self.resize_button,QtCore.SIGNAL("clicked()"),self.do_resize)
        #
        self.remove_selected_button=QtGui.QPushButton(self)
        self.remove_selected_button.setText("Remove Selected")
        self.connect(self.remove_selected_button,QtCore.SIGNAL("clicked()"),self.do_remove_selected)
        #
        layout.addWidget(self.label1)
        layout.addWidget(self.folder_list_widget)
        layout.addWidget(self.remove_selected_button)
        layout.addWidget(self.resize_button)

    def do_remove_selected(self):
        list_items = self.folder_list_widget.selectedItems()
        if not list_items:
            return

        for item in list_items:
            self.folder_list_widget.takeItem(self.folder_list_widget.row(item))

    def do_resize(self):

        items=[]
        for index in xrange(self.folder_list_widget.count()):
            items.append(str(self.folder_list_widget.item(index).text()))

        for i in items:
            arg = r'-ratio -rtype lanczos -rflag decr -resize 50%% 50%% -overwrite {}/*.png'.format(i)
            os.system("X:/UNITY/XnView/nconvert.exe " + arg)

        qm=QtGui.QMessageBox()
        qm.question(self,'Info',"Done")
        qm.show()

    def object_dropped(self,l):
        for url in l:
            if os.path.exists(url):
                print(url)
                item=QtGui.QListWidgetItem(url,self.folder_list_widget)
                item.setStatusTip(url)


def main():
    app=QtGui.QApplication(sys.argv)
    form=MainForm()
    form.show()
    app.exec_()


if __name__=='__main__':
    main()