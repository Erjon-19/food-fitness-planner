from UIFrames import DietFrame
from PyQt5 import QtCore, QtGui, QtWidgets
import config
from config import *
import os
import datetime
import sqlite3

db_file = os.getcwd() +'/pdb.db' # προορισμός αρχείου βάσης δεδομένων

class Food():
	def __init__(self,name):
		self.name = name # το ονομα του φαγητού
		self.calories = 0 # τις θερμίδες που έχει το φαγητό
		self.proteins = 0 # την προτεϊνη που περιέχει το φαγητό
		self.carbs = 0 # τους υδατάνθρακες που περιέχει το φαγητό
		self.sugars = 0 # τα ζάκχαρα που που περιέχει το φαγητό
		self.unsaturated_fat = 0 # τα μη κορεσμένα λιπαρά που περιέχει το φαγητό
		self.saturated_fat = 0 # τα κορεσμένα λιπαρά που περιέχει το φαγητό

	def fetch_DBdata(self): # παίρνει τις πληροφιρίες των τροφών με βάση το όνομα απο την βάση δεδομένων
		conn = None
		c = None
		try:
			conn = sqlite3.connect(db_file)
			c = conn.cursor()
		except Error:
			print("Error on attempt to connect with the DB:")
		q = 'SELECT calories,proteins,carbs,sugars,unsaturated_fat,saturated_fat FROM food_cat WHERE name='+"'"+str(self.name)+"'"
		c.execute(q)
		row = c.fetchall()
		if(str(self.name)==''):
			pass
		else:
			self.calories = row[0][0]
			self.proteins = row[0][1]
			self.carbs = row[0][2]
			self.sugars = row[0][3]
			self.unsaturated_fat = row[0][4]
			self.saturated_fat = row[0][5]


	def get_calories(self): # επιστρέφει τις θερμίδες που έχει το φαγητό
		return self.calories

	def get_nutrients(self): # επιστρέφει τα θρεπτικά συστατικά που έχει το φαγητό
		nutrients = self.proteins, self.carbs, self.sugars, self.unsaturated_fat, self.saturated_fat
		return nutrients


