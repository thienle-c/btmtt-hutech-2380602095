import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Import giao diện Vigenere đã thiết kế từ thư mục ui
from ui.vigenere import Ui_MainWindow  

class VigenereApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Vigenère Cipher - Lê Minh Thiên - 2380602095")
        
        # Kết nối sự kiện Click của 2 nút bấm trên giao diện
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    # =========================================================================
    # VỊ TRÍ ĐẶT HÀM: Phương thức hiển thị dòng khóa tương ứng (Key Stream Mapping)
    # =========================================================================
    def display_vigenere_mapping(self, text, key):
        """Trải phẳng Text và dòng Key lặp tương ứng lên QTableWidget mẫu minh họa"""
        if not text or not key:
            return
            
        # Chuẩn hóa nhanh để hiển thị in hoa cho đẹp đồng bộ mã hóa
        clean_text = "".join(c.upper() for c in text if c.isalpha())
        clean_key = "".join(c.upper() for c in key if c.isalpha())
        
        if not clean_text or not clean_key:
            return

        # Tạo chuỗi KeyStream lặp lại liên tục cho bằng chiều dài văn bản rõ
        key_stream = ""
        key_index = 0
        for char in clean_text:
            key_stream += clean_key[key_index % len(clean_key)]
            key_index += 1

        # Cấu hình số cột dựa vào chiều dài chuỗi chữ cái (giới hạn tối đa 20 ký tự để không bị tràn bảng)
        display_length = min(len(clean_text), 20)
        
        self.ui.table_matrix.setRowCount(2)
        self.ui.table_matrix.setColumnCount(display_length)
        self.ui.table_matrix.clear()
        
        # Đặt lại nhãn tiêu đề dòng
        self.ui.table_matrix.setVerticalHeaderLabels(["Text", "Key"])
        
        # Đặt chiều rộng mỗi ô nhỏ gọn vừa khít 1 chữ cái
        self.ui.table_matrix.horizontalHeader().setDefaultSectionSize(35)
        self.ui.table_matrix.verticalHeader().setDefaultSectionSize(40)

        # Đổ dữ liệu chữ cái vào bảng
        font = QFont()
        font.setBold(True)
        
        for col in range(display_length):
            # 1. Hàng 0: Ký tự bản rõ/bản mã
            item_text = QTableWidgetItem(clean_text[col])
            item_text.setTextAlignment(Qt.AlignCenter)
            item_text.setFont(font)
            self.ui.table_matrix.setItem(0, col, item_text)
            
            # 2. Hàng 1: Ký tự khóa tương ứng tại cột đó
            item_key = QTableWidgetItem(key_stream[col])
            item_key.setTextAlignment(Qt.AlignCenter)
            item_key.setFont(font)
            # Bạn có thể đổi màu sắc chữ của dòng Key để tạo điểm nhấn trực quan
            item_key.setForeground(Qt.blue) 
            self.ui.table_matrix.setItem(1, col, item_key)

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/vigenere/encrypt"
        
        plain_text = self.ui.txt_plain_text.toPlainText()
        key = self.ui.txt_key.toPlainText()
        
        payload = {
            "inputPlainText": plain_text,
            "inputKeyPlain": key
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                res_data = response.json()
                if res_data.get("status") == "success":
                    # Đổ kết quả bản mã ra ô Ciphertext
                    self.ui.txt_cipher_text.setPlainText(res_data["result"])
                    
                    # KÍCH HOẠT VẼ: Vẽ sự tương ứng giữa Bản rõ và Chuỗi khóa lặp
                    self.display_vigenere_mapping(plain_text, key)
                    
                    QMessageBox.information(self, "Thành công", "Mã hóa Vigenère thành công!")
                else:
                    QMessageBox.critical(self, "Lỗi Ràng Buộc", res_data.get("message"))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Kết Nối", f"Không thể kết nối API: {str(e)}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/vigenere/decrypt"
        
        cipher_text = self.ui.txt_cipher_text.toPlainText()
        key = self.ui.txt_key.toPlainText()
        
        payload = {
            "inputCipherText": cipher_text,
            "inputKeyCipher": key
        }
        
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                res_data = response.json()
                if res_data.get("status") == "success":
                    # Đổ kết quả bản rõ phục hồi
                    self.ui.txt_plain_text.setPlainText(res_data["result"])
                    
                    # KÍCH HOẠT VẼ: Khi giải mã, ta dùng chuỗi kết quả (Bản rõ vừa giải mã) đối sánh với Key
                    self.display_vigenere_mapping(res_data["result"], key)
                    
                    QMessageBox.information(self, "Thành công", "Giải mã Vigenère thành công!")
                else:
                    QMessageBox.critical(self, "Lỗi Ràng Buộc", res_data.get("message"))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Kết Nối", f"Không thể kết nối API: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VigenereApp()
    window.show()
    sys.exit(app.exec_())