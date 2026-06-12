import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Import giao diện Rail Fence đã thiết kế từ thư mục ui
from ui.railfence import Ui_MainWindow  

class RailFenceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Rail Fence Cipher - Lê Minh Thiên - 2380602095")
        
        # Kết nối sự kiện Click của 2 nút bấm trên giao diện
        self.ui.btn_encrypt.clicked.connect(self.call_api_encrypt)
        self.ui.btn_decrypt.clicked.connect(self.call_api_decrypt)

    # =========================================================================
    # VỊ TRÍ ĐẶT HÀM: Đặt làm một phương thức (method) bên trong Class như thế này
    # =========================================================================
    def display_rail_fence(self, text, num_rails):
        """Mô phỏng đường đi răng cưa Zig-zag của các ký tự lên QTableWidget"""
        if not text or num_rails <= 1:
            return
            
        # Thiết lập số hàng cố định bằng số rails, số cột bằng chiều dài chuỗi text
        self.ui.table_matrix.setRowCount(num_rails)
        self.ui.table_matrix.setColumnCount(len(text))
        self.ui.table_matrix.clear()
        
        # Đặt tiêu đề hàng cho dễ nhìn (R 1, R 2...)
        self.ui.table_matrix.setVerticalHeaderLabels([f"R {i+1}" for i in range(num_rails)])
        
        # Thuật toán quét ma trận Zig-zag nền
        row, col = 0, 0
        down_direction = False
        
        for i in range(len(text)):
            item = QTableWidgetItem(text[i])
            item.setTextAlignment(Qt.AlignCenter)
            
            # Làm chữ in đậm lên cho giảng viên dễ nhìn
            font = QFont()
            font.setBold(True)
            item.setFont(font)
            
            self.ui.table_matrix.setItem(row, col, item)
            
            # Đảo chiều hướng đi khi chạm ray trên cùng hoặc ray dưới cùng
            if row == 0 or row == num_rails - 1:
                down_direction = not down_direction
                
            col += 1
            row += 1 if down_direction else -1

    def call_api_encrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/encrypt"
        
        # Lấy số tầng rail từ ô txt_key
        raw_key = self.ui.txt_key.toPlainText().strip()
        plain_text = self.ui.txt_plain_text.toPlainText()

        # Kiểm tra nhanh số tầng hợp lệ trước khi gửi API
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
                    # Đổ kết quả bản mã ra ô Ciphertext
                    self.ui.txt_cipher_text.setPlainText(res_data["result"])
                    
                    # KÍCH HOẠT VẼ: Gọi hàm vẽ ma trận răng cưa với văn bản gốc (Bản rõ)
                    self.display_rail_fence(plain_text, num_rails)
                    
                    QMessageBox.information(self, "Thành công", "Mã hóa Rail Fence thành công!")
                else:
                    QMessageBox.critical(self, "Lỗi Ràng Buộc", res_data.get("message"))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Kết Nối", f"Không thể kết nối API: {str(e)}")

    def call_api_decrypt(self):
        url = "http://127.0.0.1:5000/api/railfence/decrypt"
        
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
                    # Đổ kết quả bản rõ phục hồi
                    self.ui.txt_plain_text.setPlainText(res_data["result"])
                    
                    # KÍCH HOẠT VẼ: Khi giải mã, ta dùng chuỗi kết quả thu được (Bản rõ) để tái dựng lại mô hình răng cưa
                    self.display_rail_fence(res_data["result"], num_rails)
                    
                    QMessageBox.information(self, "Thành công", "Giải mã Rail Fence thành công!")
                else:
                    QMessageBox.critical(self, "Lỗi Ràng Buộc", res_data.get("message"))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi Kết Nối", f"Không thể kết nối API: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RailFenceApp()
    window.show()
    sys.exit(app.exec_())