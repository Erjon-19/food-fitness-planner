# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
import matplotlib
import sys
from UIFrames import *
from usecase_3_4 import *
from usecase_5 import *
from usecase_6 import * 
from usecase_7_8 import *
from config import *
import re
import sqlite3
from sqlite3 import Error

matplotlib.use('QT5Agg')

class InsertStatScreen(QtWidgets.QMainWindow):
      def __init__(self):
          super(InsertStatScreen,self).__init__()  
          self.ui=InsertFrame()
          self.ui.setupUi(self)
          self.medhistory=""
          validator=QtGui.QDoubleValidator()
          self.ui.lineEdit.setValidator(validator)
          self.ui.lineEdit_2.setValidator(validator)
          self.ui.lineEdit_3.setValidator(validator)
          self.ui.pushButton.clicked.connect(self.btn_continue)
          self.ui.pushButton_2.clicked.connect(self.btn_noinsert)

      def check_data(self):        #έλεγχος ορθότητα στοιχείων
          if (len(self.ui.lineEdit.text()) <= 0 ):                 #έλεγχος ύψους
                self.ui.label_7.setText("Δώσε Ύψος")
                flag4 = 0
          else:      
                if ( float(self.ui.lineEdit.text()) > 3.0  or float(self.ui.lineEdit.text()) < 1.0) : #(1,3)
                    self.ui.label_7.setText("Λάθος")
                    flag4 = 0
                else:
                    self.ui.label_7.setText("")
                    flag4 = 1

          if (len(self.ui.lineEdit_2.text()) <= 0 ):               #έλεγχος βάρος
                self.ui.label_8.setText("Δώσε Βάρος")
                flag5 = 0
          else:      
                if ( float(self.ui.lineEdit_2.text()) > 300.0  or float(self.ui.lineEdit_2.text()) < 10.0) : #(10,300)
                   self.ui.label_8.setText("Λάθος")
                   flag5 = 0
                else:
                   self.ui.label_8.setText("")
                   flag5 = 1      

          if (len(self.ui.lineEdit_3.text()) <= 0 ):              #έλεγχος στόχου βάρους
                self.ui.label_9.setText("Δώσε Στόχο")
                flag6 = 0
          else:      
                if ( float(self.ui.lineEdit_3.text()) > 300.0  or float(self.ui.lineEdit_3.text()) < 10.0) : #(10,300)
                   self.ui.label_9.setText("Λάθος")
                   flag6 = 0
                else:
                    self.ui.label_9.setText("")
                    flag6 = 1

          if self.ui.radioButton.isChecked() == True:             #έλεγχος εμπειρίας γυμναστικής
                self.exp=self.ui.radioButton.text()
                flag = 1
          if self.ui.radioButton_2.isChecked() == True:
                self.exp=self.ui.radioButton_2.text()
                flag = 1         
          if self.ui.radioButton_3.isChecked() == True:                             
                self.exp=self.ui.radioButton_3.text()
                flag = 1

          if self.ui.radioButton_4.isChecked() == True:          #έλεγχος γένους
                self.gender=self.ui.radioButton_4.text()
                flag2 = 1
          if self.ui.radioButton_5.isChecked() == True:
                self.gender=self.ui.radioButton_5.text()
                flag2 = 1

          if self.ui.checkBox_4.isChecked() == True:             #έλεγχος ιατρικού ιστoρικού
                self.medhistory=self.medhistory + self.ui.checkBox_4.text()    
          if self.ui.checkBox_5.isChecked() == True:
                self.medhistory=self.medhistory + self.ui.checkBox_5.text()
          if self.ui.checkBox_6.isChecked() == True:
                self.medhistory=self.medhistory + self.ui.checkBox_6.text()

          if self.ui.radioButton_4.isChecked() == False and self.ui.radioButton_5.isChecked() == False: #ενημέρωση χρήστη αν δεν επέλεξε γένος
                self.ui.label_11.setText("Επέλεξε 1")
                flag2 = 0

          if self.ui.radioButton.isChecked() == False and self.ui.radioButton_2.isChecked() == False and self.ui.radioButton_3.isChecked() == False: #ενημέρωση χρήστη αν δεν επέλεξε εμπειρία γυμναστικής
                self.ui.label_10.setText("Επέλεξε 1")
                flag = 0      

          if (flag == 1 and flag2 == 1 and flag4 == 1 and flag5 == 1 and flag6 == 1):  # αν είναι σωστά τα στοιχεία            
                return 1
          else:
                return -1  

      def btn_continue(self):       #click Συνέχεια
          retval=self.check_data()
          if retval == 1:       #σωστά στοιχεία
           config.us.setUsrdata(self.ui.lineEdit.text(),self.ui.lineEdit_2.text(),self.ui.lineEdit_3.text(),self.exp,self.gender,self.medhistory)     
           self.close()
           self.rg=RegUserScreen()
           self.rg.show()

      def btn_noinsert(self): #click Δεν επιθυμώ να εισάγω στοιχεία
         self.close()
         self.rg=RegUserScreen()
         self.rg.show()
   
         
