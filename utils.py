import time
import pymysql
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from DataBase_Course.py_ui.ui_design import *  # Here input your own route(relative route is OK)
_translate = QtCore.QCoreApplication.translate


#  Here we define a function to get connection to the database via the package pymysql.
#  Defining such a function will be convenient when the usage is frequent later.
#  For further improvement, we can define 'self.conn = get_conn()' in each window class to avoid unnecessary repetition.
def get_conn():
    user = ''  # Here input your own user account
    password = ''  # Here input your own user password
    return pymysql.connect(host='127.0.0.1',
                           user=user,
                           password=password,
                           db='final')  # Please ensure that your database is named 'final'!


#  Then we will define all the window classes we need and the functions to realize their utility in the following part.
class AT1Window(QMainWindow, AT1_MainWindow):
    switch_MS = pyqtSignal()
    switch_MR = pyqtSignal()
    switch_MA = pyqtSignal()
    return_home2 = pyqtSignal()

    def __init__(self):
        super(AT1Window, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('比赛信息处理')
        self.set_callbacks()

    def set_callbacks(self):
        self.pushButton.clicked.connect(self.GoMS)
        self.pushButton_2.clicked.connect(self.GoMR)
        self.pushButton_3.clicked.connect(self.GoMA)
        self.pushButton_4.clicked.connect(self.GoHome2)

    def GoHome2(self):
        self.return_home2.emit()

    def GoMS(self):
        self.switch_MS.emit()

    def GoMA(self):
        self.switch_MA.emit()

    def GoMR(self):
        self.switch_MR.emit()


class AT2Window(QMainWindow, AT2_MainWindow):
    switch_AP = pyqtSignal()
    switch_TJ = pyqtSignal()
    return_home2 = pyqtSignal()

    def __init__(self):
        super(AT2Window, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('申请审批管理')
        self.set_callbacks()

    def set_callbacks(self):
        self.pushButton.clicked.connect(self.GoAP)
        self.pushButton_2.clicked.connect(self.GoTJ)
        self.pushButton_4.clicked.connect(self.GoHome2)

    def GoHome2(self):
        self.return_home2.emit()

    def GoAP(self):
        self.switch_AP.emit()

    def GoTJ(self):
        self.switch_TJ.emit()


class AffairWindow(QMainWindow, Affair_Form):
    return_home0 = pyqtSignal()
    show_history = pyqtSignal()

    def __init__(self, acc):
        super(AffairWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('场务申请')
        self.set_callbacks()
        self.account = acc

    def set_callbacks(self):
        self.pushButton.clicked.connect(self.affair)
        self.pushButton_7.clicked.connect(self.GoHome0)
        self.pushButton_2.clicked.connect(self.history)

    def GoHome0(self):
        self.return_home0.emit()

    def affair(self):
        mno = self.lineEdit.text()
        detail = self.lineEdit_2.text()
        if len(detail) > 10:
            print(QMessageBox.warning(self, '错误', '备注信息过长', QMessageBox.Yes, QMessageBox.Yes))
        else:
            conn = get_conn()
            cur = conn.cursor()
            sql = 'SELECT MNo FROM final.match;'
            cur.execute(sql)
            mno_list = []
            data = cur.fetchall()
            for item in data:
                mno_list.append(item[0])
            if mno not in mno_list:
                print(QMessageBox.warning(self, '错误', '比赛不存在', QMessageBox.Yes, QMessageBox.Yes))
            else:
                sql = 'SELECT State FROM final.match WHERE `MNo`=\'{}\';'.format(mno)
                cur.execute(sql)
                state = cur.fetchall()[0][0]
                if state == 1:
                    print(QMessageBox.warning(self, '错误', '比赛已结束', QMessageBox.Yes, QMessageBox.Yes))
                else:
                    sql = 'SELECT Account FROM final.affairrequest WHERE `MNo`=\'{}\';'.format(mno)
                    cur.execute(sql)
                    data = cur.fetchall()
                    acc_list = []
                    for item in data:
                        acc_list.append(item[0])
                    if self.account in acc_list:
                        print(QMessageBox.warning(self, '错误', '该场比赛已经提交过申请', QMessageBox.Yes, QMessageBox.Yes))
                    else:
                        sql = 'INSERT INTO final.affairrequest (`MNo`,`Account`,`State`,`Detail`) VALUES (\'{}\',' \
                              '\'{}\',0,\'{}\');'.format(mno, self.account, detail)
                        cur.execute(sql)
                        conn.commit()
                        print(QMessageBox.information(self, '提示', '申请提交成功', QMessageBox.Yes, QMessageBox.Yes))
                        cur.close()

    def history(self):
        self.show_history.emit()


class AHWindow(QMainWindow, AH_Form):
    return_affair = pyqtSignal()

    def __init__(self, acc):
        super(AHWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('查看场务申请历史记录')
        self.tableWidget.setHorizontalHeaderLabels(['比赛编号', '备注信息', '审批状态'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        for i in range(3):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Interactive)
        self.set_callbacks()
        self.info = self.get_rows()
        print(self.info)
        self.add_rows()
        self.show_data()
        self.account = acc

    def set_callbacks(self):
        self.pushButton.clicked.connect(self.GoAffair)

    def GoAffair(self):
        self.return_affair.emit()

    def get_rows(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = 'SELECT * FROM final.affairrequest;'
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        info_list = []
        for item in data:
            info_list.append(item)
        return info_list

    def get_pos(self):
        try:
            row = self.tableWidget.selectedItems()[0].row()
            return row
        except:
            return

    def add_rows(self):
        info = self.get_rows()
        n_row = len(info)
        if n_row > 1:
            for i in range(1, n_row):
                self.tableWidget.insertRow(i)

    def show_data(self):
        info_list = self.get_rows()
        n_row = len(info_list)
        print(info_list)
        flag = False
        for i in range(n_row):
            info = info_list[i]
            state = info[2]
            if state == 0:
                state = '未审批'
            elif state == 1:
                state = '通过'
            elif state == 2:
                state = '不通过'
            data = [info[0], info[3], state]
            for j in range(3):
                item = QTableWidgetItem(str(data[j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, j, item)
            if len(info[3]) >= 8:
                flag = True
                self.tableWidget.resizeColumnToContents(1)
        if not flag:
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return info_list


class APWindow(QMainWindow, AP_Form):
    return_home2 = pyqtSignal()

    def __init__(self):
        super(APWindow, self).__init__()
        self.setupUi(self)
        self.set_callbacks()
        self.setWindowTitle('场务申请审批')
        self.info = self.get_rows()
        self.add_rows()
        self.info_list = self.show_data()

    def set_callbacks(self):
        self.tableWidget.setHorizontalHeaderLabels(['比赛编号', '申请者账号', '申请者姓名', '申请状态', '备注', '选择'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.pushButton.clicked.connect(self.GoHome2)

    def GoHome2(self):
        self.return_home2.emit()

    def add_buttons(self):
        n_row = self.tableWidget.rowCount()
        for i in range(n_row):
            self.tableWidget.setCellWidget(i, self.tableWidget.columnCount() - 1, self.buttonForRow())

    def buttonForRow(self):
        widget = QWidget()
        self.updateBtn = QtWidgets.QPushButton('审批')
        self.updateBtn.setStyleSheet(''' text-align : center;
                                                  background-color : NavajoWhite;
                                                  height : 25px;
                                                  border-style: outset;
                                                  font : 13px  ''')
        self.updateBtn.clicked.connect(self.check)
        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(self.updateBtn)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget

    def get_rows(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = 'SELECT * FROM final.affairrequest;'
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        info_list = []
        for item in data:
            info_list.append((item[0], item[1]))
        return info_list

    def add_rows(self):
        n_row = len(self.info)
        if n_row > 1:
            for i in range(1, n_row):
                self.tableWidget.insertRow(i)
        self.add_buttons()

    def show_data(self):
        n_row = len(self.info)
        conn = get_conn()
        cur = conn.cursor()
        sql = 'SELECT * FROM final.affairrequest;'
        cur.execute(sql)
        data = cur.fetchall()
        info_list = []
        acc_list = []
        state_list = []
        for item in data:
            sub_list = []
            for num in item:
                sub_list.append(num)
            acc_list.append(item[1])
            state_list.append(item[2])
            info_list.append(sub_list)
        # print(info_list)
        i = 0
        for acc in acc_list:
            sql = 'SELECT Name FROM final.user WHERE `Account`=\'{}\';'.format(acc)
            cur.execute(sql)
            info_list[i].insert(2, cur.fetchall()[0][0])
            if state_list[i] == 0:
                info_list[i][3] = '未审批'
            elif state_list[i] == 1:
                info_list[i][3] = '通过'
            elif state_list[i] == 2:
                info_list[i][3] = '不通过'
            i += 1
        for i in range(n_row):
            data = info_list[i]
            for j in range(0, 5):
                item = QTableWidgetItem(data[j])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, j, item)
        cur.close()
        return info_list

    def check(self):
        button = self.sender()
        info = self.info_list
        if button:
            row = self.tableWidget.indexAt(button.parent().pos()).row()
            state = 0
            reply = QMessageBox.information(self, '审批', '是否通过？', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == 16384:
                state = 1
                print(QMessageBox.information(None, '操作完成', '审批通过！', QMessageBox.Yes, QMessageBox.Yes))
            elif reply == 65536:
                state = 2
                print(QMessageBox.information(None, '操作完成', '审批不通过！', QMessageBox.Yes, QMessageBox.Yes))
            reply = info[row][4]
            mno = info[row][0]
            acc = info[row][1]
            conn = get_conn()
            cur = conn.cursor()  # 其实Detail可以不用重置
            sql = 'UPDATE final.affairrequest SET `State`={}, `Detail`=\'{}\' WHERE `MNo`=\'{}\' AND `Account`=\'{}\';'.format(state, reply, mno, acc)
            cur.execute(sql)
            conn.commit()
            cur.close()
            self.info_list = self.show_data()


class HistoryWindow(QMainWindow, History_Form):
    return_shop = pyqtSignal()

    def __init__(self, acc):
        super(HistoryWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('查看购物历史记录')
        self.tableWidget.setHorizontalHeaderLabels(['订单编号', '订单时间', '订单金额'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        for i in range(3):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Interactive)
        self.set_callbacks()
        self.info = self.get_rows()
        print(self.info)
        self.add_rows()
        self.show_data()
        self.account = acc

    def set_callbacks(self):
        self.pushButton.clicked.connect(self.View)
        self.pushButton_2.clicked.connect(self.GoShop)

    def GoShop(self):
        self.return_shop.emit()

    def get_rows(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = 'SELECT * FROM final.itemdeal;'
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        info_list = []
        for item in data:
            info_list.append(item)
        return info_list

    def get_pos(self):
        try:
            row = self.tableWidget.selectedItems()[0].row()
            return row
        except:
            return

    def add_rows(self):
        info = self.get_rows()
        n_row = len(info)
        if n_row > 1:
            for i in range(1, n_row):
                self.tableWidget.insertRow(i)

    def show_data(self):
        info = self.get_rows()
        n_row = len(info)
        print(info)
        flag = False
        for i in range(n_row):
            data = info[i]
            for j in range(3):
                item = QTableWidgetItem(str(data[j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, j, item)
            if len(data[1]) >= 10:
                flag = True
                self.tableWidget.resizeColumnToContents(1)
        print(flag)
        if not flag:
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return info

    def View(self):
        info = self.info
        row = self.get_pos()
        if row is None:
            print(QMessageBox.warning(self, '错误', '未选择记录', QMessageBox.Yes, QMessageBox.Yes))
        else:
            print(info[row])
            conn = get_conn()
            cur = conn.cursor()
            id_no = info[row][0]
            sql = 'SELECT * FROM final.itemsale WHERE `IDNo`=\'{}\';'.format(id_no)
            cur.execute(sql)
            data = cur.fetchall()
            data = list(data)
            print(data)
            ino_list = []
            for item in data:
                ino_list.append(item[0])
            iname_list = []
            for ino in ino_list:
                sql = 'SELECT IName FROM final.item WHERE `INO`=\'{}\';'.format(ino)
                cur.execute(sql)
                iname_list.append(cur.fetchall()[0][0])
            print(iname_list)
            res = ''
            ind = 0
            for item in data:
                res += '订单编号：{} | 商品名称：{} | 购买数量：{} | 金额小计：{}\n'.format(item[1], iname_list[ind], str(item[2]), str(item[3]))
                ind += 1
            res = QMessageBox.information(self, '查询结果', res, QMessageBox.Yes, QMessageBox.Yes)
            print(res)
            cur.close()


class Home0Window(QMainWindow, Home0_MainWindow):
    switch_MS = pyqtSignal()
    switch_Shop = pyqtSignal()
    switch_Affair = pyqtSignal()

    def __init__(self, acc, name, age, sex, state):
        super(Home0Window, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('观众主界面')
        self.set_callbacks()
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">账号：{}</span></p></body></html>".format(acc)))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">姓名：{}</span></p></body></html>".format(name)))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">性别：{}</span></p></body></html>".format(sex)))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">年龄：{}</span></p></body></html>".format(age)))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">权限：{}</span></p></body></html>".format(state)))

    def set_callbacks(self):
        self.pushButton.clicked.connect(self.GoMS)
        self.pushButton_2.clicked.connect(self.GoShop)
        self.pushButton_3.clicked.connect(self.GoAffair)

    def GoMS(self):
        self.switch_MS.emit()

    def GoShop(self):
        self.switch_Shop.emit()

    def GoAffair(self):
        self.switch_Affair.emit()


class Home1Window(QMainWindow, Home1_MainWindow):
    switch_MS = pyqtSignal()
    switch_TC = pyqtSignal()

    def __init__(self, acc, name, age, sex, state):
        super(Home1Window, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('球队主界面')
        self.set_callbacks()
        self.account = acc
        self.tname = self.get_tname()
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">账号：{}</span></p></body></html>").format(acc))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">姓名：{}</span></p></body></html>").format(name))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">性别：{}</span></p></body></html>").format(sex))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">年龄：{}</span></p></body></html>").format(age))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">权限：{}</span></p></body></html>").format(state))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">球队：{}</span></p></body></html>").format(self.tname))

    def get_tname(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = 'SELECT Team FROM final.teamleader WHERE `Account`=\'{}\';'.format(self.account)
        cur.execute(sql)
        tno = cur.fetchall()[0][0]
        sql = 'SELECT TName FROM final.team WHERE `TNo`=\'{}\';'.format(tno)
        cur.execute(sql)
        return cur.fetchall()[0][0]

    def set_callbacks(self):
        self.pushButton.clicked.connect(self.GoMS)
        self.pushButton_3.clicked.connect(self.GoTC)

    def GoMS(self):
        self.switch_MS.emit()

    def GoTC(self):
        self.switch_TC.emit()


class Home2Window(QMainWindow, Home2_MainWindow):
    switch_AT1 = pyqtSignal()
    switch_AT2 = pyqtSignal()
    switch_VI = pyqtSignal()

    def __init__(self, acc, name, age, sex, state):
        super(Home2Window, self).__init__()
        self.setupUi(self)
        self.set_callbacks()
        self.setWindowTitle('管理员主界面')
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">账号：{}</span></p></body></html>".format(acc)))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">姓名：{}</span></p></body></html>".format(name)))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">性别：{}</span></p></body></html>".format(sex)))
        self.label_5.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">年龄：{}</span></p></body></html>".format(age)))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">权限：{}</span></p></body></html>".format(state)))

    def set_callbacks(self):
        self.pushButton.clicked.connect(self.GoAT1)
        self.pushButton_3.clicked.connect(self.GoAT2)
        self.pushButton_2.clicked.connect(self.GoVI)

    def GoAT1(self):
        self.switch_AT1.emit()

    def GoAT2(self):
        self.switch_AT2.emit()

    def GoVI(self):
        self.switch_VI.emit()


