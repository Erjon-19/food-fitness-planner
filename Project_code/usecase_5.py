# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from UIFrames import *
import config
import re
import sqlite3
from sqlite3 import Error

class SearchScreen(QtWidgets.QMainWindow):
      def __init__(self):
          super(SearchScreen,self).__init__()  
          self.ui=SearchFrame()
          self.ui.setupUi(self)
          self.ui.pushButton.clicked.connect(self.btn_search)
          self.ui.pushButton_3.clicked.connect(self.btn_back)
          self.ui.listWidget.itemClicked.connect(self.click_on_list)
          ss.s1.fetch_DBdata()                                            # φέρε απο την Βάση Δεδομένων 
          ss.s2.fetch_DBdata()
          ss.s3.fetch_DBdata()               
          history=ss.get_previous_search()                                # έλεγχος ιστορικού
          if history[0] !=0:
            for item in history:
              self.ui.listWidget.addItem(item)          

      def btn_search(self):                                               # Μηχανή Αναζήτησης, όπου παίρνει την διεύθυνση και ελέγχει τη ορθότητά της 
          self.ui.listWidget.clear()         
          slist=[] 
          if (len(self.ui.lineEdit.text())>0):
            slist=config.us.search(self.ui.lineEdit.text())
            if slist[0]== 0:  
              QtWidgets.QMessageBox.about(self,"Mήνυμα Αποτυχίας","Μη ορθή διεύθυνση")
            elif slist[0] == -1:
              QtWidgets.QMessageBox.about(self,"Mήνυμα Αποτυχίας","Δεν βρέθηκαν καταστήματα")
            else:  
              for item in slist:
                self.ui.listWidget.addItem(item)
          slist.clear() 
      
      def click_on_list(self):                                            # Επιλογή καταστήματος από την λίστα
           temp=self.ui.listWidget.currentItem().text()
           if "X-Treme Stores" in temp:
            dlist=ss.s1.get_store_info()
           if "Ecoshop" in temp:
            dlist=ss.s2.get_store_info()
           if "Βιταμίνες και Υγιεινές Τροφές" in temp:
            dlist=ss.s3.get_store_info()
           self.ui.label_6.setText("Δ/νση:" + "\t" + dlist[0])            # Εμφάσισε τις πληροφορίες του καταστήματος
           self.ui.label_7.setText("E-mail:" + "\t" + dlist[1])
           self.ui.label_8.setText("Αριθμός τηλεφώνου:" + " " + " " + str(dlist[2]))
           self.ui.label_9.setText("Βαθμολογία:" + " " + " " + str(dlist[3]))

      def change_filters(self):                                           # Αλλαγή φίλτρων(Δεν υλοποϊήθηκε)
        pass      
     
      def btn_back(self):                                                 # Επιστροφή στο αρχικό menu και καταγραφή ιστορικού
          if re.match("[α-ωΑ-Ωά-ώ]+[\s][0-9]*|[α-ωΑ-Ωά-ώ]",self.ui.lineEdit.text())!=None or self.ui.lineEdit.text()=="":
            ss.record_search_history(self.ui.lineEdit.text())
          self.close()

class SSession:
      def __init__(self):                                                 # Αρχικοποίηση μεταβλητών
            self.storelist=[]
            self.search_history=""
            self.s1=Store("X-Treme Stores")
            self.s2=Store("Ecoshop")
            self.s3=Store("Βιταμίνες και Υγιεινές Τροφές")

      def get_list(self,addr):
         self.storelist.clear()                                            # έλεγχος διευθύνσεων και προσθήκη λίστας Καταστημάτων
         if addr in self.s1.physaddress:
            self.storelist.append(self.s1.get_store_name())   
         if addr in self.s2.physaddress:
            self.storelist.append(self.s2.get_store_name())
         if addr in self.s3.physaddress:
            self.storelist.append(self.s3.get_store_name())
         if addr not in self.s1.physaddress and addr not in self.s2.physaddress and addr not in self.s3.physaddress:
            return [-1]
         return self.storelist                                  
      
      def get_previous_search(self):                                      # Ανάκτηση προηγούμενης αναζήτησης
         file=open("history.txt","r")
         self.search_history=file.read()
         if self.search_history != "":
           plist=self.get_list(self.search_history)
           if plist[0]!=-1:
             return plist
           else:
             return [0]  
         else:
           return [0]  

      def record_search_history(self,history):                            # Καταγραφή Αναζήτησης 
         file=open("history.txt","w")
         file.write(history)    

  
class Store:
      def __init__(self,name):                                            # Αρχικοποίηση μεταβλητών
         self.name=name
         self.physaddress=""
         self.email=""
         self.contactnum=0
         self.rating=0

      def fetch_DBdata(self):                                             # Δημιουργία σύνδεσης με την Βάση 
            conn = None
            try:
              conn = sqlite3.connect('pdb.db')              
            except Error as e:
              print(e)
                                                                          # Ανάκτηση πληροφοριών Καταστημάτων
            cur=conn.execute("select * from Store where name=?", (self.name,))
            for row in cur:
               self.physaddress=row[1]
               self.email=row[2]
               self.contactnum=row[3]
               self.rating=row[4]
            conn.close()                                                  # Τερματισμός σύνδεσης με την Βάση  

      def get_store_info(self):                                           # Επιστροφή πληροφοριών
            retlist=[self.physaddress,self.email,self.contactnum,self.rating]
            return retlist

      def get_store_name(self):                                            # Επιστροφή του ονόματος καταστήματος
            return self.name       

ss=SSession()