class Dietprog():
	def __init__(self):
		self.p_calories = 0 # τις συνολικές θερμίδες που έχει το διατροφικό πρόγραμμα
		self.p_proteins = 0 # την συνολική προτεϊνη που έχει το διατροφικό πρόγραμμα
		self.p_carbs = 0 # τους συνολικούς υδατάνθρακες που έχει το διατροφικό πρόγραμμα
		self.p_sugars = 0 # τα συνολικά ζάκχαρα που έχει το διατροφικό πρόγραμμα
		self.p_unsaturated_fat = 0 # τα συνολικά μη κορεσμένα λιπαρά που έχει το διατροφικό πρόγραμμα
		self.p_saturated_fat = 0 # τα συνολικά κορεσμένα λιπαρά που έχει το διατροφικό πρόγραμμα
		self.food_list = [[], [], [], []] # λιστα οι οποία περιέχει τις λίστες πρωινό, μεσιμεριανό, βραδινό και μία κατηγορία έξτρα η 
		# οποία περιέχει οτιδηποτε άλλο μπορεί να φάει ο χρήστης κατά την διάρκεια της ημέρας 

	def dietprog_recomd(self,goal_kg,current_kg): # προτείνει διατροφικά προγράμματα ανάλογα με τον στόχο και τα κιλά που έχει εισάγει ο χρήστης
		prog_1 = [['τοστ','γαλα','μηλο'],['πατατες','μπιφτεκι','μπροκολο'],['ρυζι','κοτοπουλο','σαλατα']]
		prog_2 = [['τοστ','γαλα','ροδακινο'],['πατατες','κοτοπουλο','μπροκολο'],['ρυζι','κοτοπουλο'],['πορτοκαλι','σαλατα']]
		prog_3 = [['γαλα','μηλο'],['πατατες','μπιφτεκι','μπροκολο'],['ρυζι','κοτοπουλο','σαλατα']]
		prog_4 = [['τοστ','γαλα','μηλο'],['πατατες','κοτοπουλο','κουνουπιδι'],['ρυζι','μοσχαρι','σαλατα'],['κρασι']]
		prog_5 = [['τοστ','γαλα'],['μπιφτεκι','σαλατα'],['ρυζι','κοτοπουλο','σαλατα'],['μηλο','ροδακινο']]
		prog_6 = [['τοστ','μηλο'],['μπιφτεκι','μπροκολο','φασολια'],['ρυζι','κοτοπουλο','σαλατα'],['σαλατα','ροδακινο']]
		programs_dict = {}
		if(goal_kg > current_kg):
			programs_dict['προγραμμα πλουσιο σε πρωτεϊνη και υδατανθρακα'] = prog_1
			programs_dict['προγραμμα πλουσιο σε πρωτεϊνη με λιγα λιπαρα'] = prog_5
			programs_dict['προγραμμα πλουσιο σε πρωτεϊνη, υδατανθρακα με λιγοστα σακχαρα'] = prog_3
		elif(goal_kg < current_kg):
			programs_dict['προγραμμα πλουσιο σε πρωτεϊνη με λιγα λιπαρα'] = prog_5
			programs_dict['προγραμμα πλουσιο σε πρωτεϊνη με λιγα λιπαρα και υδατανθρακα'] = prog_2
			programs_dict['προγραμμα πλουσιο σε πρωτεϊνη και φυτικές ινες με λιγα λιπαρα'] = prog_6
		else:
			programs_dict['προγραμμα πλουσιο σε πρωτεϊνη και υδατανθρακα'] = prog_1
			programs_dict['προγραμμα πλουσιο σε πρωτεϊνη, υδατανθρακα με κανονικη ποσοτητα σακχαρων'] = prog_4
			programs_dict['προγραμμα πλουσιο σε πρωτεϊνη και φυτικές ινες με λιγα λιπαρα'] = prog_6
		return programs_dict

	def get_prog_calories(self): # επιστρέφει τις συνολικές θερμίδες του προγράμματος διατροφής του χρήστη και ενημερώνει και τα στατιστικά του
		config.stats.update_food_stats(self.p_proteins, self.p_carbs, self.p_sugars, self.p_unsaturated_fat, self.p_saturated_fat, self.p_calories)
		return self.p_calories

	def save_to(self,lists): # αποθηκεύει το πρόγραμμα του χρήστη στην λίστα food_list με αντικείμενα της κλάσης Food
		i=0
		for l in lists:
			row = 0
			while(l.item(row)!=None):
				name = l.item(row)
				self.food_list[i].append(Food(str(name.text()))) # αντικείμενα τύπου Food
				row +=1
			i+=1
		for l in self.food_list:
			for food in l:
				food.fetch_DBdata() # φορτώνω στα φαγητά που έχει η food_list τις τιμές τους απο την βάση δεδομένων

	def compute_calories(self): # Υπολογίζει τις θερμίδες του προγράμματος διατροφής του χρήστη
		for food_sub_list in self.food_list:
			for food in food_sub_list:
				self.p_calories += food.get_calories() # παίρνω τις θερμίδες που έχει το κάθε φαγητό
		if(self.p_calories>0):
			return 0 # Επιτυχία
		else:
			return 1 # Αποτυχία

	def compute_nutrients(self): # Υπολογίζει τα θρεπτικά συστατικά του προγράμματος διατροφής του χρήστη
		for food_sub_list in self.food_list:
			for food in food_sub_list:
				tmp = food.get_nutrients() # παίρνω τα θρεπτικά συστατικά που έχει το κάθε φαγητό
				self.p_proteins += tmp[0]
				self.p_carbs += tmp[1]
				self.p_sugars += tmp[2]
				self.p_unsaturated_fat += tmp[3]
				self.p_saturated_fat += tmp[4]
		if(self.p_proteins < 0 or self.p_carbs < 0 or self.p_sugars < 0 or self.p_unsaturated_fat < 0 or self.p_saturated_fat < 0 ):
			return 1 # Αποτυχία
		return 0 # Επιτυχία


	def check_calories_limit(self,user_max_calories): # Ελένχω αν ο χρήστης έχει υπερβεί το όριο θερμίδων
		if(self.p_calories <= user_max_calories):
			return 0 # Επιτυχία αν δεν το έχει ξεπεράσει
		else:
			return 1 # Αποτυχία αν το έχει ξεπεράσει


