from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from UIFrames import *
import datetime
import re
import datetime
import sqlite3
from sqlite3 import Error
import os
import config
db_file = os.getcwd() +'/pdb.db'

class Product:
    def __init__(self):
        self.topname = []
        self.id = 0
        self.topvalue = []
        self.name = []
        self.value = []

    def fetch_DBdata(self): # Φόρτωση δεδομένων από την βάση
        conn = None
        c = None
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
        except Error as e:
            print(e)

        q = 'SELECT top_list, value_top FROM product_top'
        c.execute(q)
        row = c.fetchall()

        for i in row:
            self.topname.append(i[0])
            self.topvalue.append(i[1])

        q1 = 'SELECT product_name, value FROM products'
        c.execute(q1)
        row1 = c.fetchall()

        for j in row1:
            self.name.append(j[0])
            self.value.append(j[1])

    def get_top_name(self): # Επιστρέφει την λίστα με τα τοπ προϊόντα
        return self.topname

    def get_top_value(self): # Επιστρέφει την λίστα με τις τιμές των τοπ προϊόντων
        return self.topvalue

    def get_name(self): #Επιστρέφει την λίστα με τα προϊόντα
        return self.name

    def get_value(self): # Επιστρέφει την λίστα με τις τιμές των προϊόντων
        return self.value

class EInterface:
    def __init__(self):
        self.Buy_Product_list=[]
        self.Sell_Product_list = []
        self.val_list = []
        self.Totalval = 0.00
        self.prd = Product()
        self.prd.fetch_DBdata()

    def Addtolist(self, arg_list): # Προσθήκη στο Καλάθι
        self.Buy_Product_list = [str(arg_list.item(i).text()) for i in range(arg_list.count())]

    def get_product_list(self): # Επιστρέφει τη λίστα με προϊόντα το (Καλάθι)
        return self.Buy_Product_list

    def calc_Total(self): # Υπολογισμός συνολικού ποσού
        self.val_list.clear()
        self.Totalval=0.00
        cnt=[]
        for i in range(0,len(self.Buy_Product_list)):
            cnt.append(self.Buy_Product_list[i])
            it=cnt[i].split(" ")
            self.val_list.append(float(it[1]))


        for j in self.val_list:
            self.Totalval = self.Totalval + j

        self.Totalval = round(self.Totalval,2)
        return self.Totalval

    def Transaction(self): # Συναλλαγή
        bank_account = config.rus.get_wallet()
        if self.Totalval <= bank_account:
            return 1
        else:
            return -1

    def Search_Product(self,prod): # Αναζήτηση Προϊόντος
        pname=self.prd.get_name()
        pvalue=self.prd.get_value()
        if prod in pname:
            i = pname.index(prod)
            return pvalue[i]
        else:
            return -1

    def Store(self,dta,num_dta): # Έλεγχος τιμών δεδομένων και αριθμητικών δεδομένων
        self.Sell_Product_list = dta
        self.val_list = num_dta
        if len(self.Sell_Product_list)!=len(self.val_list) or self.Sell_Product_list[0]=='' or self.val_list[0]=='':
        	return -1
        return 1

    def Payuser(self): # Πληρωμή του χρήστη
    	payout=0
    	for i in range(0,len(self.val_list)):
    		payout=payout+(float(self.val_list[i])*80/100)
    	config.rus.recievePayment(payout)

    def update_DB(self): # Ενημέρωση Βάσης Δεδομένων και εισαγωγή στοιχείων
        conn = None
        c = None
        try:
            conn = sqlite3.connect(db_file)
            c = conn.cursor()
        except Error as e:
            print(e)

        for i in range(0,len(self.Sell_Product_list)):
            c.execute("INSERT INTO products(product_name, value) VALUES (?, ?)",(self.Sell_Product_list[i], float(self.val_list[i])))

        conn.commit()
        conn.close()


class EshopScreen(QtWidgets.QMainWindow): # Επιλογή Αγορά ή Μεταπώληση
    def __init__(self):
        super(EshopScreen,self).__init__()
        self.ui=EshopFrame()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.btn_exit) # Έξοδος
        self.ui.pushButton_2.clicked.connect(self.btn_buy) # Αγορά
        self.ui.pushButton_3.clicked.connect(self.btn_sell) # Μεταπώληση

    def btn_buy(self): #Αγορά
        self.b = BuyScreen()
        self.b.show()

    def btn_sell(self): # Μεταπώληση
        self.s=SellScreen()
        self.s.show()

    def btn_exit(self): # Έξοδος
        self.close()

