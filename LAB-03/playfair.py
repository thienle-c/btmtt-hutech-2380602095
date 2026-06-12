import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from ui.playfair import Ui_MainWindow  # Import giao diện Playfair mới tạo ở trên

class PlayfairApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Playfair Cipher - Lê Minh Thiên - 2380602095")
        
        # Kết nối sự kiện Click Button
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    def display_matrix(self, matrix_data):
        """Hàm hỗ trợ đổ ma trận ký tự vào QTableWidget phẳng và đẹp mắt"""
        if not matrix_data:
            return
        
        self.ui.table_matrix.clearContents()
        for row_idx, row in enumerate(matrix_data):
            for col_idx, char in enumerate(row):
                item = QTableWidgetItem(str(char))
                # Căn giữa ký tự trong ô ma trận
                item.setTextAlignment(Qt.AlignCenter)
                # Chỉnh chữ in đậm nhìn cho rõ ràng
                font = QFont()
                font.setBold(True)
                item.setFont(font)
                
                self.ui.table_matrix.setItem(row_idx, col_idx, item)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/encrypt" # Đảm bảo cổng 5000
        raw_key = self.ui.txt_key.toPlainText().strip()
        plain_text = self.ui.txt_plain_text.toPlainText()

        if not raw_key.isdigit():
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Số tầng đường ray (Rails) phải là một số nguyên dương!")
            return
            
        num_rails = int(raw_key)
        payload = {
            "inputPlainText": plain_text,
            "inputKeyPlain": num_rails
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                res_data = response.json()
                if res_data.get("status") == "success":
                    self.ui.txt_cipher_text.setPlainText(res_data["result"])
                    
                    # SỬA TẠI ĐÂY: Lọc chuỗi ngay trên UI trước khi gọi hàm vẽ zig-zag
                    clean_text_ui = "".join(c for c in plain_text if c.isalpha())
                    self.display_rail_fence(clean_text_ui, num_rails)
                    
                    QMessageBox.information(self, "Thành công", "Mã hóa Rail Fence thành công!")
                else:
                    QMessageBox.critical(self, "Lỗi Ràng Buộc", res_data.get("message"))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Kết Nối", f"Không thể kết nối API: {str(e)}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/decrypt" # Đảm bảo cổng 5000
        raw_key = self.ui.txt_key.toPlainText().strip()
        cipher_text = self.ui.txt_cipher_text.toPlainText()

        if not raw_key.isdigit():
            QMessageBox.warning(self, "Lỗi Nhập Liệu", "Số tầng đường ray (Rails) phải là một số nguyên dương!")
            return
            
        num_rails = int(raw_key)
        payload = {
            "inputCipherText": cipher_text,
            "inputKeyCipher": num_rails
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                res_data = response.json()
                if res_data.get("status") == "success":
                    self.ui.txt_plain_text.setPlainText(res_data["result"])
                    
                    # SỬA TẠI ĐÂY: Khi giải mã thành công, chuỗi kết quả res_data["result"] vốn đã sạch chữ cái rồi
                    self.display_rail_fence(res_data["result"], num_rails)
                    
                    QMessageBox.information(self, "Thành công", "Giải mã Rail Fence thành công!")
                else:
                    QMessageBox.critical(self, "Lỗi Ràng Buộc", res_data.get("message"))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Kết Nối", f"Không thể kết nối API: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlayfairApp()
    window.show()
    sys.exit(app.exec_())