class DietScreen(QtWidgets.QMainWindow):
	def __init__(self):
		super(DietScreen,self).__init__()
		self.ui = DietFrame()
		self.ui.setupUi(self)
		self.recmd_progs = {} # dictionary με τα προτεινόμενα προγράμματα
		self.gui_lists = [ self.ui.breakfast_list, self.ui.lunch_list, self.ui.dinner_list, self.ui.extras_list ] # Λίστα που περιέχει τις λίστες του πρωινού, μεσιμεριανού, βραδινού και τα έξτρα
		self.ui.exit.clicked.connect(self.btn_exit)
		self.currentDT = datetime.datetime.now() # Επιστρέφει την ημερομινία και την ώρα
		self.date = self.currentDT.strftime("%d -%m-%Y") # Κρατάω μόνο την ημερομηνία
		self.ui.date.setText(str(self.date)) # Εισάγω την ημερομινία στο label
		self.ui.g_calories_num.setText(str(config.us.suggestedCal)) # Παίρνω την προτεινόμενη κατανάλωση θερμίδων απο τον χρήστη και το γράφω στο label
		current_kg, goal_kg = config.us.get_goal_current_kg() # Παίρνει τον στόχο σε κιλά και το τωρινό βάρος του χρήστη
		self.recmd_progs = config.us.dprog.dietprog_recomd(goal_kg,current_kg) # Παίρνει τα προτεινόμενα προγράμματα με βάση τον στόχο σε κιλά και το τωρινό βάρος του χρήστη
		for key in self.recmd_progs:
			item = QtWidgets.QListWidgetItem(key)
			item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
			self.ui.reccomd_progs.addItem(item)
		self.ui.calories_btn.setEnabled(False)
		self.ui.nutritiens_btn.setEnabled(False)
		self.ui.save.setEnabled(False)
		# Λειτουργίες των κουμπίων
		self.ui.brekf_add.clicked.connect(lambda: self.btn_insert_to_fields(self.ui.breakfast_list))
		self.ui.lunch_add.clicked.connect(lambda: self.btn_insert_to_fields(self.ui.lunch_list))
		self.ui.diner_add.clicked.connect(lambda: self.btn_insert_to_fields(self.ui.dinner_list))
		self.ui.extras_add.clicked.connect(lambda: self.btn_insert_to_fields(self.ui.extras_list))
		self.ui.save.clicked.connect(lambda: self.btn_save(self.gui_lists))
		self.ui.nutritiens_btn.clicked.connect(self.btn_compute_nutrients)
		self.ui.calories_btn.clicked.connect(self.btn_compute_calories)
		self.ui.insert.clicked.connect(lambda: self.btn_insert_prog(self.gui_lists,self.ui.reccomd_progs,self.recmd_progs))
		self.ui.statistics.clicked.connect(self.btn_show_statistics)

	def btn_insert_prog(self,lists,list_btn,dictt): # Για το κουμπί εισαγωγή
		try:
			prog_ = list_btn.selectedItems()
			name = prog_[0].text()
			tmp = dictt[str(name)]
			self.display_on_fields(lists,tmp)
		except IndexError:
			return 

	def display_on_fields(self,lists,flist): # Εμφανίζει το προτινόμενο πρόγραμμα που έχει εισάγει ο χρήστης στα πεδία Πρωινό, Μεσιμεριανό, Βραδινό και Έξτρα
		list_ind = 0
		for l in flist:
			for it in l:
				item = QtWidgets.QListWidgetItem(it)
				lists[list_ind].addItem(item)
			list_ind += 1
		self.ui.save.setEnabled(True)

	def btn_insert_to_fields(self,list_btn): # Επιτρέπει στον χρήστη να εισάγει τροφη-τροφές στα πεδία Πρωινό, Μεσιμεριανό, Βραδινό και Έξτρα
		item = QtWidgets.QListWidgetItem()
		item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
		n = list_btn.currentRow()
		list_btn.addItem(item)
		self.ui.save.setEnabled(True)

	def btn_save(self,lists): # Καλείται οταν ο χρήστης πατάει αποθήκευση και αποθηκεύει το πρόγραμμα που έχει εισάγει
		config.us.dprog.save_to(lists)
		self.ui.nutritiens_btn.setEnabled(True)

	def btn_exit(self): # κλείνει το παράθυρο
		self.close()

	def btn_compute_nutrients(self): # Μέθοδος που εκτελείται όταν ο χρήστης πατάει το κουμί "Υπολογισμος Θρεπτικών Συστατικών"
		result_bool = config.us.dprog.compute_nutrients() # Υπολογίζει τα θρεπτικά συστατικά του προγράμματος διατροφής
		if(result_bool==1):
			self.msg = QtWidgets.QMessageBox()
			self.msg.setWindowTitle("Μήνυμα")
			self.msg.setText("Τα θρεπτικά συστατικά του προγράμματος δεν υπολογίστικαν.")
			self.msg.show()
		self.ui.calories_btn.setEnabled(True)

	def btn_compute_calories(self): # Μέθοδος που εκτελείται όταν ο χρήστης πατάει το κουμί "Υπολογισμος Θερμίδων"
		result_bool = config.us.dprog.compute_calories()# Υπολογίζει τις θερμίδες του προγράμματος διατροφής
		self.msg = QtWidgets.QMessageBox()
		self.msg.setWindowTitle("Μήνυμα")
		self.msg.buttonClicked.connect(self.btn_ok)
		if(result_bool==0):
			self.msg.setText("Οι θερμίδες υπολογίστικαν.")
			self.msg.show()
		else:
			self.msg.setText("Οι θερμίδες δεν υπολογίστικαν.")	

	def show_calories(self,calories): # Δείχνει στο gui τις θερμίδες που έχει καταναλώσει ο χρήστης
		self.ui.f_calories_num.setText(str(calories))
				
	def btn_ok(self): # Μέθοδος που εκτελείται αφού έχουν υπολογιστεί επιτυχώς οι θερμίδες που έχει καταναλώσει ο χρήστης
		  user_calories = config.us.fetch_max_calories() # Επιστρέφει το προτεινόμενο ποσό θερμίδων που πρέπει να καταναλώσει ο χρήστης
		  cmp_cal_bool = config.us.dprog.check_calories_limit(user_calories) # ελένχει αν οι θερμίδες που έχει καταναλώσει ο χρήστης υπερβαίνουν το προτεινόμενο ποσό θερμίδων
		  if(cmp_cal_bool==0):
			   calories = config.us.dprog.get_prog_calories() # Παίρνει τις θερμίδες του προγράματος διατροφής
			   self.show_calories(calories)
		  else:
			  self.wmsg = QtWidgets.QMessageBox()
			  self.wmsg.setWindowTitle("Προειδοποιητικό Μήνυμα")
			  self.wmsg.setText("Το προτεινόμενο όριο θερμίδων έχει ξεπεραστεί.")
			  self.wmsg.show()
			  calories = config.us.dprog.get_prog_calories()
			  self.show_calories(calories)

	def btn_show_statistics(self): # Εμφανίζει το παράθυρο των στατιστικών
		self.stwin = StatisticsScreen()
		self.stwin.show()