class RegUserScreen(QtWidgets.QMainWindow):
      def __init__(self):
          super(RegUserScreen,self).__init__()  
          self.ui=RegisterFrame()
          self.ui.setupUi(self)
          validator=QtGui.QIntValidator()
          self.ui.lineEdit_5.setValidator(validator)
          self.ui.lineEdit_6.setValidator(validator)
          self.ui.lineEdit_7.setValidator(validator)
          self.ui.pushButton.clicked.connect(self.btn_noreg)
          self.ui.pushButton_2.clicked.connect(self.btn_register)

      def check_data(self):      #έλεγχος ορθότητας στοιχείων 
            if (len(self.ui.lineEdit.text()) > 0):  #έλεγχος ον/μου
                  flag=1
            else:
                  flag=0

            if (len(self.ui.lineEdit_2.text()) > 0): #έλεγχος username
                  flag1=1
            else:
                  flag1=0

            if (len(self.ui.lineEdit_3.text()) >= 6): #έλεγχος password (τουλ 6 χαρακτήρες)
                  flag2=1
                  self.ui.label_9.setText("")
            else:
                  self.ui.label_9.setText("Λάθος")
                  flag2=0

            if (len(self.ui.lineEdit_4.text()) > 7): #έλεγχος ορθότητας email
              if (re.match('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$',self.ui.lineEdit_4.text())!= None):       
                  flag3=1
                  self.ui.label_10.setText("")
              else:
                  self.ui.label_10.setText("Λάθος")
                  flag3=0

            if (len(self.ui.lineEdit_5.text()) >0): #έλεγχος νούμερου μπλούζας   
              if  int(self.ui.lineEdit_5.text()) < 48  and  int(self.ui.lineEdit_5.text()) > 17 : #(17,48)
                  flag4=1
                  self.ui.label_11.setText("")
              else:
                  flag4=0
                  self.ui.label_11.setText("Λάθος")
            else:
              self.ui.label_11.setText("Δώσε νούμερο")
              flag4=0
                  
            if (len(self.ui.lineEdit_6.text()) >0): #έλεγχος νούμερου παντελονιού
              if  int(self.ui.lineEdit_6.text()) < 48  and  int(self.ui.lineEdit_6.text()) > 17 : #(17,48)
                  flag5=1
                  self.ui.label_12.setText("")
              else:
                  flag5=0
                  self.ui.label_12.setText("Λάθος")
            else:
                  self.ui.label_12.setText("Δώσε νούμερο")
                  flag5=0

            if (len(self.ui.lineEdit_7.text()) >0): #έλεγχος νούμερου παπουτσιού                                    
              if  int(self.ui.lineEdit_7.text()) < 48  and  int(self.ui.lineEdit_7.text()) > 17 : #(17,48)
                  flag6=1
                  self.ui.label_13.setText("")
              else:
                  flag6=0
                  self.ui.label_13.setText("Λάθος")
            else:
                  self.ui.label_13.setText("Δώσε νούμερο")
                  flag6=0

            if (flag==1 and flag1==1 and flag2==1 and flag3==1 and flag4==1 and flag5==1 and flag6==1): # αν είναι σωστά τα στοιχεία
                  return 1
            else:
                  return -1
                  
      def btn_noreg(self): #click Δεν επιθυμώ να εγγραφώ
          self.close()   
          self.ap=MainMenuScreen()
          self.ap.show()
          
      def btn_register(self): #click Ολοκλήρωση εγγραφής
         retval=self.check_data()
         if retval==1:  #σωστά στοιχεία
            retval1=config.rus.updateDB(self.ui.lineEdit.text(),self.ui.lineEdit_2.text(),self.ui.lineEdit_3.text(),self.ui.lineEdit_4.text(),self.ui.lineEdit_5.text(),self.ui.lineEdit_6.text(),self.ui.lineEdit_7.text()) #ενημέρωση βάσης δεδομένων
            if retval1 == 1:               
              self.close()   
              self.ap=MainMenuScreen()
              self.ap.show()
            else:
               self.ui.label_14.setText("Βάλε άλλο όνομα χρήστη")     

               
