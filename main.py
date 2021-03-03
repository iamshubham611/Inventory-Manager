import sys,os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import sqlite3
import addProduct,addmember,style
from PIL import Image
con=sqlite3.connect("products.db")
cur=con.cursor()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Emerson HYD Inventory Manager")
        #self.setWindowIcon(QIcon('icons/icon.ico'))
        self.setGeometry(450,150,1350,750)

        self.UI()
        self.show()

    def UI(self):
        self.toolBar()
        self.tabWidget()
        self.widgets()
        self.layouts()
        self.displayProducts()
        self.displayMembers()
        self.getStatistics()

    def toolBar(self):
        self.tb=self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        ############################## Toolbar Buttons ####################
        ############################## Add Product #######################
        self.addProduct=QAction(QIcon('icons/add.png'),"Add Product",self)
        self.tb.addAction(self.addProduct)
        self.addProduct.triggered.connect(self.funcAddProduct)
        self.tb.addSeparator()
        ############################## Add Member #########################
        self.addMember=QAction(QIcon('icons/users.png'),"Add Member",self)
        self.tb.addAction(self.addMember)
        self.addMember.triggered.connect(self.funcAddMember)
        self.tb.addSeparator()

    def tabWidget(self):
        self.tabs=QTabWidget()
        self.tabs.blockSignals(True)
        self.tabs.currentChanged.connect(self.tabChanged)
        self.setCentralWidget(self.tabs)  ####to dispaly tabs######
        self.tab1=QWidget()
        self.tab2=QWidget()
        self.tab3=QWidget()
        self.tabs.addTab(self.tab1,"Products")
        self.tabs.addTab(self.tab2,"Members")
        self.tabs.addTab(self.tab3,"Statistics")

    def widgets(self):
        ####################################### Tab1 Widgets ####################
        ###################################### Main Left layout widget ###########
        self.productsTable=QTableWidget()
        self.productsTable.setColumnCount(8)
        #self.productsTable.setColumnHidden(0,True)  #### To hide coloumn 0 #######
        self.productsTable.setHorizontalHeaderItem(0,QTableWidgetItem("Serial No"))
        self.productsTable.setHorizontalHeaderItem(1,QTableWidgetItem("Module Name"))
        self.productsTable.setHorizontalHeaderItem(2,QTableWidgetItem("Description"))
        self.productsTable.setHorizontalHeaderItem(3,QTableWidgetItem("BOE#/PO#"))
        self.productsTable.setHorizontalHeaderItem(4,QTableWidgetItem("Owner"))
        self.productsTable.setHorizontalHeaderItem(5,QTableWidgetItem("Availability"))
        self.productsTable.setHorizontalHeaderItem(6,QTableWidgetItem("Stored Loc"))
        self.productsTable.setHorizontalHeaderItem(7,QTableWidgetItem("Fixture Loc"))
        self.productsTable.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        self.productsTable.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        self.productsTable.horizontalHeader().setSectionResizeMode(4,QHeaderView.Stretch)
        self.productsTable.horizontalHeader().setSectionResizeMode(6,QHeaderView.Stretch)
        self.productsTable.horizontalHeader().setSectionResizeMode(7,QHeaderView.Stretch)
        self.productsTable.doubleClicked.connect(self.selectedProduct)

        ####################### Right top layout widgets #######################
        self.searchText=QLabel("Search")
        self.searchEntry=QLineEdit()
        self.searchEntry.setPlaceholderText("Search for Product")
        self.searchButton=QPushButton("Search")
        self.searchButton.clicked.connect(self.searachProducts)
        self.searchButton.setStyleSheet(style.searchButtonStyle())

        ###################### Right midddle layout widgets ######
        self.allProduts = QRadioButton("All Products")
        self.availableProducts = QRadioButton("Available Products")
        self.notAvailableProducts = QRadioButton("Not Available Products")
        self.listButton=QPushButton("List")
        self.listButton.clicked.connect(self.listProducts)
        self.listButton.setStyleSheet(style.listButtonStyle())

        ###################### Tab 2 Widgets ###########################
        self.membersTable=QTableWidget()
        self.membersTable.setColumnCount(4)
        self.membersTable.setHorizontalHeaderItem(0,QTableWidgetItem("Member ID"))
        self.membersTable.setHorizontalHeaderItem(1,QTableWidgetItem("Member Name"))
        self.membersTable.setHorizontalHeaderItem(2,QTableWidgetItem("Member SSO"))
        self.membersTable.setHorizontalHeaderItem(3,QTableWidgetItem("Phone/Email"))
        self.membersTable.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
        self.membersTable.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
        self.membersTable.horizontalHeader().setSectionResizeMode(3,QHeaderView.Stretch)
        self.membersTable.doubleClicked.connect(self.selectedMember)
        self.memberSearchText=QLabel("Search Members")
        self.memberSerachEntry=QLineEdit()
        self.memberSearchButton=QPushButton("Search ")
        self.memberSearchButton.clicked.connect(self.serachMembers)

        ########################### TAB 3 Wiwgets ########################
        self.totalProductsLabel=QLabel()
        self.totalMembersLabel=QLabel()
        self.totalAvailableProductsLabel=QLabel()
        self.totalUnavailableProdutsLabel=QLabel()

    def layouts(self):
        ################### Tab1 Layouts ################:
        self.mainLayout=QHBoxLayout()
        self.mainLeftLayout=QVBoxLayout()
        self.mainRightLayout=QVBoxLayout()
        self.rightTopLayout=QHBoxLayout()
        self.rightMiddleLayout=QHBoxLayout()
        self.rightBottomLayout=QHBoxLayout()
        self.topGroupBox=QGroupBox("Search Box")
        self.topGroupBox.setStyleSheet(style.searchBoxStyle())
        self.middleGroupBox=QGroupBox("List Box")
        self.middleGroupBox.setStyleSheet(style.listBoxStyle())
        self.bottomGroupBox=QGroupBox()

        ##################### Add Widgets##################
        ##################### Left main Layout widgets ##############

        self.mainLeftLayout.addWidget(self.productsTable)

        ################### Right top layout widgets ########
        self.rightTopLayout.addWidget(self.searchText)
        self.rightTopLayout.addWidget(self.searchEntry)
        self.rightTopLayout.addWidget(self.searchButton)
        self.topGroupBox.setLayout(self.rightTopLayout)

        ################# Right Middle Layout widgets ########
        self.rightMiddleLayout.addWidget(self.allProduts)
        self.rightMiddleLayout.addWidget(self.availableProducts)
        self.rightMiddleLayout.addWidget(self.notAvailableProducts)
        self.rightMiddleLayout.addWidget(self.listButton)
        self.middleGroupBox.setLayout(self.rightMiddleLayout)

        self.mainRightLayout.addWidget(self.topGroupBox,20)
        self.mainRightLayout.addWidget(self.middleGroupBox,20)
        self.mainRightLayout.addWidget(self.bottomGroupBox,60)
        self.mainLayout.addLayout(self.mainLeftLayout,80)
        self.mainLayout.addLayout(self.mainRightLayout,20)
        self.tab1.setLayout(self.mainLayout)

    ############################ Tab 2 Layouts #################
        self.memberMainLayout=QHBoxLayout()
        self.memberLeftLayout=QHBoxLayout()
        self.memberRightLayout=QHBoxLayout()
        self.memberRightGroupBox=QGroupBox("Search For Members")
        self.memberRightGroupBox.setContentsMargins(10,10,10,600)
        self.memberRightLayout.addWidget(self.memberSearchText)
        self.memberRightLayout.addWidget(self.memberSerachEntry)
        self.memberRightLayout.addWidget(self.memberSearchButton)
        self.memberRightGroupBox.setLayout(self.memberRightLayout)

        self.memberLeftLayout.addWidget(self.membersTable)
        self.memberMainLayout.addLayout(self.memberLeftLayout,70)
        self.memberMainLayout.addWidget(self.memberRightGroupBox,30)
        self.tab2.setLayout(self.memberMainLayout)

        ################## Tab3 Layouts ###########################
        self.statisticsMainLayout=QVBoxLayout()
        self.statisticsLayout=QFormLayout()
        self.statistictsGroupBox=QGroupBox("Statistics")
        self.statisticsLayout.addRow(QLabel("Total Products: "),self.totalProductsLabel)
        self.statisticsLayout.addRow(QLabel("Total Members: "),self.totalMembersLabel)
        self.statisticsLayout.addRow(QLabel("Available Products: "),self.totalAvailableProductsLabel)
        self.statisticsLayout.addRow(QLabel("Unavailable Products: "),self.totalUnavailableProdutsLabel)

        self.statistictsGroupBox.setLayout(self.statisticsLayout)
        self.statistictsGroupBox.setFont(QFont("Arial",16))
        self.statisticsMainLayout.addWidget(self.statistictsGroupBox)
        self.tab3.setLayout(self.statisticsMainLayout)
        self.tabs.blockSignals(False)

    def funcAddProduct(self):
        self.newProduct=addProduct.AddProduct()
    def funcAddMember(self):
        self.newMember=addmember.AddMember()
    def displayProducts(self):
        self.productsTable.setFont(QFont("Times",12))
        for i in reversed(range(self.productsTable.rowCount())):
            self.productsTable.removeRow(i)

        query=cur.execute("SELECT serial_number,module,description,boe,owner,module_availability,stored_location,fixture_location FROM 'products'")
        for row_data in query:
            row_number=self.productsTable.rowCount()
            self.productsTable.insertRow(row_number)
            for coloumn_number, data in enumerate(row_data):
                self.productsTable.setItem(row_number,coloumn_number,QTableWidgetItem(str(data)))

        self.productsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
    def displayMembers(self):
        self.membersTable.setFont(QFont("Times",12))
        for i in reversed(range(self.membersTable.rowCount())):
            self.membersTable.removeRow(i)

        members=cur.execute("SELECT * FROM members")
        for row_data in members:
            row_number=self.membersTable.rowCount()
            self.membersTable.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.membersTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        self.membersTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def selectedProduct(self):
        global productId
        listProduct=[]
        for i in range(0,8):
            listProduct.append(self.productsTable.item(self.productsTable.currentRow(),i).text())
        #print(listProduct)
        productId=listProduct[0]
        self.display=DisplayProduct()
        self.display.show()

    def selectedMember(self):
        global memberId
        listMember=[]
        for i in range(0,4):
            listMember.append(self.membersTable.item(self.membersTable.currentRow(),i).text())
        #print(listMember)
        memberId=listMember[0]
        self.displayMember=DisplayMember()
        self.displayMember.show()

    def searachProducts(self):
        value=self.searchEntry.text()
        if value=="":
            QMessageBox.information(self,"Warning","Serach query can not be empty!!!")
        else:
            self.searchEntry.setText("")

            query=("SELECT serial_number,module,description,boe,owner,module_availability,stored_location,fixture_location FROM products WHERE module LIKE ? or boe LIKE ? or owner LIKE ?")
            results=cur.execute(query,('%' + value + '%','%'+ value + '%','%'+ value + '%')).fetchall()
            #print(results)

            if results==[]:
                QMessageBox.information(self,"Warning","There is no such a product or manufacturer")
            else:
                for i in reversed(range(self.productsTable.rowCount())):
                    self.productsTable.removeRow(i)
                for row_data in results:
                    row_number=self.productsTable.rowCount()
                    self.productsTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.productsTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))

    def serachMembers(self):
        value=self.memberSerachEntry.text()
        if value=="":
            QMessageBox.information(self,"Warning","Search query can not be empty")
        else:
            self.memberSerachEntry.setText("")
            query=("SELECT * FROM members WHERE member_name LIKE ? or member_sso LIKE ? or member_phone LIKE ?")
            results=cur.execute(query,('%' + value + '%','%' + value + '%','%' + value + '%')).fetchall()
            #print(results)
            if results == []:
                QMessageBox.information(self, "Warning", "There is no such a member")
            else:
                for i in reversed(range(self.membersTable.rowCount())):
                    self.membersTable.removeRow(i)
                for row_data in results:
                    row_number=self.membersTable.rowCount()
                    self.membersTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.membersTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))

    def listProducts(self):
        if self.allProduts.isChecked()==True:
            self.displayProducts()
        elif self.availableProducts.isChecked():
            query=("SELECT serial_number,module,description,boe,owner,module_availability,stored_location,fixture_location FROM products WHERE module_availability='Available'")
            products=cur.execute(query).fetchall()
            #print(products)
            for i in reversed(range(self.productsTable.rowCount())):
                self.productsTable.removeRow(i)
            for row_data in products:
                row_number=self.productsTable.rowCount()
                self.productsTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.productsTable.setItem(row_number,column_number,QTableWidgetItem(str(data)))
        elif self.notAvailableProducts.isChecked():
            query = ("SELECT serial_number,module,description,boe,owner,module_availability,stored_location,fixture_location FROM products WHERE module_availability='Unavailable'")
            products = cur.execute(query).fetchall()
            # print(products)
            for i in reversed(range(self.productsTable.rowCount())):
                self.productsTable.removeRow(i)
            for row_data in products:
                row_number = self.productsTable.rowCount()
                self.productsTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.productsTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def getStatistics(self):
        countProducts=cur.execute("SELECT count(serial_number) FROM products").fetchall()
        countMembers=cur.execute("SELECT count(member_id) FROM members").fetchall()
        countMembers=countMembers[0][0]
        totalAvailableProdutcs=cur.execute("SELECT count(module_availability) FROM products WHERE module_availability='Available'").fetchall()
        availbaleProducts=totalAvailableProdutcs[0][0]
        totalUnvailableProdutcs = cur.execute("SELECT count(module_availability) FROM products WHERE module_availability='Unavailable'").fetchall()
        unavailableProducts = totalUnvailableProdutcs[0][0]
        #totalAmount=cur.execute("SELECT SUM(selling_amount) FROM sellings").fetchall()
        #totalAmount=totalAmount[0][0]
        #print(countProducts)
        countProducts=countProducts[0][0]
        self.totalProductsLabel.setText(str(countProducts))
        self.totalMembersLabel.setText(str(countMembers))
        self.totalAvailableProductsLabel.setText(str(availbaleProducts))
        self.totalUnavailableProdutsLabel.setText(str(unavailableProducts))

    def tabChanged(self):
        self.getStatistics()
        self.displayProducts()
        self.displayMembers()