class LoginWindow(QMainWindow, Login_Form):
    switch_regis = pyqtSignal()
    switch_home0 = pyqtSignal()
    switch_home1 = pyqtSignal()
    switch_home2 = pyqtSignal()

    def __init__(self):
        super(LoginWindow, self).__init__()
        self.setupUi(self)
        self.set_callbacks()
        self.setWindowTitle('登录')
        self.account = None
        self.name = None
        self.sex = None
        self.age = 0
        self.state = None
        self.textEdit.setFocusPolicy(Qt.NoFocus)
        self.lineEdit.setFocusPolicy(Qt.NoFocus)

    def set_callbacks(self):
        self.pushButton.clicked.connect(self.Login)
        self.pushButton_2.clicked.connect(self.GoRegis)
        self.lineEdit_2.returnPressed.connect(self.Login)
        self.lineEdit_3.returnPressed.connect(self.Login)

    def GoRegis(self):
        self.switch_regis.emit()

    def Login(self):
        userid = self.lineEdit_2.text()
        password = self.lineEdit_3.text()
        if userid == '' or password == '':
            print(QMessageBox.warning(self, '警告', '不可为空', QMessageBox.Yes, QMessageBox.Yes))
        else:
            conn = get_conn()
            cur = conn.cursor()
            sql = 'SELECT * FROM user'
            cur.execute(sql)
            data = cur.fetchall()
            data_dict = {'user_id': [], 'passwd': []}
            for item in data:
                data_dict['user_id'].append(item[0])
                data_dict['passwd'].append(item[1])

            if userid not in data_dict['user_id']:
                print(QMessageBox.warning(None, '提示', '账号不存在', QMessageBox.Yes, QMessageBox.Yes))
            else:
                ind = data_dict['user_id'].index(userid)
                t_passwd = data_dict['passwd'][ind]
                if t_passwd == password:
                    print(QMessageBox.information(None, '提示', '登录成功！', QMessageBox.Yes, QMessageBox.Yes))
                    sql = 'SELECT * FROM final.user WHERE `Account`=\'{}\';'.format(userid)
                    cur.execute(sql)
                    data = cur.fetchall()[0]
                    self.account = userid
                    self.name = data[2]
                    self.age = data[3]
                    self.sex = data[4]
                    state = data[5]
                    if state == 0:
                        self.state = '观众'
                        self.switch_home0.emit()
                    elif state == 1:
                        self.state = '球队'
                        self.switch_home1.emit()
                    elif state == 2:
                        self.state = '管理员'
                        self.switch_home2.emit()
                else:
                    print(QMessageBox.warning(None, '提示', '密码错误！', QMessageBox.Yes, QMessageBox.Yes))
            cur.close()
            return


