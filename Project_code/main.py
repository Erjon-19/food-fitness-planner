from usecase_1_2 import *
from usecase_3_4 import *
from usecase_5 import *
from usecase_6 import *
from usecase_7_8 import *

def main():
    app = QtWidgets.QApplication(sys.argv)
    ins=InsertStatScreen()
    ins.show()
    config.stats=Statistics() #Δημιουργία αντικειμένου στατιστικών
    config.us=User() #Δημιουργία αντικειμένου χρήστη
    config.rus=regUser() #Δημιουργία αντικειμένου εγγεγραμμένου χρήστη
    sys.exit(app.exec_())

if __name__== '__main__':
    main()
