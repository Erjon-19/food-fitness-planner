from UIFrames import *
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
us = None
rus = None
stats = None
ins = None

class StatisticsScreen(QtWidgets.QMainWindow):
      def __init__(self):
          super(StatisticsScreen,self).__init__()  
          self.ui=StatisticsFrame()
          self.ui.setupUi(self)
          self.ui.pushButton.clicked.connect(self.btn_exit)
          self.displist=stats.get_gym_Stats() #λίστα με τα στατιστικά γυμναστικής
          self.dispfoodstats_list = stats.get_food_stats() #λίστα με τα στατιστικά διατροφής           
          #------------Γυμναστική-----------
          self.ui.lineEdit_4.setText(str(self.displist[0])) #αριθμός επαναλήψεων κοιλιακών
          self.ui.lineEdit_3.setText(str(self.displist[1])) #αριθμός σετ κοιλιακών
          self.ui.lineEdit_5.setText(str(self.displist[2])) #αριθμός επανάλήψεων ραχαίων
          self.ui.lineEdit_6.setText(str(self.displist[3])) #αριθμός σετ ραχαίων
          self.ui.lineEdit.setText(str(self.displist[4]))   #αριθμός επαναλήψεων βάρη
          self.ui.lineEdit_2.setText(str(self.displist[5])) #αριθμός σετ βάρη
          self.ui.lineEdit_17.setText(str(self.displist[6])) #μεγιστα κιλά βάρη
          self.ui.lineEdit_7.setText(str(self.displist[7])) #αριθμός επαναλήψεων εργαλείων γυμναστικής 
          self.ui.lineEdit_8.setText(str(self.displist[8])) #αριθμός σετ εργαλείων γυμναστικής
          self.ui.lineEdit_16.setText(str(self.displist[9])) #ώρα διάδρομος
          self.ui.lineEdit_9.setText(str(self.displist[10])) #ταχύτητα διάδρομος
          #----------- Διατροφη ----------
          self.ui.lineEdit_10.setText(str(self.dispfoodstats_list[1])) # αριθμός υδατανθράκων που έχει γενικά ο χρήστης
          self.ui.lineEdit_11.setText(str(self.dispfoodstats_list[2])) # αριθμός ζακχάρων που έχει γενικά ο χρήστης
          self.ui.lineEdit_12.setText(str(self.dispfoodstats_list[0])) # αριθμός πρωτεϊνων που έχει γενικά ο χρήστης
          self.ui.lineEdit_13.setText(str(self.dispfoodstats_list[4])) # αριθμός κορεσμένων λιπαρών που έχει γενικά ο χρήστης
          self.ui.lineEdit_14.setText(str(self.dispfoodstats_list[3])) # αριθμός μη κορεσμένων λιπαρών που έχει γενικά ο χρήστης
          self.ui.lineEdit_15.setText(str(self.dispfoodstats_list[5])) # αριθμός θερμίδων που έχει γενικά ο χρήστης
          self.plotWidget = None
          self.show_graph()          

      def btn_exit(self):
           self.close()

      def show_graph(self): # Μεθοδος η οποία φτιάχνει το διάγραμμα πίτας στο παράθυρο των στατιστικών
        labels = ['protein','carbs','sugars','unsaturated_fat','saturated_fat']
        data = self.dispfoodstats_list[0:5]
        fig = Figure()
        ax = fig.add_subplot(111)
        ax.pie(data,labels=labels)
        self.plotWidget = Canvas(fig)
        lay = QtWidgets.QVBoxLayout(self.ui.graph_widget)
        lay.setContentsMargins(0,0,0,0)
        lay.addWidget(self.plotWidget)        