class MainMenuScreen(QtWidgets.QMainWindow):
      def __init__(self):
          super(MainMenuScreen,self).__init__()  
          self.ui=AppmenuFrame()
          self.ui.setupUi(self)
          self.ui.pushButton.clicked.connect(self.btn_changeUsrdata)
          self.ui.pushButton_2.clicked.connect(self.btn_gym)
          self.ui.pushButton_3.clicked.connect(self.btn_additional_features)
          self.ui.pushButton_4.clicked.connect(self.btn_diet)
          self.ui.pushButton_5.clicked.connect(self.btn_store)
          self.ui.pushButton_6.clicked.connect(self.btn_search_engine)
          self.dlist=config.us.getUsrdata()
          self.ui.lineEdit.setText(str(self.dlist[0]))
          self.ui.lineEdit_2.setText(str(self.dlist[1]))
          self.ui.lineEdit_3.setText(str(self.dlist[2]))
          self.ui.lineEdit_4.setText(str(self.dlist[6]))
          self.ui.lineEdit_5.setText(str(self.dlist[7]))
          self.ui.lineEdit_6.setText(str(self.dlist[8]))
       
      def btn_changeUsrdata(self): #click Αλλαγή στοιχείων
         self.close()   
         self.ins=InsertStatScreen()
         self.ins.show()

      def btn_gym(self): #click Γυμναστική   
         self.gm=GymMenuScreen()
         self.gm.show()

      def btn_additional_features(self): #click Πρόσθετες λειτουργίες  
         self.ad=AdditionalScreen()
         self.ad.show()   

      def btn_diet(self): #click Διατροφή
         self.dt = DietScreen()
         self.dt.show()

      def btn_store(self): #click Ηλεκτρονικό κατάστημα  
         self.es=LoginScreen()
         self.es.show()

      def btn_search_engine(self): #click Μηχανή αναζήτησης 
         self.se=SearchScreen()
         self.se.show()
         
class LoginScreen(QtWidgets.QDialog):
      def __init__(self):
          super(LoginScreen,self).__init__()  
          self.ui=LoginFrame()
          self.ui.setupUi(self)
          self.ui.pushButton.clicked.connect(self.btn_connect)

      def btn_connect(self): #click Σύνδεση
          retval=config.rus.validateCredentials(self.ui.lineEdit.text(),self.ui.lineEdit_2.text()) #επικύρωση στοιχείων
          if retval == -1 : #αποτυχία
                QtWidgets.QMessageBox.about(self, "Μήνυμα", "Ελέγξτε τα στοιχεία που δώσατε")
                self.close()
          if retval == 1 : #επιτυχία
                self.msg = QtWidgets.QMessageBox()
                self.msg.setWindowTitle("Μήνυμα")
                self.msg.setText("Συνδεθήκατε Επιτυχώς")
                self.msg.show()
                self.msg.buttonClicked.connect(self.btn_ok)

      def btn_ok(self):
          self.close()
          self.es=EshopScreen()
          self.es.show()          
         
