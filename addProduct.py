import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
from PIL import Image
import os
import style

con=sqlite3.connect("products.db")
cur=con.cursor()

defaultImg="store.png"

class AddProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Product")
        #self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,450,650)
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()


    def widgets(self):
        ###################### Top Layout Widgets ###################
        self.addProductImg=QLabel()
        self.img=QPixmap("icons/addproduct.png")
        self.addProductImg.setPixmap(self.img)
        self.tittleText=QLabel("Add Product")
        ###################### Bottom Layout Widgets ###################
        self.serialEntry=QLineEdit()
        self.serialEntry.setPlaceholderText("Enter Serial Number")
        self.nameEntry = QLineEdit()
        self.nameEntry.setPlaceholderText("Enter Module Name")
        self.detailEntry = QLineEdit()
        self.detailEntry.setPlaceholderText("Enter Description")
        self.boeEntry = QLineEdit()
        self.boeEntry.setPlaceholderText("Enter BOE#/PO#")
        self.ownerEntry = QComboBox()
        #self.ownerEntry.setPlaceholderText("Enter Owner")
        query2 = ("SELECT member_id, member_name FROM members")
        members = cur.execute(query2).fetchall()
        for member in members:
            self.ownerEntry.addItem(member[1], member[0])

        self.storedEntry = QLineEdit()
        self.storedEntry.setPlaceholderText("Enter Stored Location")
        self.uploadBtn=QPushButton("Upload")
        self.uploadBtn.clicked.connect(self.uploadImg)
        self.submitBtn=QPushButton("Submit")
        self.submitBtn.clicked.connect(self.submitProduct)


    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QHBoxLayout()
        self.bottomLayout=QFormLayout()
        self.topFrame=QFrame()
        self.topFrame.setStyleSheet(style.addProductTopFrame())
        self.bottomFrame=QFrame()
        self.bottomFrame.setStyleSheet(style.addProductBottomFrame())
        ############### Add widgets############
        ############### widgets of top layout #########
        self.topLayout.addWidget(self.addProductImg)
        self.topLayout.addWidget(self.tittleText)
        self.topFrame.setLayout(self.topLayout)
        ################## Widgets of form layout ###########
        self.bottomLayout.addRow(QLabel("Serial Number*: "),self.serialEntry)
        self.bottomLayout.addRow(QLabel("Module Name*: "),self.nameEntry)
        self.bottomLayout.addRow(QLabel("Description: "),self.detailEntry)
        self.bottomLayout.addRow(QLabel("BOE#/PO#*: "),self.boeEntry)
        self.bottomLayout.addRow(QLabel("Owner*: "),self.ownerEntry)
        self.bottomLayout.addRow(QLabel("Stored Location: "),self.storedEntry)
        self.bottomLayout.addRow(QLabel("Upload: "),self.uploadBtn)
        self.bottomLayout.addRow(QLabel(""),self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)


    def uploadImg(self):
        global defaultImg
        size=(256,256)
        self.filename,ok=QFileDialog.getOpenFileName(self,"Upload Image","","Image Files (*.jpg *.png)")
        if ok:
            #print(self.filename)
            defaultImg=os.path.basename(self.filename)
            #print(defaultImg)
            img=Image.open(self.filename)
            img=img.resize(size)
            img.save("img/{}".format(defaultImg))

    def submitProduct(self):
        global defaultImg
        serial=self.serialEntry.text()
        name=self.nameEntry.text()
        detail=self.detailEntry.text()
        boe=self.boeEntry.text()
        owner=self.ownerEntry.currentText()
        stored=self.storedEntry.text()

        if (serial and name and boe and owner !=""):
            try:
                query="INSERT INTO 'products' (serial_number,module,description,boe,owner,stored_location,product_img) VALUES (?,?,?,?,?,?,?)"
                cur.execute(query,(serial,name,detail,boe,owner,stored,defaultImg))
                con.commit()
                QMessageBox.information(self,"Info","Product has been added")


            except:
                QMessageBox.information(self, "Info", "Product has not been added")
        else:
            QMessageBox.information(self, "Info", "Fields can not be empty!!!")