class BuyScreen(QtWidgets.QMainWindow): # Αγορά Προϊόντων Οθόνη
    def __init__(self):
        super(BuyScreen,self).__init__()
        self.ui=Buy_ProductFrame()
        self.ui.setupUi(self)
        self.name=ein.prd.get_top_name()
        self.val=ein.prd.get_top_value()

        for i in range(0, len(self.name)):
            item = QtWidgets.QListWidgetItem(self.name[i] + " " + str(self.val[i]))
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
            self.ui.listWidget_2.addItem(item)

        self.ui.pushButton.clicked.connect(self.btn_search) # κουμπί αναζήτηση
        self.ui.pushButton_6.clicked.connect(self.btn_back) # κουμπί πίσω
        self.ui.pushButton_2.setEnabled(False) # απενεργοποιημένο κουμπί Συνέχεια
        self.ui.pushButton_4.clicked.connect(lambda: self.btn_Add(self.ui.listWidget_2)) # κουμπί Προσθήκη
        self.ui.pushButton_5.clicked.connect(lambda: self.btn_Delete(self.ui.listWidget)) # κουμπί Αφαίρεση
        self.ui.pushButton_2.clicked.connect(lambda: self.btn_Continue(self.ui.listWidget)) # κουμπί Συνέχεια

    def btn_Add(self, list):
        prods = list.selectedItems()
        if not prods:
            return
        itm = prods[0]
        self.ui.listWidget.addItem(itm.text())
        self.ui.pushButton_2.setEnabled(True)

    def btn_Delete(self, list):
        listItems= list.selectedItems()
        if not listItems:
            return
        list.takeItem(list.currentRow())
        if self.ui.listWidget.count() != 0:
            self.ui.pushButton_2.setEnabled(True)
        else:
            self.ui.pushButton_2.setEnabled(False)

    def btn_Continue(self, arg_list):
        ein.Addtolist(arg_list)
        self.close()
        self.p = PayScreen()
        self.p.show()

    def change_filters(): # Φίλτρα δεν το έχουμε υλοποιήση στον κωδικα
        pass

    def btn_back(self): # κουμπί Πίσω
        self.close()

    def btn_search(self):
        retval = ein.Search_Product(self.ui.lineEdit.text())
        if retval!=-1:
            self.ui.listWidget.addItem(self.ui.lineEdit.text() + " " + str(retval))
            self.ui.pushButton_2.setEnabled(True)
        else:
            QtWidgets.QMessageBox.about(self, "Μήνυμα", "Προϊόν δεν βρέθηκε")

class PayScreen(QtWidgets.QMainWindow): # Οθ΄΄ονη Πληρωμή
    def __init__(self):
        super(PayScreen,self).__init__()
        self.ui=Pay_outFrame()
        self.ui.setupUi(self)
        prd_list=ein.get_product_list() # Λήψη προϊόντων
        calc=ein.calc_Total() # Λήψη συνολικού ποσού

        for i in prd_list:
            item = QtWidgets.QListWidgetItem(str(i))
            self.ui.listWidget.addItem(item)

        self.ui.listWidget_2.addItem(str(calc))
        self.ui.pushButton_2.clicked.connect(lambda: self.btn_Verify()) #κουμπί Επιβεβαίωση

    def btn_Verify(self): #κουμπί Επιβεβαίωση
        return self.CheckInfoUser()

    def CheckInfoUser(self): # Έλεγχος των στοιχείων που έδωσε ο χρήστης

        Credit_Card = self.ui.lineEdit.text()
        CCV = self.ui.lineEdit_2.text()
        MB_number = self.ui.lineEdit_3.text()

        if len(Credit_Card) == 16: # Πρέπει να έχει 16 ψηφία
            if Credit_Card.isdigit() == True:
                flag=1
            else:
                flag=0
                QtWidgets.QMessageBox.about(self, "Μήνυμα", "Λανθασμένα στοιχεία")
        else:
            flag=0
            QtWidgets.QMessageBox.about(self, "Μήνυμα", "Λανθασμένα στοιχεία")

        if len(CCV) == 3: # Πρέπει να έχει 3 ψηφία
            if CCV.isdigit() == True:
                flag2=1
            else:
                flag2=0
                QtWidgets.QMessageBox.about(self, "Μήνυμα", "Λανθασμένα στοιχεία")
        else:
            flag2=0
            QtWidgets.QMessageBox.about(self, "Μήνυμα", "Λανθασμένα στοιχεία")

        if len(MB_number) == 10: # Πρέπει να έχει 10 ψηφία
            if MB_number[:2] == "69" and MB_number[2:10].isdigit() == True:
                flag3=1
            else:
                flag3=0
                QtWidgets.QMessageBox.about(self, "Μήνυμα", "Λανθασμένα στοιχεία")
        else:
            flag3=0
            QtWidgets.QMessageBox.about(self, "Μήνυμα", "Λανθασμένα στοιχεία")

        if flag==1 and flag2==1 and flag3==1:
            retval=ein.Transaction() # Κλήση Transaction αν retval1=1 τότε επιτυχία, διαφορετικά αποτυχία
            if retval==1:

               self.msg = QtWidgets.QMessageBox()
               self.msg.setWindowTitle("Μήνυμα")
               self.msg.setText("Η συναλλαγή σας oλοκληρώθηκε.")
               self.msg.show()
               self.msg.buttonClicked.connect(self.btn_ok)
            else:

               self.msg = QtWidgets.QMessageBox()
               self.msg.setWindowTitle("Μήνυμα")
               self.msg.setText("Η συναλλαγή σας δεν oλοκληρώθηκε.")
               self.msg.show()
               self.msg.buttonClicked.connect(self.btn_ok)
        else:
            pass

    def btn_ok(self):
        self.close()