class GymMenuScreen(QtWidgets.QMainWindow):
      def __init__(self):
          super(GymMenuScreen,self).__init__()  
          self.ui=GymnasticsFrame()
          self.ui.setupUi(self)
          self.ui.pushButton.clicked.connect(self.btn_insertGProg)
          self.ui.pushButton_2.clicked.connect(self.btn_calculate_calories)
          self.ui.pushButton_3.clicked.connect(self.btn_exit)
          self.ui.pushButton_4.clicked.connect(self.btn_statistics)
          self.ui.pushButton_5.clicked.connect(self.btn_save)
          self.ui.listWidget.itemClicked.connect(lambda: self.btn_save)
          self.glist=config.us.suggestgprogs() #λίστα προτεινόμενων προγραμμάτων
          for item in self.glist:
              self.ui.listWidget.addItem(item)

      def btn_save(self): #αποθήκευση προτεινόμενου προγράμματος 
            self.val=1
            g=[]
            if self.ui.listWidget.currentItem() != None:
              temp=self.ui.listWidget.currentItem().text()
              temp=re.split('" "|,',temp)
              for i in temp:
               g.append(i.split(" ")) 

              if "Βάρη" in g[0][0]:
                arg1=g[0][1]
                arg2=g[0][3]
              else:
                  arg1=0
                  arg2=0
              if "Κοιλιακοί" in g[1][0]:
                arg3=g[1][1]
              else:
                arg3=0  
              if "Ραχαίοι" in g[2][0]:
                arg4=g[2][1]
              else:
                arg4=0  
              if "Διάδρομος" in g[3][0]:
                arg5=g[3][1]
                arg6=g[3][4]
              else:
                arg5=0
                arg6=0

              config.us.gprog.setgprog("10",arg3,"10",arg4,"10",arg1,arg2,"0","0",arg5,arg6) #εισαγωγή προγράμματος γυμναστικής
              self.ui.label_2.setText("Επιλέξατε")

      def btn_insertGProg(self):  #click εισαγωγή προγράμματος διατροφής
         self.gmp=GprogmenuScreen()
         self.gmp.show()
         self.ui.label_2.setText("Η αποθήκευση ολοκληρώθηκε")         

      def btn_calculate_calories(self):            
               calc=config.us.gprog.calc_p_burnedCal()
               if calc!=0:
                 self.ui.lineEdit.setText(str(calc))
               else:
                 self.ui.label_2.setText("Αποτυχία υπολογισμού")  

      def btn_exit(self):
         self.close()

      def btn_statistics(self): #click στατιστικά χρήστη
         self.sc=StatisticsScreen()
         self.sc.show()
         
class GprogmenuScreen(QtWidgets.QMainWindow):
      def __init__(self):
          super(GprogmenuScreen,self).__init__()  
          self.ui=GymProgFrame()
          self.ui.setupUi(self)
          self.ui.pushButton.clicked.connect(self.btn_save)
          validator=QtGui.QIntValidator()
          self.ui.lineEdit.setValidator(validator)
          self.ui.lineEdit_2.setValidator(validator)
          self.ui.lineEdit_3.setValidator(validator)
          self.ui.lineEdit_4.setValidator(validator)
          self.ui.lineEdit_5.setValidator(validator)
          self.ui.lineEdit_6.setValidator(validator)
          self.ui.lineEdit_7.setValidator(validator)
          self.ui.lineEdit_8.setValidator(validator)
          self.ui.lineEdit_9.setValidator(validator)
          self.ui.lineEdit_10.setValidator(validator)
          self.ui.lineEdit_11.setValidator(validator)


      def btn_save(self): #αποθήκευση προγράμματος γυμναστικής που εισάχθηκε από τον χρήστη
            if( len(self.ui.lineEdit.text())> 0 and len(self.ui.lineEdit_2.text())> 0 and len(self.ui.lineEdit_3.text())> 0 and len(self.ui.lineEdit_4.text())> 0 and len(self.ui.lineEdit_5.text())> 0 and len(self.ui.lineEdit_6.text())> 0 and len(self.ui.lineEdit_7.text())> 0 and len(self.ui.lineEdit_8.text())> 0 and len(self.ui.lineEdit_9.text())> 0 and len(self.ui.lineEdit_10.text())> 0 and len(self.ui.lineEdit_11.text())> 0):
              config.us.gprog.setgprog(self.ui.lineEdit_4.text(),self.ui.lineEdit_3.text(),self.ui.lineEdit_6.text(),self.ui.lineEdit_5.text(),self.ui.lineEdit_2.text(),self.ui.lineEdit.text(),self.ui.lineEdit_9.text(),self.ui.lineEdit_7.text(),self.ui.lineEdit_8.text(),self.ui.lineEdit_11.text(),self.ui.lineEdit_10.text())
              self.close()
            else:
              self.ui.label_17.setText("Συμπλήρωσε όλα τα πεδία!")     

