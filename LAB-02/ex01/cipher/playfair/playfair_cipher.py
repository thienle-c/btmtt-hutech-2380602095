import re

class PlayFairCipher:
    def __init__(self) -> None:
        pass

    def create_playfair_matrix(self, key):
        # Chuẩn hóa khóa: viết hoa, đổi J thành I, lọc bỏ mọi ký tự không phải chữ
        key = "".join(c.upper() for c in key if c.isalpha()).replace("J", "I")

        # ĐỂ KHÔNG BỊ LẶP CHỮ: Duyệt qua từng ký tự của khóa và lọc trùng giữ nguyên thứ tự
        unique_key_letters = []
        for letter in key:
            if letter not in unique_key_letters:
                unique_key_letters.append(letter)

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

        # Lọc các chữ cái còn lại chưa xuất hiện trong khóa đã lọc trùng
        remaining_letters = [
            letter for letter in alphabet
            if letter not in unique_key_letters
        ]

        # Gộp chuỗi khóa sạch và chuỗi bảng chữ cái sạch thành mảng 25 phần tử duy nhất
        matrix = unique_key_letters + remaining_letters

        # Chia thành ma trận 5x5 hoàn hảo
        playfair_matrix = [
            matrix[i:i + 5]
            for i in range(0, 25, 5)
        ]

        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        # Trả về tọa độ mặc định (0,0) nếu gặp ký tự lạ để tránh crash app ngoài ý muốn
        return 0, 0

    def playfair_encrypt(self, plain_text, matrix):
        # Lọc sạch văn bản: chỉ lấy các chữ cái từ A-Z, chuyển J thành I
        plain_text = "".join(c.upper() for c in plain_text if c.isalpha()).replace("J", "I")
        
        if not plain_text:
            return ""

        # Tiền xử lý chèn ký tự đệm 'X' cho các cặp trùng nhau (Ví dụ: LL -> LX)
        prepared_text = ""
        i = 0
        while i < len(plain_text):
            prepared_text += plain_text[i]
            if i + 1 < len(plain_text):
                if plain_text[i] == plain_text[i + 1]:
                    # Nếu 2 ký tự đi liền nhau giống nhau, chèn thêm 'X' vào giữa
                    prepared_text += "X"
                    i += 1
                else:
                    prepared_text += plain_text[i + 1]
                    i += 2
            else:
                i += 1

        # Nếu tổng chuỗi sau khi xử lý trùng bị lẻ, chèn thêm 'X' ở cuối
        if len(prepared_text) % 2 != 0:
            prepared_text += "X"

        encrypted_text = ""

        # Tiến hành mã hóa theo các cặp đôi (Bigram)
        for i in range(0, len(prepared_text), 2):
            pair = prepared_text[i:i + 2]

            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:  # Cùng hàng -> Trượt phải
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:  # Cùng cột -> Trượt xuống
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:  # Tạo thành hình chữ nhật -> Đổi góc chéo
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]

        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        # Bản mã Playfair chuẩn bắt buộc chỉ chứa chữ cái chữ in hoa
        cipher_text = "".join(c.upper() for c in cipher_text if c.isalpha())
        
        if not cipher_text or len(cipher_text) % 2 != 0:
            return ""

        decrypted_text = ""

        # Tiến hành giải mã hình học ngược cho từng cặp
        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i + 2]

            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:  # Cùng hàng -> Trượt trái
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:  # Cùng cột -> Trượt lên
                decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:  # Hình chữ nhật -> Đổi góc chéo
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]

        # Khôi phục bản rõ gốc (Xóa bỏ các ký tự đệm 'X' đã thêm lúc mã hóa một cách chính xác)
        banro = ""
        i = 0
        while i < len(decrypted_text):
            banro += decrypted_text[i]
            if i + 1 < len(decrypted_text):
                # Nếu chữ tiếp theo là 'X' nằm giữa 2 chữ giống nhau (Ví dụ: L X L) -> Bỏ qua chữ X đó
                if decrypted_text[i + 1] == "X" and i + 2 < len(decrypted_text) and decrypted_text[i] == decrypted_text[i + 2]:
                    banro += decrypted_text[i + 2]
                    i += 3
                else:
                    banro += decrypted_text[i + 1]
                    i += 2
            else:
                i += 1

        # Nếu chữ cái cuối cùng là 'X' dư thừa do ép chuỗi chẵn lúc trước -> Cắt bỏ đi
        if banro.endswith("X") and len(banro) > 1:
            banro = banro[:-1]

        return banro