class DisplayMember(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Member Details")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(450,150,450,700)
        #self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.memberDetails()
        self.widgets()
        self.layouts()

    def memberDetails(self):
        global memberId
        query=("SELECT * FROM members WHERE member_id=?")
        member=cur.execute(query,(memberId,)).fetchone()
        #print(member)
        self.memberName=member[1]
        self.memberSSO=member[2]
        self.memberPhone=member[3]

    def widgets(self):
        ################## Widgets for top layouts ##########
        self.memberImg=QLabel()
        self.img=QPixmap('icons/members.png')
        self.memberImg.setPixmap(self.img)
        self.memberImg.setAlignment(Qt.AlignCenter)
        self.tittleText=QLabel("Display Member")
        self.tittleText.setAlignment(Qt.AlignCenter)

        ################## Widgets for Bottom layouts ##########
        self.nameEntry=QLineEdit()
        self.nameEntry.setText(self.memberName)
        self.ssoEntry=QLineEdit()
        self.ssoEntry.setText(self.memberSSO)
        self.phoneEntry=QLineEdit()
        self.phoneEntry.setText(self.memberPhone)
        self.updateBtn=QPushButton("Update")
        self.updateBtn.clicked.connect(self.updateMember)
        self.deleteBtn=QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.deleteMember)

    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QVBoxLayout()
        self.bottomLayout=QFormLayout()
        self.topFrame=QFrame()
        self.topFrame.setStyleSheet(style.memberTopFrame())
        self.bottomFrame=QFrame()
        self.bottomFrame.setStyleSheet(style.memberBottomFrame())

        ############## add widgets ##############
        self.topLayout.addWidget(self.tittleText)
        self.topLayout.addWidget(self.memberImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow(QLabel("Name*: "),self.nameEntry)
        self.bottomLayout.addRow(QLabel("SSO: "),self.ssoEntry)
        self.bottomLayout.addRow(QLabel("Phone/Email*: "),self.phoneEntry)
        self.bottomLayout.addRow(QLabel(""),self.updateBtn)
        self.bottomLayout.addRow(QLabel(""),self.deleteBtn)
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)
        self.setLayout(self.mainLayout)

    def deleteMember(self):
        global memberId
        try:
            query="DELETE FROM members WHERE member_id=?"
            cur.execute(query,(memberId,))
            con.commit()
            QMessageBox.information(self,"Info","Member has been deleted")
        except:
            QMessageBox.information(self, "Info", "Member has not been deleted")

    def updateMember(self):
        global memberId
        name=self.nameEntry.text()
        sso=self.ssoEntry.text()
        phone=self.phoneEntry.text()
        if (name and phone !=""):
            try:
                query="UPDATE members set member_name=?,member_sso=?,member_phone=? WHERE member_id=?"
                cur.execute(query,(name,sso,phone,memberId))
                con.commit()
                QMessageBox.information(self,"Info","Memeber has been updated!")
            except:
                QMessageBox.information(self, "Info", "Memeber has not been updated!")
        else:
            QMessageBox.information(self, "Info", "Fields can not be empty!")