class User:
      def __init__(self):
       self.height=0
       self.weight=0
       self.gender=""
       self.exp=""
       self.medhistory=""
       self.targetweight=0
       self.bmi=0
       self.fatlvl=""
       self.suggestedCal=0
       self.articlepref=""
       self.comment=""
       self.rating=0
       self.searchquery=""       
       self.gprog=Gymprog()
       self.dprog = Dietprog()

      def get_goal_current_kg(self): # Επιστρέφει τα κιλά και τον στοχο σε κιλα του χρήστη
        return self.weight, self.targetweight

      def fetch_max_calories(self): # Επιστρέφει το προτεινόμενο ποσό θερμίδων που πρέπει να καταναλώσει ο χρήστης
        return self.suggestedCal
      
      def setUsrdata(self,h,w,tw,e,g,mh): #αποθήκευση στοιχείων
          self.height=h
          self.weight=w
          self.targetweight=tw
          self.gender=g
          self.exp=e
          self.medhistory=mh
          self.calcbmi()
          self.calcfatlvl()
          
      def calcbmi(self): #υπολογισμός δείκτη μάζας σώματος
          self.height=float(self.height)
          self.weight=float(self.weight)
          self.targetweight=float(self.targetweight)
          self.bmi= self.weight/(pow(self.height,2))
          self.bmi=float("{:.3f}".format(self.bmi))

      def calcfatlvl(self): #υπολογισμός λιποσαρκείας και προτεινόμενων θερμίδων 
            if self.bmi >= 25.0:
                  self.fatlvl = "Υπερβαρος"
            elif self.bmi < 18.5:
                  self.fatlvl = "Υπόβαρος"
            else:
                  self.fatlvl = "Κανονικό βάρος"

            if "Άνδρας" in self.gender :
                  if (self.weight > self.targetweight):
                    self.suggestedCal=2000
                  elif (self.weight < self.targetweight):
                    self.suggestedCal=3000
                  else:
                    self.suggestedCal=2500

            else:
                  if (self.weight > self.targetweight):
                    self.suggestedCal=1500
                  elif (self.weight < self.targetweight):
                    self.suggestedCal=2500
                  else:
                    self.suggestedCal=2000         
         

      def getUsrdata(self): #άντληση στοιχείων χρήστη
            retlist=[self.height,self.weight,self.targetweight,self.gender,self.exp,self.medhistory,self.bmi,self.fatlvl,self.suggestedCal]
            return retlist

      def suggestgprogs(self): #προτεινόμενα προγράμματα
            suggestlist=[]
            
            if "άσθμα" in self.medhistory and "Άνδρας" in self.gender and ( "Αρχάριος" in self.exp or "Συνιθησμένος" in self.exp):
                  suggestlist.append("Βάρη 20 σετ 10 κιλά, Κοιλιακοί 50 σετ,Ραχαίοι 50 σετ,Διάδρομος 5 λεπτά ταχύτητα 2")

            if "άσθμα" in self.medhistory and "Γυναίκα" in self.gender and ( "Αρχάριος" in self.exp or "Συνιθησμένος" in self.exp) :
                  suggestlist.append("Βάρη 10 σετ 5 κιλά, Κοιλιακοί 25 σετ,Ραχαίοι 25 σετ,Διάδρομος 5 λεπτά ταχύτητα 2")
                  
            if "καρδιακά" in self.medhistory and "Άνδρας" in self.gender and ( "Αρχάριος" in self.exp or "Συνιθησμένος" in self.exp) :
                  suggestlist.append("Βάρη 10 σετ 6 κιλά, Κοιλιακοί 10 σετ,Ραχαίοι 10 σετ,Διάδρομος 15 λεπτά ταχύτητα 2")

            if "καρδιακά" in self.medhistory and "Γυναίκα" in self.gender and ( "Αρχάριος" in self.exp or "Συνιθησμένος" in self.exp) :
                  suggestlist.append("Βάρη 6 σετ 3 κιλά, Κοιλιακοί 5 σετ,Ραχαίοι 5 σετ,Διάδρομος 8 λεπτά ταχύτητα 2")

            if "υπέρβαρος" in self.medhistory and "Άνδρας" in self.gender and ( "Αρχάριος" in self.exp or "Συνιθησμένος" in self.exp) : 
                  suggestlist.append("Βάρη 5 σετ 10 κιλά,Κοιλιακοί 40 σετ,Ραχαίοι 40 σετ,Διάδρομος 40 λεπτά ταχύτητα 6")

            if "υπέρβαρος" in self.medhistory and "Γυναίκα" in self.gender and ( "Αρχάριος" in self.exp or "Συνιθησμένος" in self.exp) : 
                  suggestlist.append("Βάρη 5 σετ 10 κιλά,Κοιλιακοί 20 σετ,Ραχαίοι 20 σετ,Διάδρομος 40 λεπτά ταχύτητα 6")

            if "Έμπειρος" in self.exp:
                  suggestlist.append("Βάρη 50 σετ 10 κιλά,Κοιλιακοί 70 σετ,Ραχαίοι 70 σετ,Διάδρομος 60 λεπτά ταχύτητα 5")
                  
            if not suggestlist:
                  emptylist=[]
                  return emptylist      
                   
            return suggestlist

      def check_n_addCnR(self,com,rat,c): #έλεγχος και προσθήκη σχόλιου
            if(len(com)<=150 and len(com)>0):
               self.comment=com
               self.rating=rat  
               if c==1:
                 a1.saveCnR(self.comment,self.rating)
               elif c==2:
                 a2.saveCnR(self.comment,self.rating)
               else:                  
                 a3.saveCnR(self.comment,self.rating)
               return 1     
            else:
               return -1

      def savePref(self,pref): #αποθήκευση προτημήσεων σε άρθρα
            self.articlepref=pref
            file=open("userpref.txt","w")
            file.write(self.articlepref)

      def search(self,text): #Έλεγχος ορθότητας διεύθυνσης/πόλης και πραγματοποίηση αναζήτησης
            searchlist=[]
            self.searchquery=text
            if re.match("[α-ωΑ-Ωά-ώΆ-Ώ]+[\s][0-9]*|[α-ωΑ-Ωά-ώΆ-Ώ]",self.searchquery)!=None:
               searchlist=ss.get_list(self.searchquery)
               if searchlist[0] == -1:
                  return [-1]
            else:
                  return [0]     
            return searchlist            
            


