import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.caesar import Ui_MainWindow 

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Đảm bảo hiển thị tên của bạn ngay trên title bar để định danh đồ án
        self.setWindowTitle("Đồ án Mật Mã Cổ Điển - Lê Minh Thiên - 2380602095")
        
        # Kết nối sự kiện Click Button
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def call_api_encrypt(self):
        # Sử dụng port 5000 theo file Flask hiện tại của bạn
        url = "http://127.0.0.1:5000/api/caesar/encrypt"
        
        payload = {
            "inputPlainText": self.ui.txt_plain_text.toPlainText(),
            "inputKeyPlain": self.ui.txt_key.toPlainText()
        }
        
        try:
            # Sửa đổi quan trọng: dùng json=payload để Flask đọc được bằng request.json
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                res_data = response.json()
                
                if res_data.get("status") == "success":
                    self.ui.txt_cipher_text.setPlainText(res_data["result"])
                    
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("Thành công")
                    msg.setText("Mã hóa thành công dữ liệu!")
                    msg.exec_()
                else:
                    QMessageBox.critical(self, "Lỗi Ràng Buộc", res_data.get("message"))
            else:
                QMessageBox.warning(self, "Lỗi Hệ Thống", "Không thể kết nối đến máy chủ API hoặc Endpoint sai.")
                
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi Kết Nối", f"Không thể kết nối API:\n{str(e)}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/caesar/decrypt"
        
        payload = {
            "inputCipherText": self.ui.txt_cipher_text.toPlainText(),
            "inputKeyCipher": self.ui.txt_key.toPlainText()
        }
        
        try:
            # Sửa đổi quan trọng: dùng json=payload
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                res_data = response.json()
                
                if res_data.get("status") == "success":
                    self.ui.txt_plain_text.setPlainText(res_data["result"])
                    
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setWindowTitle("Thành công")
                    msg.setText("Giải mã dữ liệu thành công!")
                    msg.exec_()
                else:
                    QMessageBox.critical(self, "Lỗi Ràng Buộc", res_data.get("message"))
            else:
                QMessageBox.warning(self, "Lỗi Hệ Thống", "Không thể kết nối đến máy chủ API hoặc Endpoint sai.")
                
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Lỗi Kết Nối", f"Không thể kết nối API:\n{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())