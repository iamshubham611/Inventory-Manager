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

class AddMember(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Member")
        #self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,350,550)
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        ###################### Widgets of top Layout ################
        self.addMemberImg=QLabel()
        self.img=QPixmap("icons/addmember.png")
        self.addMemberImg.setPixmap(self.img)
        self.addMemberImg.setAlignment(Qt.AlignCenter)
        self.tittleText=QLabel("Add Member")
        self.tittleText.setAlignment(Qt.AlignCenter)
        ####################### Widgets of bottom Layout ############
        self.nameEntry=QLineEdit()
        self.nameEntry.setPlaceholderText("Enter Name")
        self.ssoEntry = QLineEdit()
        self.ssoEntry.setPlaceholderText("Enter SSO")
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setPlaceholderText("Enter Phone/Email")
        self.submitBtn=QPushButton("Submit")
        self.submitBtn.clicked.connect(self.submitMember)




    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QVBoxLayout()
        self.bottomLayout=QFormLayout()
        self.topFrame=QFrame()
        self.topFrame.setStyleSheet(style.addMemberTopFrame())
        self.bottomFrame=QFrame()
        self.bottomFrame.setStyleSheet(style.addMemberBottomFrame())
        ################### add Widgets######################
        self.topLayout.addWidget(self.tittleText)
        self.topLayout.addWidget(self.addMemberImg)
        self.topFrame.setLayout(self.topLayout)
        self.bottomLayout.addRow(QLabel("Name*: "),self.nameEntry)
        self.bottomLayout.addRow(QLabel("SSO: "), self.ssoEntry)
        self.bottomLayout.addRow(QLabel("Phone/Email*: "), self.phoneEntry)
        self.bottomLayout.addRow(QLabel(""), self.submitBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def submitMember(self):
        name=self.nameEntry.text()
        sso=self.ssoEntry.text()
        phone=self.phoneEntry.text()


        if (name and phone !=""):
            try:
                query="INSERT into 'members' (member_name,member_sso,member_phone) VALUES (?,?,?)"
                cur.execute(query,(name,sso,phone))
                con.commit()
                QMessageBox.information(self,"Info","Member has been Added!!!")
                self.nameEntry.setText("")
                self.ssoEntry.setText("")
                self.phoneEntry.setText("")

            except:
                QMessageBox.information(self, "Info", "Member has not been Added!!!")

        else:
            QMessageBox.information(self,"Info","Field can not be empty")