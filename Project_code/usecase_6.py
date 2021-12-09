# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from UIFrames import AdditionalFrame,ArticleFrame
import config
import sqlite3
from sqlite3 import Error

class AdditionalScreen(QtWidgets.QMainWindow):
      def __init__(self):
          super(AdditionalScreen,self).__init__()  
          self.ui=AdditionalFrame()
          self.ui.setupUi(self)
          self.ui.pushButton.clicked.connect(self.btn_display)
          self.ui.pushButton_2.clicked.connect(self.btn_exit)
          self.ui.listWidget.itemClicked.connect(lambda: self.btn_display)
          a1.fetch_DBdata()                                                                # Φέρε απο την Βάση Δεδομένων 
          a2.fetch_DBdata()
          a3.fetch_DBdata()
          self.tlist=[a1.get_title(),a2.get_title(),a3.get_title()]                        # Δημιουργία Λίστας τίτλων άρθρων  
          self.rlist=[a1.get_rating(),a2.get_rating(),a3.get_rating()]                     # Δημιουργία Λίστας βαθμολογίας                                       
          self.ui.listWidget.addItem("Τίτλος:" + "\t" + self.tlist[0] + "\t" + "Βαθμολογία:" + "\t"  + str(self.rlist[0])  + "/5")        # Εμφάνισε
          self.ui.listWidget.addItem("Τίτλος:" + "\t"  + self.tlist[1] + "\t" + "Βαθμολογία:" + "\t"  + str(self.rlist[1]) +"/5")
          self.ui.listWidget.addItem("Τίτλος:" + "\t"  + self.tlist[2] + "\t" + "Βαθμολογία:" + "\t"  + str(self.rlist[2]) +"/5")
                     
      def btn_display(self):                                                               # Προβολή επιλεγμένου άρθρου
         if self.ui.listWidget.currentItem() != None:   
           temp=self.ui.listWidget.currentItem().text()
           if "Άρθρο1" in temp:
            a1.auth.fetch_DBdata()
            c=1
           elif "Άρθρο2" in temp:
            a2.auth.fetch_DBdata()
            c=2
           else:
            a3.auth.fetch_DBdata()
            c=3
            
           self.close()
           self.ar = ArticleScreen(c)                                                      # κάλεσε την οθόνη άρθρου, με όρισμα το επιλεγμενο άρθρο
           self.ar.show()
         
      def btn_exit(self):                                                                  # επιλογή έξοδος και Κλείσιμο παραθύρου
            self.close()

class ArticleScreen(QtWidgets.QMainWindow):
      def __init__(self,c):
          super(ArticleScreen,self).__init__()                                             # Ανάκτηση ορισμάτων απο την κυρια κλάση 
          self.ui=ArticleFrame()
          self.ui.setupUi(self)
          self.ui.pushButton.clicked.connect(self.btn_submit)
          self.ui.pushButton_2.clicked.connect(self.btn_back)
          self.c=c
          if self.c==1:
            list1=a1.getArticleinfo()
            list2=a1.auth.getAuthorinfo()
          elif self.c==2:
            list1=a2.getArticleinfo()
            list2=a2.auth.getAuthorinfo()
          else:
            list1=a3.getArticleinfo()
            list2=a3.auth.getAuthorinfo()
          self.ui.textEdit.setText(list1[0])
          self.ui.textEdit_2.setText(list1[1])
          self.ui.lineEdit.setText(list2[0])
          self.ui.lineEdit_2.setText(list2[1]) 
          self.ui.textEdit_4.setText(list2[2])
          self.ui.textEdit.selectionChanged.connect(self.allow_user_comment)
          
      def allow_user_comment(self):                                                             # Εισαγωγή σχόλιου
          self.ui.textEdit_3.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse|QtCore.Qt.TextEditable)

      def btn_submit(self):                                                                     # Έλεγχος σχόλιου και υποβολή
            if self.ui.radioButton.isChecked()==True:
                  rating=1
            elif self.ui.radioButton_2.isChecked()==True:
                  rating=2
            elif self.ui.radioButton_3.isChecked()==True:
                  rating=3
            elif self.ui.radioButton_4.isChecked()==True:
                  rating=4
            elif self.ui.radioButton_5.isChecked()==True:
                  rating=5
            else:
                  rating=0
            retval=config.us.check_n_addCnR(self.ui.textEdit_3.toPlainText(),rating,self.c)
            if retval==1:
              if self.c==1:
                self.cat=a1.get_category()
              elif self.c==2:
                self.cat=a2.get_category()
              else:
                self.cat=a3.get_category()         	
              
              config.us.savePref(self.cat)
              self.ad=AdditionalScreen()
              self.ad.show()              
              self.close()
            else:
              QtWidgets.QMessageBox.about(self, "Μήνυμα", "Το σχόλιο έχει δεν έχει τον επιτρεπόμενο αριθμό χαρακτήρων")    

      def btn_back(self):                                                                       # καταγραφή και ενημέρωση 
            if self.c==1:
               self.cat=a1.get_category()
            elif self.c==2:
               self.cat=a2.get_category()
            else:
               self.cat=a3.get_category()
               
            config.us.savePref(self.cat)
            self.ad=AdditionalScreen()
            self.ad.show()
            self.close()

class Article:
      def __init__(self,title):                                                                 # Αρχικοποίηση μεταβλητών
            self.title=title
            self.rating=0
            self.articletext=""
            self.comments=""
            self.category=""
            self.auth=AAuthor(self.title)

      def fetch_DBdata(self):                                                                   # Δημιουργία σύνδεσης με την Βάση 
            conn = None
            try:
              conn = sqlite3.connect('pdb.db')
              
            except Error as e:
              print(e)

            cur=conn.execute("select * from Article where title=?", (self.title,))              # Ανάκτηση πληροφοριών των Άρθρων 
            for row in cur:
                self.rating=row[1]
                self.articletext=row[2]
                self.comments=row[3]
                self.category=row[4]

            conn.close()                                                                        # Τερματισμός σύνδεσης με την Βάση  

      def get_title(self):                                                                      # Επιστροφή δεδομένων 
             return self.title

      def get_rating(self):
             return self.rating

      def getArticleinfo(self):
             articleinfo=[self.articletext,self.comments]
             return articleinfo

      def get_category(self):
            return self.category       

      def saveCnR(self,ct,rt):
            conn = None
            try:
              conn = sqlite3.connect('pdb.db')
              
            except Error as e:
              print(e)
                                                                                                # Ενημέρωση βάσης δεδομένων ύστερα απο την επιτυχή υποβολή του σχολίου
            conn.execute("update Article Set rating=?,comments=? where title=?", (rt,self.comments + "\n" + ct,self.title,))
            conn.commit()
            conn.close()
              
             

class AAuthor:
      def __init__(self,art):                                                                   # Αρχικοποίηση μεταβλητών
            self.article=art
            self.fullname=""
            self.bio=""
            self.email=""

      def fetch_DBdata(self):
            conn = None
            try:
              conn = sqlite3.connect('pdb.db')
              
            except Error as e:
              print(e)

            cur=conn.execute("select * from AAuthor where Article=?", (self.article,))          # Ανάκτηση των στοιχείων του συγγραφέα από την βαση
            for row in cur:
                self.fullname=row[0]
                self.bio=row[1]
                self.email=row[2]

            conn.close()

      def getAuthorinfo(self):                                                                  # Επιστροφή των δεδομένων 
           authorinfo=[self.fullname,self.email,self.bio]
           return authorinfo

a1=Article("Άρθρο1")
a2=Article("Άρθρο2")
a3=Article("Άρθρο3")      