class regUser(User):
      def __init__(self):
            self.fullname=""
            self.username=""
            self.password=""
            self.email=""
            self.torsonum=0
            self.pantsnum=0
            self.shoesnum=0
            self.wallet=0

      def updateDB(self,f,u,p,e,t,pn,s): #ενημέρωση βάσης δεδομένων
            self.fullname=str(f)
            self.username=str(u)
            self.password=str(p)
            self.email=str(e)
            self.torsonum=int(t)
            self.pantsnum=int(pn)
            self.shoesnum=int(s)
            
            conn = None
            try:
              conn = sqlite3.connect('pdb.db')
              
            except Error as e:
              print(e)
            
            cur=conn.execute("select username from regUser")
            for row in cur:                                  
                  if self.username==row[0]:     #έλεγχος για κοινά username
                        return -1
            conn.execute("insert into regUser (fullname,username,password,email,torsonum,pantsnum,shoenum) values (?,?,?,?,?,?,?)",(self.fullname,self.username,self.password,self.email,self.torsonum,self.pantsnum,self.shoesnum,))
            conn.commit()
            conn.close()
            return 1

      def validateCredentials(self,user,passwd): #επικύρωση στοιχείων
            conn = None
            try:
              conn = sqlite3.connect('pdb.db')
              
            except Error as e:
              print(e)
 
            cur=conn.execute("select username,password from regUser")
            for row in cur:
                  if user==str(row[0]) and passwd==str(row[1]):
                    return 1
            conn.close()            
            return -1

      def get_wallet(self): #τραπεζικός λογαριασμός χρήστη
           self.wallet=30
           return self.wallet

      def recievePayment(self,pay): #αποπληρωμή χρήστη
           self.wallet=self.wallet+pay           

