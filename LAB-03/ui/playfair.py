# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/playfair.ui'
# Updated manually for Playfair Cipher Matrix display support.

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # 1. TIÊU ĐỀ CHÍNH (Đổi thành PLAYFAIR CIPHER)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 10, 750, 71))
        self.label.setScaledContents(False)
        self.label.setObjectName("label")
        
        # 2. KHU VỰC NHẬP LIỆU BÊN TRÁI (Thu hẹp chiều rộng từ 521 xuống 350 để chừa chỗ cho Ma trận)
        self.txt_plain_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_plain_text.setGeometry(QtCore.QRect(120, 110, 350, 80))
        self.txt_plain_text.setObjectName("txt_plain_text")
        
        self.txt_key = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_key.setGeometry(QtCore.QRect(120, 210, 350, 60))
        self.txt_key.setObjectName("txt_key")
        
        self.txt_cipher_text = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.txt_cipher_text.setGeometry(QtCore.QRect(120, 290, 350, 80))
        self.txt_cipher_text.setObjectName("txt_cipher_text")
        
        # LABELS CHO CÁC Ô NHẬP LIỆU
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 110, 71, 16))
        self.label_2.setObjectName("label_2")
        
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 210, 61, 16))
        self.label_3.setObjectName("label_3")
        
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 290, 71, 16))
        self.label_4.setObjectName("label_4")
        
        # 3. MA TRẬN PLAYFAIR 5x5 (Thêm mới bên phải giao diện)
        self.label_matrix = QtWidgets.QLabel(self.centralwidget)
        self.label_matrix.setGeometry(QtCore.QRect(500, 90, 150, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_matrix.setFont(font)
        self.label_matrix.setObjectName("label_matrix")
        
        self.table_matrix = QtWidgets.QTableWidget(self.centralwidget)
        self.table_matrix.setGeometry(QtCore.QRect(500, 110, 262, 260))
        self.table_matrix.setRowCount(5)
        self.table_matrix.setColumnCount(5)
        self.table_matrix.setObjectName("table_matrix")
        
        # Cấu hình cho bảng ma trận hiển thị đẹp, đều ô
        self.table_matrix.horizontalHeader().setVisible(False)
        self.table_matrix.verticalHeader().setVisible(False)
        self.table_matrix.horizontalHeader().setDefaultSectionSize(50)
        self.table_matrix.verticalHeader().setDefaultSectionSize(50)
        self.table_matrix.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers) # Chỉ xem, không cho sửa đè
        
        # 4. HỆ THỐNG PHÍM BẤM
        self.btn_encrypt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_encrypt.setGeometry(QtCore.QRect(140, 410, 120, 35))
        self.btn_encrypt.setObjectName("btn_encrypt")
        
        self.btn_decrypt = QtWidgets.QPushButton(self.centralwidget)
        self.btn_decrypt.setGeometry(QtCore.QRect(330, 410, 120, 35))
        self.btn_decrypt.setObjectName("btn_decrypt")
        
        # 5. THÔNG TIN CÁ NHÂN (Giữ vững thương hiệu Lê Minh Thiên)
        self.label_student_info = QtWidgets.QLabel(self.centralwidget)
        self.label_student_info.setGeometry(QtCore.QRect(30, 510, 450, 30))
        self.label_student_info.setObjectName("label_student_info")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Playfair Cipher - Đồ án"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:42pt; font-weight:600; color:#2c3e50;\">PLAYFAIR CIPHER</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "Plain Text:"))
        self.label_3.setText(_translate("MainWindow", "Key Matrix:"))
        self.label_4.setText(_translate("MainWindow", "Ciphertext:"))
        self.label_matrix.setText(_translate("MainWindow", "Playfair Matrix (5x5):"))
        self.btn_encrypt.setText(_translate("MainWindow", "Encrypt"))
        self.btn_decrypt.setText(_translate("MainWindow", "Decrypt"))
        self.label_student_info.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600; color:#c0392b;\">Sinh viên: Lê Minh Thiên - MSSV: 2380602095</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())