class SellScreen(QtWidgets.QMainWindow): # Οθόνη Μεταπώληση προϊόντων
    def __init__(self):
        super(SellScreen,self).__init__()
        self.ui=Sell_productFrame()
        self.ui.setupUi(self)
        self.sell_list = []

        self.ui.pushButton_4.clicked.connect(self.btn_back)
        self.textEdit= QtWidgets.QTextEdit()
        self.ui.pushButton_3.clicked.connect(lambda: self.btn_store())
        self.ui.pushButton_2.clicked.connect(lambda: self.btn_Continue())
        self.ui.pushButton_2.setEnabled(False)


    def btn_store(self): # κουμπί Αποθήκευση
        data = self.ui.textEdit.toPlainText()
        d = data.strip()
        data = re.split('[\n\t^\s+$,$]{1,100}', d) # Regular expression για τα ονόματα των προϊόντων

        num_data = self.ui.textEdit_2.toPlainText()
        n_d = num_data.strip()
        num_data = re.split('[\n\t^\s+$,$]{1,100}', n_d) #Regular expression για τις τιμές των προϊόντων
        retval=ein.Store(data, num_data) # κλήση συνάρτησης Store από την κλάση EInterface για την αποθήκευση στοιχείων
        if retval==1:
        	self.ui.pushButton_2.setEnabled(True)
        	QtWidgets.QMessageBox.about(self, "Μήνυμα", "Eπιτυχία αποθήκευσης")
        else:
            QtWidgets.QMessageBox.about(self, "Μήνυμα", "Αποτυχία αποθήκευσης")


    def btn_Continue(self):
        self.close()
        self.g = GainScreen()
        self.g.show()

    def btn_back(self):
        self.close()


class GainScreen(QtWidgets.QMainWindow): # Οθόνη Αποπληρωμή
    def __init__(self):
        super(GainScreen,self).__init__()
        self.ui=PaybackFrame()
        self.ui.setupUi(self)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_2.clicked.connect(lambda: self.btn_Verify())
        self.ui.pushButton_2.setEnabled(True)

    def btn_Verify(self):
        return self.CheckInfoUser()

    def CheckInfoUser(self):
        IBAN = self.ui.lineEdit.text() # for check GR9608100010000001234568900
        MB_number = self.ui.lineEdit_3.text() # 6912345678

        if len(IBAN) == 27: # Πρέπει να είναι 27  το IBAN υποστηρίζει μόνο την έκδοση GR96 όχι άλλες
            if IBAN[:4] == "GR96" and IBAN[4:27].isdigit() == True:
                flag=1
            else:
                flag=0
                QtWidgets.QMessageBox.about(self, "Μήνυμα", "Λανθασμένα στοιχεία")
        else:
            flag=0
            QtWidgets.QMessageBox.about(self, "Μήνυμα", "Λανθασμένα στοιχεία")
        if len(MB_number) == 10: # Πρέπει να είναι 10
            if MB_number[:2] == "69" and MB_number[2:10].isdigit() == True:
                flag2=1
            else:
                flag2=0
                QtWidgets.QMessageBox.about(self, "Μήνυμα", "Λανθασμένα στοιχεία")
        else:
            flag2=0
            QtWidgets.QMessageBox.about(self, "Μήνυμα", "Λανθασμένα στοιχεία")

        if flag==1 and flag2==1:
            retval = ein.Payuser()

            self.msg = QtWidgets.QMessageBox()
            self.msg.setWindowTitle("Μήνυμα")
            self.msg.setText("Η συναλλαγή σας oλοκληρώθηκε.")
            self.msg.show()
            self.msg.buttonClicked.connect(self.btn_ok)
        else:
            pass

    def btn_ok(self):
        ein.update_DB()
        self.close()

ein = EInterface() # Δημιουργία αντικειμένου