class Gymprog:
      def __init__(self):
            self.situpNum=0
            self.situpSNum=0
            self.backextNum=0
            self.backextSNum=0
            self.weightsNum=0
            self.weightsSNum=0
            self.weightsKg=0
            self.toolexerciseNum=0
            self.toolexerciseSNum=0
            self.runtime=0
            self.runspeed=0
            self.p_burnedCal=0

      def setgprog(self,sn,ssn,bn,bsn,wn,wsn,wkg,ten,tesn,rt,rp): #αποθήκευση προγράμματος γυμναστικής και άντληση στοιχείων από την ΒΔ για κάθε άσκηση
            self.situpNum=int(sn)
            self.situpSNum=int(ssn)
            self.backextNum=int(bn)
            self.backextSNum=int(bsn)
            self.weightsNum=int(wn)
            self.weightsSNum=int(wsn)
            self.weightsKg=int(wkg)
            self.toolexerciseNum=int(ten)
            self.toolexerciseSNum=int(tesn)
            self.runtime=int(rt)
            self.runspeed=int(rp)
            if int(sn)>0:
                  self.a=GExercise("situp")
                  self.a.fetch_DBdata()
            if int(bn)>0:
                  self.b=GExercise("backext")
                  self.b.fetch_DBdata()
            if int(wn)>0:
                  self.c=GExercise("weights")
                  self.c.fetch_DBdata()
            if int(ten)>0:
                  self.d=GExercise("toolexercise")
                  self.d.fetch_DBdata()
            if int(rt)>0:
                  self.e=GExercise("run")
                  self.e.fetch_DBdata()
                  
                  
      def calc_p_burnedCal(self): # υπολογισμός καμένων θερμίδων
            if int(self.situpNum)>0:
                  cal1=self.a.getburnedCal()
            else:
                  cal1=0
            if int(self.backextNum)>0:
                  cal2=self.b.getburnedCal()
            else:
                  cal2=0
            if int(self.weightsNum)>0:
                  cal3=self.c.getburnedCal()
            else:
                  cal3=0
            if int(self.toolexerciseNum)>0:
                  cal4=self.d.getburnedCal()
            else:
                  cal4=0
            if int(self.runtime)>0:
                  cal5=self.e.getburnedCal()
            else:
                  cal5=0

            self.p_burnedCal=(cal1*self.situpNum*self.situpSNum) + (cal2*self.backextNum*self.backextSNum) + (cal3*self.weightsNum*self.weightsSNum) + (cal4*self.toolexerciseNum*self.toolexerciseSNum) + (cal5*self.runtime*self.runspeed)
            if self.p_burnedCal!=0:
               config.stats.update_gym_Stats(self.situpNum,self.situpSNum,self.backextNum,self.backextSNum,self.weightsNum,self.weightsSNum,self.weightsKg,self.toolexerciseNum,self.toolexerciseSNum,self.runtime,self.p_burnedCal) # ενημέρωση στατιστικών
               return self.p_burnedCal
            else:
               return 0   

class GExercise:
      def __init__(self,name):
            self.name=name
            self.burnedCal=0

      def fetch_DBdata(self): # άντληση στοιχείων από την ΒΔ
            conn = None
            try:
              conn = sqlite3.connect('pdb.db')
              
            except Error as e:
              print(e)

            cur=conn.execute("select burnedcalories from Exercise where type=?", (self.name,))
            for row in cur:
                  self.burnedCal=row[0]

            conn.close()

      def getburnedCal(self): #άντληση καμένων θερμίδων της άσκησης
            return self.burnedCal         

