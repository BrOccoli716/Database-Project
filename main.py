import sys
from DataBase_Course.py.utils import *  # Here input your own route(relative route is OK)


#  In the Controller, we enable connections between different windows.
#  This is realized by launching another target window when the current window's corresponding 'pyqtsignal' is emitted.
#  We also need to judge whether to close the current window.
class Controller:
    def __init__(self):
        #  Here we store the information of the current user, which will be used later.
        self.account = None
        self.name = None
        self.sex = None
        self.age = 0
        self.state = None

    #### login & regis & homes
    def show_login(self):  # init / regis_login
        self.login = LoginWindow()
        self.login.switch_regis.connect(self.show_regis)
        self.login.switch_home0.connect(self.show_home0)
        self.login.switch_home1.connect(self.show_home1)
        self.login.switch_home2.connect(self.show_home2)
        self.login.show()

    def show_regis(self):  # login_regis
        self.regis = RegisWindow()
        self.login.close()
        self.regis.return_login.connect(self.regis_login)
        self.regis.show()

    def regis_login(self):  # regis_login
        self.regis.close()
        self.show_login()

    def show_home0(self):  # login_home0 / others_home0: e.g. self.showMR
        self.account = self.login.account
        self.name = self.login.name
        self.age = self.login.age
        self.sex = self.login.sex
        self.state = self.login.state
        self.home0 = Home0Window(self.account, self.name, self.age, self.sex, self.state)
        try:
            self.login.close()
        except:
            pass
        self.home0.switch_MS.connect(self.show_MS0)
        self.home0.switch_Affair.connect(self.show_Affair)
        self.home0.switch_Shop.connect(self.show_Shop)
        self.home0.show()

    def show_home1(self):  # login_home1 / others_home1
        self.account = self.login.account
        self.name = self.login.name
        self.age = self.login.age
        self.sex = self.login.sex
        self.state = self.login.state
        self.home1 = Home1Window(self.account, self.name, self.age, self.sex, self.state)
        try:
            self.login.close()
        except:
            pass
        self.home1.switch_MS.connect(self.show_MS1)
        self.home1.switch_TC.connect(self.show_TC)
        self.home1.show()

    def show_home2(self):  # login_home2 / AT1_home2 / AT2_home2
        self.account = self.login.account
        self.name = self.login.name
        self.age = self.login.age
        self.sex = self.login.sex
        self.state = self.login.state
        self.home2 = Home2Window(self.account, self.name, self.age, self.sex, self.state)
        # print('account: {}'.format(self.account))
        try:
            self.login.close()
        except:
            pass
        try:
            self.AT1.close()
        except:
            pass
        try:
            self.AT2.close()
        except:
            pass
        self.home2.switch_AT1.connect(self.show_AT1)
        self.home2.switch_AT2.connect(self.show_AT2)
        self.home2.switch_VI.connect(self.show_VI)
        self.home2.show()

    def show_AT1(self):  # home2_AT1
        self.AT1 = AT1Window()
        self.home2.close()
        self.AT1.switch_MS.connect(self.show_MS2)
        self.AT1.switch_MR.connect(self.show_MR)
        self.AT1.switch_MA.connect(self.show_MA)
        self.AT1.return_home2.connect(self.show_home2)
        self.AT1.show()

    def show_AT2(self):  # home2_AT2
        self.AT2 = AT2Window()
        self.home2.close()
        self.AT2.switch_AP.connect(self.show_AP)
        self.AT2.switch_TJ.connect(self.show_TJ)
        self.AT2.return_home2.connect(self.show_home2)
        self.AT2.show()

    #### XX_home0
    def Affair_home0(self):   # Affair_home0
        self.Affair.close()
        self.show_home0()

    def Affair_AH(self):  # Affair_AH
        self.show_AH()

    def return_Affair(self):  # AH_Affair
        self.AH.close()

    def MS0_home0(self):  # MS0_home0
        self.MS0.close()
        self.show_home0()

    def Shop_home0(self):  # Shop_home0
        self.Shop.close()
        self.show_home0()

    def Shop_History(self):  # Shop_History
        self.show_History()

    def return_Shop(self):  # History_Shop
        self.History.close()

    #### show_XX(home0)
    def show_Affair(self):  # home0_Affair
        self.Affair = AffairWindow(self.account)
        self.home0.close()
        try:
            self.AH.close()
        except:
            pass
        self.Affair.show_history.connect(self.Affair_AH)
        self.Affair.return_home0.connect(self.Affair_home0)
        self.Affair.show()

    def show_AH(self):  # home0_AH
        self.AH = AHWindow(self.account)
        self.AH.return_affair.connect(self.return_Affair)
        self.AH.show()

    def show_MS0(self):  # home0_MS0
        self.MS0 = MSWindow()
        self.home0.close()
        self.MS0.return_home.connect(self.MS0_home0)
        self.MS0.show()

    def show_Shop(self):  # home0_Shop
        self.Shop = ShopWindow(self.account)
        self.home0.close()
        try:
            self.History.close()
        except:
            pass
        self.Shop.show_history.connect(self.Shop_History)
        self.Shop.return_home0.connect(self.Shop_home0)
        self.Shop.show()

    def show_History(self):  # Shop_History
        self.History = HistoryWindow(self.account)
        self.History.return_shop.connect(self.return_Shop)
        self.History.show()

    #### XX_home1
    def MS1_home1(self):  # MS1_home1
        self.MS1.close()
        self.show_home1()

    def TC_home1(self):  # TC_home1
        self.TC.close()
        self.show_home1()

    def TC_TH(self):  # TC_TH
        self.show_TH()

    def return_TC(self):  # TH_TC
        self.TH.close()

    #### show_XX(home1)
    def show_MS1(self):  # home1_MS1
        self.MS1 = MSWindow()
        self.home1.close()
        self.MS1.return_home.connect(self.MS1_home1)
        self.MS1.show()

    def show_TC(self):  # home1_TC
        self.TC = TCWindow(self.account)
        self.home1.close()
        try:
            self.TH.close()
        except:
            pass
        self.TC.show_history.connect(self.TC_TH)
        self.TC.return_home0.connect(self.TC_home1)
        self.TC.show()

    def show_TH(self):  # TC_TH
        self.TH = THWindow(self.account)
        self.TH.return_TC.connect(self.return_TC)
        self.TH.show()

    #### XX_home2
    def MR_AT1(self):  # MR_AT1
        self.MR.close()
        self.show_AT1()

    def MA_AT1(self):  # MA_AT1
        self.MA.close()
        self.show_AT1()

    def MS2_AT1(self):  # MS2_AT1
        self.MS2.close()
        self.show_AT1()

    def AP_AT2(self):  # AP_AT2
        self.AP.close()
        self.show_AT2()

    def VI_home2(self):  # VI_home2
        self.VI.close()
        self.show_home2()

    def TJ_AT2(self):  # TJ_AT2
        self.TJ.close()
        self.show_AT2()

    #### show_XX(home2)
    def show_MR(self):  # AT1_MR
        self.MR = MRWindow()
        self.AT1.close()
        self.MR.return_home2.connect(self.MR_AT1)
        self.MR.show()

    def show_MA(self):  # AT1_MA
        self.MA = MAWindow()
        self.AT1.close()
        self.MA.return_home2.connect(self.MA_AT1)
        self.MA.show()

    def show_MS2(self):  # AT1_MS2
        self.MS2 = MSWindow()
        try:
            self.AT1.close()
        except:
            pass
        self.MS2.return_home.connect(self.MS2_AT1)
        self.MS2.show()

    def show_AP(self):  # AT2_AP
        self.AP = APWindow()
        self.AT2.close()
        self.AP.return_home2.connect(self.AP_AT2)
        self.AP.show()

    def show_VI(self):  # Home2_VI
        self.VI = VIWindow()
        self.home2.close()
        self.VI.return_home2.connect(self.VI_home2)
        self.VI.show()

    def show_TJ(self):  # AT2_TJ
        self.TJ = TJWindow()
        self.AT2.close()
        self.TJ.return_home2.connect(self.TJ_AT2)
        self.TJ.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    cont = Controller()
    cont.show_login()
    sys.exit(app.exec_())