class MAWindow(QMainWindow, MA_Form):
    return_home2 = pyqtSignal()

    def __init__(self):
        super(MAWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('比赛信息添加')
        self.set_callbacks()

    def set_callbacks(self):
        self.pushButton.clicked.connect(self.MA)
        self.pushButton_2.clicked.connect(self.GoHome2)

    def GoHome2(self):
        self.return_home2.emit()

    def MA(self):
        mno = self.lineEdit_5.text()
        time = self.lineEdit.text()
        ref = self.lineEdit_3.text()
        court = self.lineEdit_4.text()
        h_tno = self.lineEdit_6.text()
        g_tno = self.lineEdit_2.text()

        conn = get_conn()
        cur = conn.cursor()
        sql = 'SELECT `MNo` FROM final.match'
        cur.execute(sql)
        data = cur.fetchall()
        mno_list = []
        for item in data:
            mno_list.append(item[0])
        court_list = []
        sql = 'SELECT CName FROM final.court;'
        cur.execute(sql)
        data = cur.fetchall()
        if data is not None:
            for item in data:
                court_list.append(item[0])
        print(court_list)
        tno_list = []
        sql = 'SELECT TNo FROM final.team;'
        cur.execute(sql)
        data = cur.fetchall()
        if data is not None:
            for item in data:
                tno_list.append(item[0])
        if mno in mno_list:
            print(QMessageBox.warning(self, '错误', '比赛已存在', QMessageBox.Yes, QMessageBox.Yes))
        elif court not in court_list:
            print(QMessageBox.warning(self, '错误', '场地不存在', QMessageBox.Yes, QMessageBox.Yes))
        elif len(time) != 17:
            print(QMessageBox.warning(self, '错误', '时间输入有误', QMessageBox.Yes, QMessageBox.Yes))
        elif h_tno not in tno_list:
            print(QMessageBox.warning(self, '错误', '主队不存在', QMessageBox.Yes, QMessageBox.Yes))
        elif g_tno not in tno_list:
            print(QMessageBox.warning(self, '错误', '客队不存在', QMessageBox.Yes, QMessageBox.Yes))
        elif h_tno == g_tno:
            print(QMessageBox.warning(self, '错误', '主客队相同', QMessageBox.Yes, QMessageBox.Yes))
        else:
            sql = 'SELECT CNo FROM final.court WHERE `CName`=\'{}\';'.format(court)
            cur.execute(sql)
            court = cur.fetchall()[0][0]
            sql = 'INSERT INTO final.match (`MNo`, `Time`, `State`, `Referee`, `Court`) VALUES (\'{}\',\'{}\',0,\'{}\',' \
                  '\'{}\');'.format(mno, time, ref, court)
            cur.execute(sql)
            conn.commit()
            sql = 'INSERT INTO final.homematch (`HomeMatchNo`,`HomeTeamNo`,`Score`,`Result`) VALUES (\'{}\',\'{}\',0,' \
                  '\'N\')'.format(mno, h_tno)
            cur.execute(sql)
            conn.commit()
            sql = 'INSERT INTO final.guestmatch (`GuestMatchNo`,`GuestTeamNo`,`Score`,`Result`) VALUES (\'{}\',' \
                  '\'{}\',0,\'N\');'.format(mno, g_tno)
            cur.execute(sql)
            conn.commit()
            cur.close()
            print(QMessageBox.information(self, '提示', '添加成功', QMessageBox.Yes, QMessageBox.Yes))
        return


class MRWindow(QMainWindow, MR_Form):
    return_home2 = pyqtSignal()

    def __init__(self):
        super(MRWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('比赛结果记录')
        self.set_callbacks()

    def set_callbacks(self):
        self.pushButton_3.clicked.connect(self.MR)
        self.pushButton_4.clicked.connect(self.GoHome2)

    def GoHome2(self):
        self.return_home2.emit()

    def MR(self):
        mno = self.lineEdit_2.text()
        home_tno = self.lineEdit_3.text()
        guest_tno = self.lineEdit.text()
        info = self.lineEdit_4.text()
        print('比赛编号:{}\n主队编号:{}\n客队编号:{}\n比分信息:{}'.format(mno, home_tno, guest_tno, info))

        if mno == '' or home_tno == '' or guest_tno == '' or info == '':
            print(QMessageBox.warning(self, '警告', '不可为空', QMessageBox.Yes, QMessageBox.Yes))
        else:
            conn = get_conn()
            cur = conn.cursor()
            sql = 'SELECT MNo FROM Final.match;'
            cur.execute(sql)
            data = cur.fetchall()
            mno_list = []
            for item in data:
                mno_list.append(item[0])
            sql = 'SELECT TNo FROM final.team;'
            cur.execute(sql)
            data = cur.fetchall()
            tno_list = []
            for item in data:
                tno_list.append(item[0])
            print(tno_list)
            if mno not in mno_list:
                print(QMessageBox.warning(self, '警告', '比赛不存在', QMessageBox.Yes, QMessageBox.Yes))
            else:
                sql = 'SELECT * FROM final.homematch WHERE `HomeMatchNo`=\'{}\';'.format(mno)
                cur.execute(sql)
                home_data = cur.fetchall()[0]
                htno_true = home_data[1]
                sql = 'SELECT * FROM final.guestmatch WHERE `GuestMatchNo`=\'{}\';'.format(mno)
                cur.execute(sql)
                guest_data = cur.fetchall()[0]
                gtno_true = guest_data[1]
                if home_tno not in tno_list:
                    print(QMessageBox.warning(self, '警告', '主队不存在', QMessageBox.Yes, QMessageBox.Yes))
                elif guest_tno not in tno_list:
                    print(QMessageBox.warning(self, '警告', '客队不存在', QMessageBox.Yes, QMessageBox.Yes))
                elif home_tno != htno_true:
                    print(QMessageBox.warning(self, '警告', '主队错误', QMessageBox.Yes, QMessageBox.Yes))
                elif guest_tno != gtno_true:
                    print(QMessageBox.warning(self, '警告', '客队错误', QMessageBox.Yes, QMessageBox.Yes))
                else:
                    ind = info.find('-')
                    if ind == -1:
                        print(QMessageBox.warning(self, '错误', '比分输入错误', QMessageBox.Yes, QMessageBox.Yes))
                    else:
                        home_score = int(info[:ind])
                        guest_score = int(info[ind + 1:])
                        if home_score == guest_score:
                            print(QMessageBox.warning(self, '错误', '两队比分相同', QMessageBox.Yes, QMessageBox.Yes))
                        else:
                            # First deal with home team info
                            # get home team statistics
                            sql = 'SELECT `Statistic`,`NetScore` FROM final.team WHERE `TNo`=\'{}\';'.format(home_tno)
                            cur.execute(sql)
                            data = cur.fetchall()[0]
                            stat = data[0]
                            win = int(stat[1:3])
                            lose = int(stat[5:7])
                            net = data[1]
                            # judge win or lose for home and guest
                            if home_score > guest_score:
                                home_res = 'W'
                                guest_res = 'L'
                            elif home_score < guest_score:
                                home_res = 'L'
                                guest_res = 'W'
                            # update home match info
                            sql = 'UPDATE final.homematch SET `Score`={},`Result`=\'{}\' WHERE `HomeTeamNo`=\'{}\' AND ' \
                                  '`HomeMatchNo`=\'{}\';'.format(home_score, home_res, home_tno, mno)
                            cur.execute(sql)
                            conn.commit()
                            # check whether this is insert or update
                            res = home_data[3]
                            if res == 'N':  # insert
                                print(QMessageBox.information(self, '提示', '主队信息添加成功', QMessageBox.Yes, QMessageBox.Yes))
                            else:  # update
                                print(QMessageBox.information(self, '提示', '主队信息更改成功', QMessageBox.Yes, QMessageBox.Yes))
                                if res == 'W':  # 需要扣除这场比赛的信息
                                    win -= 1
                                elif res == 'L':
                                    lose -= 1
                                net += (guest_data[2] - home_data[2])
                            if home_res == 'W':
                                win += 1
                            elif home_res == 'L':
                                lose += 1
                            win = '%02d' % win
                            lose = '%02d' % lose
                            stat = 'W{}-L{}'.format(win, lose)
                            net += (home_score - guest_score)
                            # update home team info
                            sql = 'UPDATE final.team SET `Statistic`=\'{}\',`NetScore`=\'{}\' WHERE `TNo`=\'{}\';'.format(
                                stat, net, home_tno)
                            cur.execute(sql)
                            conn.commit()

                            # Next deal with guest team info
                            # get guest team statistics
                            sql = 'SELECT `Statistic`,`NetScore` FROM final.team WHERE `TNo`=\'{}\';'.format(guest_tno)
                            cur.execute(sql)
                            data = cur.fetchall()[0]
                            stat = data[0]
                            win = int(stat[1:3])
                            lose = int(stat[5:7])
                            net = data[1]
                            # update guest match info
                            sql = 'UPDATE final.guestmatch SET `Score`={},`Result`=\'{}\' WHERE `GuestTeamNo`=\'{}\' ' \
                                  'AND `GuestMatchNo`=\'{}\';'.format(guest_score, guest_res, guest_tno, mno)
                            cur.execute(sql)
                            conn.commit()
                            # check whether this is insert or update
                            res = guest_data[3]
                            if res == 'N':
                                print(QMessageBox.information(self, '提示', '客队信息添加成功', QMessageBox.Yes, QMessageBox.Yes))
                            else:
                                print(QMessageBox.information(self, '提示', '客队信息更改成功', QMessageBox.Yes, QMessageBox.Yes))
                                if res == 'W':  # 需要扣除这场比赛的信息
                                    win -= 1
                                elif res == 'L':
                                    lose -= 1
                                net += (home_data[2] - guest_data[2])
                            if guest_res == 'W':
                                win += 1
                            elif guest_res == 'L':
                                lose += 1
                            win = '%02d' % win
                            lose = '%02d' % lose
                            stat = 'W{}-L{}'.format(win, lose)
                            net += (guest_score - home_score)
                            # update guest team info
                            sql = 'UPDATE final.team SET `Statistic`=\'{}\',`NetScore`=\'{}\' WHERE `TNo`=\'{}\';'.format(
                                stat, net, guest_tno)
                            cur.execute(sql)
                            conn.commit()
                            # update match info
                            sql = 'UPDATE final.match SET `State`=1 WHERE (`MNo`=\'{}\');'.format(mno)
                            cur.execute(sql)
                            conn.commit()
                            cur.close()
        return


class MSWindow(QMainWindow, MS_Form):
    return_home = pyqtSignal()

    def __init__(self):
        super(MSWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('比赛信息查询')
        self.set_callbacks()

    def set_callbacks(self):
        self.pushButton.clicked.connect(self.MS1)
        self.pushButton_2.clicked.connect(self.MS2)
        self.pushButton_3.clicked.connect(self.GoHome)

    def GoHome(self):
        self.return_home.emit()

    def search(self, mno):  # 根据MNo查找单场比赛信息并返回文本
        conn = get_conn()
        cur = conn.cursor()
        sql = 'SELECT * FROM final.match WHERE `MNo`=\'{}\';'.format(mno)
        cur.execute(sql)
        data = cur.fetchall()
        state = data[0][2]
        match_time = data[0][1]
        cno = data[0][4]
        sql = 'SELECT CName FROM final.court WHERE `CNo`=\'{}\';'.format(cno)
        cur.execute(sql)
        match_court = cur.fetchall()[0][0]
        text = '\n比赛编号：{} | 比赛时间：{} | 比赛场地：{}\n'.format(mno, match_time, match_court)
        sql = 'SELECT `HomeTeamNo`,`Score` FROM final.homematch WHERE `HomeMatchNo`=\'{}\';'.format(mno)
        cur.execute(sql)
        data = cur.fetchall()
        ht_list = data[0]  # {TNo, Score, Result}
        sql = 'SELECT `GuestTeamNo`,`Score` FROM final.guestmatch WHERE `GuestMatchNo`=\'{}\';'.format(mno)
        cur.execute(sql)
        data = cur.fetchall()
        gt_list = data[0]
        sql = 'SELECT `TName` FROM final.team WHERE `TNo`=\'{}\''.format(ht_list[0])
        cur.execute(sql)
        ht_name = cur.fetchall()[0][0]
        sql = 'SELECT `TName` FROM final.team WHERE `TNo`=\'{}\''.format(gt_list[0])
        cur.execute(sql)
        gt_name = cur.fetchall()[0][0]
        cur.close()
        text += '赛果：（客）{} {} —— {} {}（主）\n'.format(gt_name, gt_list[1],  ht_list[1], ht_name)
        if state == 0:
            text += '比赛未开始！\n'
        return text

    def MS1(self):  # 根据MNo查询，返回单场比赛结果
        mno = self.lineEdit.text()
        if mno == '':
            print(QMessageBox.warning(self, '警告', '不可为空', QMessageBox.Yes, QMessageBox.Yes))
        else:
            conn = get_conn()
            cur = conn.cursor()
            sql = 'SELECT MNo FROM final.match;'
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            mno_list = []
            for item in data:
                mno_list.append(item[0])
            if mno not in mno_list:
                print(QMessageBox.warning(self, '警告', '比赛信息不存在', QMessageBox.Yes, QMessageBox.Yes))
            else:
                text = self.search(mno)
                print(QMessageBox.information(self, '结果', text, QMessageBox.Yes, QMessageBox.Yes))

    def MS2(self):  # 根据TNo查找比赛信息
        tno = self.lineEdit_2.text()
        if tno == '':
            print(QMessageBox.warning(self, '警告', '不可为空', QMessageBox.Yes, QMessageBox.Yes))
        else:
            conn = get_conn()
            cur = conn.cursor()
            tno_list = []
            sql = 'SELECT TNo FROM final.team;'
            cur.execute(sql)
            data = cur.fetchall()
            for item in data:
                tno_list.append(item[0])
            if tno not in tno_list:
                print(QMessageBox.warning(self, '错误', '该队不存在', QMessageBox.Yes, QMessageBox.Yes))
            else:
                mno_list = []
                sql = 'SELECT HomeMatchNo FROM final.homematch WHERE `HomeTeamNo`=\'{}\';'.format(tno)
                cur.execute(sql)
                data1 = cur.fetchall()
                if data1 is not None:
                    for item in data1:
                        mno_list.append(item[0])
                sql = 'SELECT GuestMatchNo FROM final.guestmatch WHERE `GuestTeamNo`=\'{}\';'.format(tno)
                cur.execute(sql)
                data2 = cur.fetchall()
                if data2 is not None:
                    for item in data2:
                        mno_list.append(item[0])
                out = ''
                if len(data1) > 0 or len(data2) > 0:
                    print('if')
                    if mno_list is not None:
                        mno_list.sort()
                        for mno in mno_list:
                            text = self.search(mno)
                            out += text
                        # res = QMessageBox.information(self, '结果', out, QMessageBox.Yes, QMessageBox.Yes)
                        # print(res)
                    else:
                        out = '该队无比赛信息\n'
                        # print(QMessageBox.information(self, '结果', '该队无比赛信息', QMessageBox.Yes, QMessageBox.Yes))
                else:
                    out = '该队无任何比赛信息\n'
                    # print(QMessageBox.information(self, '结果', '该队无任何比赛信息', QMessageBox.Yes, QMessageBox.Yes))
                sql = 'SELECT `Statistic`,`NetScore`,`TName` FROM final.team WHERE `TNO`=\'{}\';'.format(tno)
                cur.execute(sql)
                data = cur.fetchall()[0]
                cur.close()
                stat = data[0]
                net = data[1]
                name = data[2]
                win = int(stat[1:3])
                lose = int(stat[5:7])
                info = '\n球队编号：{}\n球队名称：{}\n球队战绩：胜{}——负{}\n净胜分：{}\n'.format(tno, name, win, lose, net)
                out += info
                print(QMessageBox.information(self, '结果', out), QMessageBox.Yes, QMessageBox.Yes)


class RegisWindow(QMainWindow, Regis_Form):
    return_login = pyqtSignal()

    def __init__(self):
        super(RegisWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('注册')
        self.set_callbacks()
        self.comboBox.addItems(['男', '女'])
        self.comboBox.currentIndexChanged[str].connect(self.print_value)
        self.comboBox.highlighted[str].connect(self.print_value)

    def print_value(self, i):
        print(i)

    def set_callbacks(self):
        self.pushButton.clicked.connect(self.Regis)
        self.pushButton_2.clicked.connect(self.GoLogin)

    def GoLogin(self):
        self.return_login.emit()

    def Regis(self):
        account = self.lineEdit.text()
        passwd = self.lineEdit_2.text()
        passwd_1 = self.lineEdit_3.text()
        name = self.lineEdit_4.text()
        gender = self.comboBox.currentText()
        age = self.lineEdit_5.text()
        print('account:{}\npasswd: {}\npasswd_1: {}\nname: {}'.format(account, passwd, passwd_1, name))
        if account == '' or passwd == '' or passwd_1 == '':
            print(QMessageBox.warning(self, '警告', '不可为空', QMessageBox.Yes, QMessageBox.Yes))
        else:
            conn = get_conn()
            cur = conn.cursor()
            if passwd != passwd_1:
                print(QMessageBox.warning(self, '警告', '两次密码不同', QMessageBox.Yes, QMessageBox.Yes))
            else:
                sql = 'SELECT account FROM Final.user;'  # ########### Change applied Final.
                cur.execute(sql)
                data = cur.fetchall()
                account_list = []
                for item in data:
                    account_list.append(item[0])
                print(account in account_list)
                if account in account_list:
                    print(QMessageBox.warning(self, '警告', '账号已存在', QMessageBox.Yes, QMessageBox.Yes))
                else:
                    sql = 'INSERT INTO user (`Account`, `password`, `Name`, `State`, `Sex`, `Age`) VALUES (\'{}\',' \
                          '\'{}\',\'{}\',{},\'{}\',\'{}\')'.format(account, passwd, name, 0, gender, age)
                    print(sql)
                    cur.execute(sql)
                    conn.commit()
                    sql = 'INSERT INTO audience (`Account`) VALUES (\'{}\')'.format(account)
                    print(sql)
                    cur.execute(sql)
                    conn.commit()
                    print(cur.fetchall())
                    cur.close()
                    print(QMessageBox.information(self, '提示', '注册成功', QMessageBox.Yes, QMessageBox.Yes))
        return


class ShopWindow(QMainWindow, Shop_Form):
    return_home0 = pyqtSignal()
    show_history = pyqtSignal()

    def __init__(self, acc):
        super(ShopWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('购物')
        self.set_callbacks()
        self.tableWidget.setHorizontalHeaderLabels(['商品编号', '商品名称', '商品库存', '商品单价'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_2.setHorizontalHeaderLabels(['商品编号', '商品名称', '购买数量', '金额小计'])
        self.tableWidget_2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_2.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.info = self.get_rows()
        self.add_rows()
        self.show_data()
        self.selected = 0
        self.sum = 0
        self.account = acc

    def set_callbacks(self):
        self.pushButton.clicked.connect(self.show_data)
        self.pushButton_2.clicked.connect(self.add_cart)
        self.pushButton_3.clicked.connect(self.buy)
        self.pushButton_4.clicked.connect(self.clear_all)
        self.pushButton_5.clicked.connect(self.clear)
        self.pushButton_6.clicked.connect(self.history)
        self.tableWidget.cellPressed.connect(self.get_pos)
        self.tableWidget_2.cellPressed.connect(self.get_pos_2)
        self.pushButton_7.clicked.connect(self.GoHome0)

    def GoHome0(self):
        self.return_home0.emit()

    def get_pos(self):
        try:
            row = self.tableWidget.selectedItems()[0].row()
            return row
        except:
            return

    def get_pos_2(self):
        try:
            row = self.tableWidget_2.selectedItems()[0].row()
            return row
        except:
            return

    def get_rows(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = 'SELECT * FROM final.item;'
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        info_list = []
        for item in data:
            info_list.append(item)
        return info_list

    def add_rows(self):
        info = self.get_rows()
        n_row = len(info)
        if n_row > 1:
            for i in range(1, n_row):
                self.tableWidget.insertRow(i)

    def show_data(self):
        info = self.get_rows()
        n_row = len(info)
        print(info)
        for i in range(n_row):
            data = info[i]
            for j in range(4):
                item = QTableWidgetItem(str(data[j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, j, item)
        return info

    def add_cart(self):
        info = self.info
        row = self.get_pos()
        if row is None:
            print(QMessageBox.warning(self, '错误', '未选择商品', QMessageBox.Yes, QMessageBox.Yes))
        else:
            dialog = QInputDialog()
            num, ok = dialog.getInt(self, '商品购买', '请输入购买数量：')
            num = int(num)
            sto = int(info[row][2])
            if num <= 0:
                print(QMessageBox.warning(self, '错误', '购买数量有误', QMessageBox.Yes, QMessageBox.Yes))
            elif sto < num:
                print(QMessageBox.warning(self, '错误', '库存不足', QMessageBox.Yes, QMessageBox.Yes))
            else:
                print(QMessageBox.information(self, '提示', '添加购物车成功', QMessageBox.Yes, QMessageBox.Yes))
                data = info[row]
                sum = '%.02f' % (num * int(data[3]))
                add = [data[0], data[1], num, sum]
                self.selected += 1
                print(add)
                n_row = self.tableWidget_2.rowCount()
                if n_row < self.selected:  # 最多少1行
                    self.tableWidget_2.insertRow(n_row)
                ind = self.selected - 1
                for j in range(4):
                    item = QTableWidgetItem(str(add[j]))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tableWidget_2.setItem(ind, j, item)
                self.sum += num * int(data[3])
                sum = '%.02f' % self.sum
                self.label_3.setText('合计金额：{}'.format(sum))
                sto -= num
                sql = 'UPDATE final.item SET `Storage`=\'{}\' WHERE `INo`=\'{}\';'.format(sto, add[0])
                conn = get_conn()
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()
                cur.close()
                self.info = self.get_rows()
                self.show_data()

    def buy(self):
        #  创建ItemOrder
        conn = get_conn()
        cur = conn.cursor()
        sql = 'SELECT * FROM final.itemdeal;'
        cur.execute(sql)
        n = len(cur.fetchall()) + 1
        n = '%02d' % n
        idno = 'ID{}'.format(n)
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        sum = self.sum
        acc = self.account
        sql = 'INSERT INTO final.itemdeal (`IDNo`,`Date`,`Sum`,`Account`) VALUES (\'{}\',\'{}\',{},\'{}\');'.format(idno, date, sum, acc)
        cur.execute(sql)
        conn.commit()
        print(QMessageBox.information(self, '提示', '购买成功', QMessageBox.Yes, QMessageBox.Yes))
        n_row = self.tableWidget_2.rowCount()
        info = []
        for i in range(n_row):
            sub_list = []
            for j in range(0, 4):
                sub_list.append(self.tableWidget_2.item(0, j).text())
            info.append(sub_list)
            self.tableWidget_2.removeRow(0)
        print(info)
        for i in range(len(info)):
            data = info[i]
            ino = data[0]
            quant = int(data[2])
            sum = float(data[3])
            sql = 'INSERT INTO final.itemsale (`INo`,`IDNo`,`Quantity`,`Sum`) VALUES (\'{}\',\'{}\',{},{});'.format(ino, idno, quant, sum)
            cur.execute(sql)
            conn.commit()
        cur.close()
        self.tableWidget_2.insertRow(0)
        self.info = self.get_rows()
        self.show_data()
        self.sum = 0
        self.selected = 0
        self.label_3.setText('合计金额：0.00'.format(sum))

    def clear_all(self):
        n_row = self.tableWidget_2.rowCount()
        for i in range(n_row):
            info = []
            for j in range(0, 4):
                info.append(self.tableWidget_2.item(0, j).text())
            print(info)
            ino = info[0]
            num = int(info[2])
            sum = float(info[3])
            self.selected -= 1
            self.sum -= sum
            sum = '%.02f' % self.sum
            self.label_3.setText('合计金额：{}'.format(sum))
            conn = get_conn()
            cur = conn.cursor()
            sql = 'SELECT Storage FROM final.item WHERE `INo`=\'{}\';'.format(ino)
            cur.execute(sql)
            sto = cur.fetchall()[0][0]
            sto += num
            sql = 'UPDATE final.item SET `Storage`=\'{}\' WHERE `INo`=\'{}\';'.format(sto, ino)
            cur.execute(sql)
            conn.commit()
            cur.close()
            self.tableWidget_2.removeRow(0)
        self.tableWidget_2.insertRow(0)
        self.info = self.get_rows()
        self.show_data()
        self.sum = 0
        self.selected = 0
        self.label_3.setText('合计金额：0.00'.format(sum))

    def clear(self):
        row = self.get_pos_2()
        if row is None:
            print(QMessageBox.warning(self, '错误', '未选择商品', QMessageBox.Yes, QMessageBox.Yes))
        else:
            res = QMessageBox.information(self, '确认', '是否删除选定商品？', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if res == 16384:
                info = []
                for j in range(0, 4):
                    info.append(self.tableWidget_2.item(row, j).text())
                ino = info[0]
                num = int(info[2])
                sum = float(info[3])
                self.selected -= 1
                self.sum -= sum
                sum = '%.02f' % self.sum
                self.label_3.setText('合计金额：{}'.format(sum))
                conn = get_conn()
                cur = conn.cursor()
                sql = 'SELECT Storage FROM final.item WHERE `INo`=\'{}\';'.format(ino)
                cur.execute(sql)
                sto = cur.fetchall()[0][0]
                sto += num
                sql = 'UPDATE final.item SET `Storage`=\'{}\' WHERE `INo`=\'{}\';'.format(sto, ino)
                cur.execute(sql)
                conn.commit()
                cur.close()
                self.info = self.get_rows()
                self.show_data()
                self.tableWidget_2.removeRow(row)
                if self.tableWidget_2.rowCount() == 0:
                    self.tableWidget_2.insertRow(0)
                print(QMessageBox.information(self, '提示', '商品删除成功', QMessageBox.Yes, QMessageBox.Yes))

    def history(self):
        self.show_history.emit()


class TCWindow(QMainWindow, TC_Form):
    return_home0 = pyqtSignal()
    show_history = pyqtSignal()

    def __init__(self, acc):
        super(TCWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('更换比赛时间申请')
        self.set_callbacks()
        self.account = acc

    def set_callbacks(self):
        self.pushButton.clicked.connect(self.TC)
        self.pushButton_2.clicked.connect(self.GoHome0)
        self.pushButton_3.clicked.connect(self.history)

    def GoHome0(self):
        self.return_home0.emit()

    def TC(self):
        mno = self.lineEdit.text()
        new_time = self.lineEdit_2.text()
        if mno == '' or new_time == '':
            print(QMessageBox.warning(self, '错误', '不可为空', QMessageBox.Yes, QMessageBox.Yes))
        else:
            conn = get_conn()
            cur = conn.cursor()
            sql = 'SELECT State FROM final.match WHERE `MNo`=\'{}\';'.format(mno)
            cur.execute(sql)
            state = cur.fetchall()[0][0]
            sql = 'SELECT Time FROM final.match WHERE `MNo`=\'{}\';'.format(mno)
            cur.execute(sql)
            old_time = cur.fetchall()[0][0]
            if len(new_time) != 17:
                print(QMessageBox.warning(self, '错误', '时间输入有误', QMessageBox.Yes, QMessageBox.Yes))
            elif state == 1:
                print(QMessageBox.warning(self, '错误', '比赛已结束', QMessageBox.Yes, QMessageBox.Yes))
            elif old_time == new_time:
                print(QMessageBox.warning(self, '错误', '新时间与原时间相同', QMessageBox.Yes, QMessageBox.Yes))
            else:
                sql = 'SELECT HomeTeamNo FROM final.homematch WHERE `HomeMatchNo`=\'{}\';'.format(mno)
                cur.execute(sql)
                h_tno = cur.fetchall()[0][0]
                sql = 'SELECT GuestTeamNo FROM final.guestmatch WHERE `GuestMatchNo`=\'{}\';'.format(mno)
                cur.execute(sql)
                g_tno = cur.fetchall()[0][0]
                sql = 'SELECT Team FROM final.teamleader WHERE `Account`=\'{}\';'.format(self.account)
                cur.execute(sql)
                tno = cur.fetchall()[0][0]
                if tno != h_tno and tno != g_tno:
                    print(QMessageBox.warning(self, '错误', '没有权限申请更改其它比赛时间', QMessageBox.Yes, QMessageBox.Yes))
                else:
                    sql = 'SELECT `MNo`,`TeamAccount` FROM final.timerequest;'
                    cur.execute(sql)
                    data = cur.fetchall()
                    print(data)
                    tup = tuple([mno, self.account])
                    print(tup)
                    if tup in data:
                        print(QMessageBox.warning(self, '错误', '已经申请更改本场比赛时间', QMessageBox.Yes, QMessageBox.Yes))
                    else:
                        sql = 'INSERT INTO final.timerequest (`MNo`,`TeamAccount`,`NewTime`,`State`) VALUES (\'{}\',' \
                              '\'{}\',\'{}\',0);'.format(mno, self.account, new_time)
                        cur.execute(sql)
                        conn.commit()
                        print(QMessageBox.information(self, '提示', '申请提交成功', QMessageBox.Yes, QMessageBox.Yes))
                        cur.close()

    def history(self):
        self.show_history.emit()


class THWindow(QMainWindow, TH_Form):
    return_TC = pyqtSignal()

    def __init__(self, acc):
        super(THWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('查看比赛时间更改申请历史记录')
        self.tableWidget.setHorizontalHeaderLabels(['比赛编号', '新时间', '审批状态'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        for i in range(3):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Interactive)
        self.set_callbacks()
        self.account = acc
        self.info = self.get_rows()
        print(self.info)
        self.add_rows()
        self.show_data()

    def set_callbacks(self):
        self.pushButton.clicked.connect(self.GoTC)

    def GoTC(self):
        self.return_TC.emit()

    def get_rows(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = 'SELECT * FROM final.timerequest;'
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        info_list = []
        for item in data:
            if item[1] == self.account:
                info_list.append(item)
        return info_list

    def get_pos(self):
        try:
            row = self.tableWidget.selectedItems()[0].row()
            return row
        except:
            return

    def add_rows(self):
        info = self.get_rows()
        n_row = len(info)
        if n_row > 1:
            for i in range(1, n_row):
                self.tableWidget.insertRow(i)

    def show_data(self):
        info_list = self.get_rows()
        n_row = len(info_list)
        print(info_list)
        flag = False
        for i in range(n_row):
            info = info_list[i]
            state = info[3]
            if state == 0:
                state = '未审批'
            elif state == 1:
                state = '通过'
            elif state == 2:
                state = '不通过'
            data = [info[0], info[2], state]
            for j in range(3):
                item = QTableWidgetItem(str(data[j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, j, item)
            if len(info[2]) >= 10:
                flag = True
                self.tableWidget.resizeColumnToContents(1)
        if not flag:
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        return info_list


class TJWindow(QMainWindow, TJ_Form):
    return_home2 = pyqtSignal()

    def __init__(self):
        super(TJWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle('比赛时间更换审批')
        self.set_callbacks()
        for i in range(6):
            self.tableWidget.horizontalHeader().setSectionResizeMode(i, QHeaderView.Interactive)
        self.info = self.get_rows()
        self.add_rows()
        self.info_list = self.show_data()

    def set_callbacks(self):
        self.tableWidget.setHorizontalHeaderLabels(['比赛编号', '申请球队账号', '申请球队名称', '新时间', '申请状态', '选择'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.pushButton.clicked.connect(self.GoHome2)

    def GoHome2(self):
        self.return_home2.emit()

    def add_buttons(self):
        n_row = self.tableWidget.rowCount()
        for i in range(n_row):
            self.tableWidget.setCellWidget(i, self.tableWidget.columnCount() - 1, self.buttonForRow())

    def buttonForRow(self):
        widget = QWidget()
        self.updateBtn = QtWidgets.QPushButton('审批')
        self.updateBtn.setStyleSheet(''' text-align : center;
                                                  background-color : NavajoWhite;
                                                  height : 25px;
                                                  border-style: outset;
                                                  font : 13px  ''')
        self.updateBtn.clicked.connect(self.TJ)
        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(self.updateBtn)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget

    def add_rows(self):
        n_row = len(self.info)
        if n_row > 1:
            for i in range(1, n_row):
                self.tableWidget.insertRow(i)
        self.add_buttons()

    def get_rows(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = 'SELECT * FROM final.timerequest;'
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        info_list = []
        for item in data:
            info_list.append((item[0], item[1]))
        return info_list

    def show_data(self):
        n_row = len(self.info)
        conn = get_conn()
        cur = conn.cursor()
        sql = 'SELECT * FROM final.timerequest;'
        cur.execute(sql)
        data = cur.fetchall()
        info_list = []
        acc_list = []
        state_list = []
        for item in data:
            sub_list = []
            for num in item:
                sub_list.append(num)
            acc_list.append(item[1])
            state_list.append(item[3])
            info_list.append(sub_list)
        i = 0
        for acc in acc_list:
            sql = 'SELECT Team FROM final.teamleader WHERE `Account`=\'{}\';'.format(acc)
            cur.execute(sql)
            tno = cur.fetchall()[0][0]
            sql = 'SELECT TName FROM final.team WHERE `TNo`=\'{}\';'.format(tno)
            cur.execute(sql)
            t_name = cur.fetchall()[0][0]
            info_list[i].insert(2, t_name)
            if state_list[i] == 0:
                info_list[i][4] = '未审批'
            elif state_list[i] == 1:
                info_list[i][4] = '通过'
            elif state_list[i] == 2:
                info_list[i][4] = '不通过'
            i += 1
        print(info_list)
        for i in range(n_row):
            data = info_list[i]
            for j in range(0, 5):
                item = QTableWidgetItem(data[j])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, j, item)
        cur.close()
        self.tableWidget.resizeColumnToContents(3)
        return info_list

    def TJ(self):
        button = self.sender()
        info = self.info_list
        if button:
            row = self.tableWidget.indexAt(button.parent().pos()).row()
            state = 0
            reply = QMessageBox.information(self, '审批', '是否通过？', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == 16384:
                state = 1
                print(QMessageBox.information(None, '操作完成', '审批通过！', QMessageBox.Yes, QMessageBox.Yes))
            elif reply == 65536:
                state = 2
                print(QMessageBox.information(None, '操作完成', '审批不通过！', QMessageBox.Yes, QMessageBox.Yes))
            mno = info[row][0]
            acc = info[row][1]
            conn = get_conn()
            cur = conn.cursor()
            sql = 'UPDATE final.timerequest SET `State`={} WHERE `MNo`=\'{}\' AND `TeamAccount`=\'{}\';'.format(state, mno, acc)
            cur.execute(sql)
            conn.commit()
            cur.close()
            self.change_time(mno, info[row][3])
            self.info_list = self.show_data()

    def change_time(self, mno, new_time):
        conn = get_conn()
        cur = conn.cursor()
        sql = 'UPDATE final.match SET `Time`=\'{}\' WHERE `MNo`=\'{}\';'.format(new_time, mno)
        cur.execute(sql)
        conn.commit()
        cur.close()


class VIWindow(QMainWindow, VI_Form):
    return_home2 = pyqtSignal()

    def __init__(self):
        super(VIWindow, self).__init__()
        self.setupUi(self)
        self.set_callbacks()
        self.setWindowTitle('商品信息查看')
        self.info = self.get_rows()
        self.add_rows()
        self.show_data()

    def set_callbacks(self):
        self.tableWidget.setHorizontalHeaderLabels(['商品编号', '商品名称', '商品库存', '商品单价', '更改'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.pushButton.clicked.connect(self.GoHome2)

    def GoHome2(self):
        self.return_home2.emit()

    def add_buttons(self):
        n_row = self.tableWidget.rowCount()
        for i in range(n_row):
            self.tableWidget.setCellWidget(i, self.tableWidget.columnCount() - 1, self.buttonForRow())

    def buttonForRow(self):
        widget = QWidget()
        self.storageBtn = QtWidgets.QPushButton('库存')
        self.storageBtn.setStyleSheet(''' text-align : center;
                                                  background-color : NavajoWhite;
                                                  height : 25px;
                                                  border-style: outset;
                                                  font : 13px  ''')
        self.storageBtn.clicked.connect(self.storage)
        self.priceBtn = QtWidgets.QPushButton('单价')
        self.priceBtn.setStyleSheet(''' text-align : center;
                                    background-color : LightCoral;
                                    height : 30px;
                                    border-style: outset;
                                    font : 13px; ''')
        self.priceBtn.clicked.connect(self.price)
        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(self.storageBtn)
        hLayout.addWidget(self.priceBtn)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget

    def get_rows(self):
        conn = get_conn()
        cur = conn.cursor()
        sql = 'SELECT * FROM final.item;'
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        info_list = []
        for item in data:
            info_list.append(item)
        return info_list

    def add_rows(self):
        n_row = len(self.info)
        if n_row > 1:
            for i in range(1, n_row):
                self.tableWidget.insertRow(i)
        self.add_buttons()

    def show_data(self):
        info = self.get_rows()
        n_row = len(info)
        print(info)
        for i in range(n_row):
            data = info[i]
            for j in range(4):
                item = QTableWidgetItem(str(data[j]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tableWidget.setItem(i, j, item)
        return info

    def storage(self):
        button = self.sender()
        info = self.info
        if button:
            row = self.tableWidget.indexAt(button.parent().pos()).row()
            dialog = QInputDialog()
            sto, ok = dialog.getInt(self, '库存更改', '请输入商品库存：')
            sto = int(sto)
            print(QMessageBox.information(self, '提示', '库存更改成功', QMessageBox.Yes, QMessageBox.Yes))
            conn = get_conn()
            cur = conn.cursor()
            ino = info[row][0]
            sql = 'UPDATE final.item SET `Storage`=\'{}\' WHERE `INo`=\'{}\';'.format(sto, ino)
            cur.execute(sql)
            conn.commit()
            cur.close()
            self.info = self.show_data()

    def price(self):
        button = self.sender()
        info = self.info
        if button:
            row = self.tableWidget.indexAt(button.parent().pos()).row()
            dialog = QInputDialog()
            price, ok = dialog.getInt(self, '单价更改', '请输入商品单价：')
            price = int(price)
            print(QMessageBox.information(self, '提示', '单价更改成功', QMessageBox.Yes, QMessageBox.Yes))
            conn = get_conn()
            cur = conn.cursor()
            ino = info[row][0]
            sql = 'UPDATE final.item SET `Price`=\'{}\' WHERE `INo`=\'{}\';'.format(price, ino)
            cur.execute(sql)
            conn.commit()
            cur.close()
            self.info = self.show_data()