class Statistics:
      def __init__(self):
            # ----- Gymprog ------        
            self.totalsitupNum=0 #συνολικός αριθμός επαναλήψεων κοιλιακών
            self.totalsitupSNum=0 #συνολικός αριθμός σετ κοιλιακών
            self.totalbackextNum=0 #συνολικός αριθμός επαναλήψεων ραχαίων
            self.totalbackextSNum=0 #συνολικός αριθμός σετ ραχαίων
            self.totalweightsNum=0 #συνολικός αριθμός επαναλήψεων βάρη
            self.totalweightsSNum=0 #συνολικός αριθμός σετ βάρη
            self.maxweight=0 #μέγιστα κιλά
            self.totaltoolexerciseNum=0 #συνολικός αριθμός επαναλήψεων εργαλείων γυμναστικής
            self.totaltoolexerciseSNum=0 #συνολικός αριθμός σετ εργαλείων γυμναστικής
            self.totalruntime=0 #συνολική ώρα διάδομος
            self.totalburnedCal=0 #συνολικός αριθμός καμένων θερμίδων
            # ----- Dietprog -------
            self.totalProteins = 0 # συνολική προτεϊνη
            self.totalCarbs = 0 # συνολικούς υδατάνθρακες
            self.totalSugars = 0 # συνολικά ζάκχαρα
            self.totalUns_Fat = 0 # συνολικά μη κορεσμένα λιπαρά
            self.totalSat_Fat = 0 # συνολικά κορεσμένα λιπαρά
            self.totalconsumedCal = 0 # συνολικές θερμίδες           

      def update_gym_Stats(self,sn,ssn,bn,bsn,wn,wsn,wkg,ten,tesn,rt,bc): #ενημέρωση της ΒΔ με τα στατιστικά γυμναστικής
            conn = None
            try:
              conn = sqlite3.connect('pdb.db')
              
            except Error as e:
              print(e)

            cur=conn.execute("select * from Statistics")
            for row in cur:
                  self.totalsitupNum=sn + row[0]
                  self.totalsitupSNum=ssn + row[1]
                  self.totalbackextNum=bn +row[2]
                  self.totalbackextSNum=bsn + row[3]
                  self.totalweightsNum=wn + row[4]
                  self.totalweightsSNum=wsn + row[5]
                  if wkg > row[6]:
                      self.maxweight=wkg
                  else:
                      self.maxweight=row[6]  
                  self.totaltoolexerciseNum=ten + row[7]
                  self.totaltoolexerciseSNum=tesn + row[8]
                  self.totalruntime=rt + row[9]
                  self.totalburnedCal=bc + row[10]

            conn.execute("update Statistics Set sn=?,ssn=?,bn=?,bsn=?,wn=?,wsn=?,wkgmax=?,ten=?,tesn=?,rt=?,bc=?",(self.totalsitupNum,self.totalsitupSNum,self.totalbackextNum,self.totalbackextSNum,self.totalweightsNum,self.totalweightsSNum,self.maxweight,self.totaltoolexerciseNum,self.totaltoolexerciseSNum,self.totalruntime,self.totalburnedCal,))
            conn.commit()
            conn.close()

      def get_gym_Stats(self): # άντληση στατιστικών γυμναστικής από την ΒΔ
            conn = None
            try:
              conn = sqlite3.connect('pdb.db')
              
            except Error as e:
              print(e)

            cur=conn.execute("select * from Statistics")
            for row in cur:
                  self.totalsitupNum=row[0]
                  self.totalsitupSNum=row[1]
                  self.totalbackextNum=row[2]
                  self.totalbackextSNum=row[3]
                  self.totalweightsNum=row[4]
                  self.totalweightsSNum=row[5]
                  self.maxweight=row[6] 
                  self.totaltoolexerciseNum=row[7]
                  self.totaltoolexerciseSNum=row[8]
                  self.totalruntime=row[9]
                  self.totalburnedCal=row[10]            

            retlist=[self.totalsitupNum,self.totalsitupSNum,self.totalbackextNum,self.totalbackextSNum,self.totalweightsNum,self.totalweightsSNum,self.maxweight,self.totaltoolexerciseNum,self.totaltoolexerciseSNum,self.totalruntime,self.totalburnedCal]
            conn.close()
            return retlist

      def update_food_stats(self,proteins,carbs,sugars,unsaturated_fat,saturated_fat,calories): # Ενημερώνει τα στατιστικά διατροφής του χρήστη στν ΒΔ
            conn = None
            c = None
            try:
             conn = sqlite3.connect('pdb.db')
             c = conn.cursor()
            except Error:
             print("Error on attempt to connect with the DB:")
            q = 'SELECT carbs,sugars,proteins,sat_fat,unsat_fat,cc FROM Statistics'
            c.execute(q) 
            for row in c:                        
              self.totalProteins = row[2] + proteins
              self.totalCarbs = row[0] + carbs
              self.totalSugars = row[1] + sugars
              self.totalUns_Fat = row[4] + unsaturated_fat
              self.totalSat_Fat = row[3] + saturated_fat
              self.totalconsumedCal = row[5] + calories

            conn.execute("UPDATE Statistics SET carbs=?,sugars=?,proteins=?,sat_fat=?,unsat_fat=?,cc=?",(self.totalCarbs, self.totalSugars, self.totalProteins, self.totalSat_Fat, self.totalUns_Fat, self.totalconsumedCal,))            
            conn.commit()
            conn.close()             

      def get_food_stats(self): # Επιστρέφει τα στατιστικά διατροφής του χρήστη για να χρησιμοποιηθούν στην οθόνη των στατιστικών από την ΒΔ
       conn = None
       c = None
       try:
        conn = sqlite3.connect('pdb.db')
        c = conn.cursor()
       except Error:
        print("Error on attempt to connect with the DB:")
       q = 'SELECT carbs,sugars,proteins,sat_fat,unsat_fat,cc FROM Statistics'
       c.execute(q)
       for row in c:
         self.totalProteins=row[0]
         self.totalCarbs=row[1]
         self.totalSugars=row[2]
         self.totalUns_Fat=row[3]
         self.totalSat_Fat=row[4]
         self.totalconsumedCal=row[5]
       conn.close()  

       p_food_stat_res = [self.totalProteins, self.totalCarbs, self.totalSugars, self.totalUns_Fat, self.totalSat_Fat, self.totalconsumedCal]
       return p_food_stat_res