class DisplayProduct(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Module Details")
        self.setWindowIcon(QIcon("icons/icon.ico"))
        self.setGeometry(450,150,450,700)
        #self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.productDetails()
        self.widgets()
        self.layouts()

    def productDetails(self):
        global productId
        query=("SELECT * FROM products WHERE serial_number=?")
        product=cur.execute(query,(productId,)).fetchone()#single item tuple=(1,)
        #print(product)
        self.moduleName=product[1]
        self.moduleDetail=product[2]
        self.moduleBoe=product[3]
        self.moduleOwner=product[4]
        self.moduleAvailability=product[5]
        self.moduleStoredLocation=product[6]
        self.moduleFixtureLocation=product[7]
        self.moduleImg=product[8]

    def widgets(self):
        global productId
        ###################### Top Laout Widgets ############
        self.module_Img=QLabel()
        self.img=QPixmap('img/{}'.format(self.moduleImg))
        self.module_Img.setPixmap(self.img)
        self.module_Img.setAlignment(Qt.AlignCenter)
        self.tittleText=QLabel("Update Product")
        self.tittleText.setAlignment(Qt.AlignCenter)

        ##################### Bottom Layout #################
        #self.serialNumber=QLineEdit()
        #self.serialNumber.setText(str(productId))
        self.nameEntry=QLineEdit()
        self.nameEntry.setText(self.moduleName)
        self.detailEntry=QLineEdit()
        self.detailEntry.setText(self.moduleDetail)
        self.boeEntry = QLineEdit()
        self.boeEntry.setText(str(self.moduleBoe))
        self.ownerEntry = QComboBox()


        query2 = ("SELECT member_id, member_name FROM members")
        members = cur.execute(query2).fetchall()
        for member in members:
            self.ownerEntry.addItem(member[1],member[0])

        query1="SELECT owner FROM products WHERE serial_number=?"
        self.comboowner=cur.execute(query1,(productId,)).fetchone()
        self.ownerEntry.setCurrentText(self.comboowner[0])

        self.availabilityCombo=QComboBox()
        self.availabilityCombo.addItems(["Available","Unavailable"])
        query3="SELECT module_availability FROM products WHERE serial_number=?"
        self.comboAvailability=cur.execute(query3,(productId,)).fetchone()
        self.availabilityCombo.setCurrentText(self.comboAvailability[0])

        self.storedEntry=QLineEdit()
        self.storedEntry.setText(self.moduleStoredLocation)
        self.fixtureEntry=QLineEdit()
        self.fixtureEntry.setText(self.moduleFixtureLocation)
        self.uploadBtn=QPushButton("Upload")
        self.uploadBtn.clicked.connect(self.uploadImg)
        self.deleteBtn=QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.deleteProduct)
        self.updateBtn=QPushButton("Update")
        self.updateBtn.clicked.connect(self.updateProduct)

    def layouts(self):
        self.mainLayout=QVBoxLayout()
        self.topLayout=QVBoxLayout()
        self.bottomLayout=QFormLayout()
        self.topFrame=QFrame()
        self.topFrame.setStyleSheet(style.productTopFrame())
        self.bottomFrame=QFrame()
        self.bottomFrame.setStyleSheet(style.productBottomFrame())

        ############### add widgets ####################
        self.topLayout.addWidget(self.tittleText)
        self.topLayout.addWidget(self.module_Img)
        self.topFrame.setLayout(self.topLayout)

        #self.bottomLayout.addRow(QLabel("Serial Number: "),self.serialNumber)
        self.bottomLayout.addRow(QLabel("Module Name*: "),self.nameEntry)
        self.bottomLayout.addRow(QLabel("Description: "),self.detailEntry)
        self.bottomLayout.addRow(QLabel("BOE#/PO#*: "),self.boeEntry)
        self.bottomLayout.addRow(QLabel("Owner*: "),self.ownerEntry)
        self.bottomLayout.addRow(QLabel("Availability: "),self.availabilityCombo)
        self.bottomLayout.addRow(QLabel("Stored Location: "), self.storedEntry)
        self.bottomLayout.addRow(QLabel("Fixture Location: "), self.fixtureEntry)
        self.bottomLayout.addRow(QLabel("Image: "),self.uploadBtn)
        self.bottomLayout.addRow(QLabel(""),self.deleteBtn)
        self.bottomLayout.addRow(QLabel(""),self.updateBtn)
        self.bottomFrame.setLayout(self.bottomLayout)
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def uploadImg(self):
        size=(256,256)
        self.filename,ok =QFileDialog.getOpenFileName(self,'Upload Image','','Image Files (*.jpg *.png)')
        if ok:
            #print(self.filename)
            self.moduleImg=os.path.basename(self.filename)
            img=Image.open(self.filename)

            img=img.resize(size)
            img.save("img/{0}".format(self.moduleImg))

    def updateProduct(self):
        global productId
        #serial=int(self.serialNumber.text())
        name=self.nameEntry.text()
        detail=self.detailEntry.text()
        boe=self.boeEntry.text()
        owner=self.ownerEntry.currentText()
        availability=self.availabilityCombo.currentText()
        stored=self.storedEntry.text()
        fixture=self.fixtureEntry.text()
        defaultImg=self.moduleImg

        if (name and boe and owner !=""):
            try:
                #query=("UPDATE products set module=?,description=?,boe=?,owner=?,available=?,stored_location=?,fixture_location=?,product_img WHERE serial_number=?")
                query = ("UPDATE products set module=?,description=?,boe=?,owner=?,stored_location=?,fixture_location=?,product_img=?,module_availability=? WHERE serial_number=?")
                #cur.execute(query,((name,detail,boe,owner,availability,stored,fixture,defaultImg,productId)))
                cur.execute(query, ((name,detail,boe,owner,stored,fixture,defaultImg,availability,productId)))
                con.commit()
                QMessageBox.information(self,"Info","Product has been updated!!!")

            except:
                QMessageBox.information(self,"Info","Product has not been updated!!!")

        else:
            QMessageBox.information(self, "Info", "Fields can not be empty!!!")

    def deleteProduct(self):
        global productId

        #mbox=QMessageBox.question(self,"Warning""you sure",QMessageBox.Yes)
        #if(mbox==QMessageBox.Yes):
        try:
            cur.execute("DELETE FROM products WHERE serial_number=?",(productId,))
            con.commit()
            QMessageBox.information(self,"Info","Product has been deleted!")
            self.close()
        except:
            QMessageBox.information(self, "Info", "Product has not been deleted!")


def main():
    App=QApplication(sys.argv)
    window=Main()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()
