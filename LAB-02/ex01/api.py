import re
from flask import Flask, request, jsonify

from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher

app = Flask(__name__)

# Khởi tạo các instance mật mã toàn cục
caesar_cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()
railfence_cipher = RailFenceCipher()
playfair_cipher = PlayFairCipher()

# ==========================================
# GLOBAL VALIDATION CONFIG
# ==========================================
MAX_TEXT_LENGTH = 5000
PLAYFAIR_MIN = 2
PLAYFAIR_MAX = 25

# ==========================================
# SAFE REQUEST HANDLER
# ==========================================
def get_json_safe():
    if not request.is_json:
        return None, jsonify({"status": "error", "message": "Request phải là định dạng JSON!"})
    return request.get_json(), None

# ==========================================
# COMMON VALIDATION
# ==========================================
def validate_common(data, text_key, key_name):
    if not data:
        return None, None, "Dữ liệu JSON đầu vào không hợp lệ!"

    # SỬA LỖI: Ép kiểu str() an toàn để chặn lỗi AttributeError: 'int' object has no attribute 'strip'
    text = str(data.get(text_key) or "").strip()
    key = str(data.get(key_name) or "").strip()

    if not text or not key:
        return None, None, "Vui lòng nhập đầy đủ cả văn bản và khóa!"

    # Chuẩn hóa khoảng trắng cơ bản
    text = re.sub(r"\s+", " ", text)
    key = re.sub(r"\s+", "", key)

    return text, key, None

# ==========================================
# TEXT VALIDATION HELPERS
# ==========================================
def validate_text_length(text):
    if len(text) < 1:
        return "Văn bản không được để rỗng!"
    if len(text) > MAX_TEXT_LENGTH:
        return f"Văn bản vượt quá độ dài quy định (tối đa {MAX_TEXT_LENGTH} ký tự)!"
    return None

def validate_text_safety(text):
    if any(ord(c) < 32 and c not in "\n\t" for c in text):
        return "Văn bản chứa ký tự hệ thống không hợp lệ!"
    return None

def validate_alpha_key(key, cipher_name):
    if not re.fullmatch(r"[A-Za-z]+", key):
        return f"Khóa mật mã {cipher_name} chỉ được chứa chữ cái A-Z và không có khoảng trắng!"
    return None

# ==========================================
# ENDPOINT: CAESAR CIPHER
# ==========================================
@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data, err = get_json_safe()
    if err: return err

    text, key_raw, error = validate_common(data, "inputPlainText", "inputKeyPlain")
    if error: return jsonify({"status": "error", "message": error}), 200

    err_text = validate_text_length(text)
    if err_text: return jsonify({"status": "error", "message": err_text}), 200

    err_safe = validate_text_safety(text)
    if err_safe: return jsonify({"status": "error", "message": err_safe}), 200

    try:
        if not re.fullmatch(r"-?\d+", key_raw):
            return jsonify({"status": "error", "message": "Khóa Caesar bắt buộc phải là một số nguyên!"}), 200

        key_parsed = int(key_raw)
        key = key_parsed % 26

        if key == 0:
            return jsonify({"status": "error", "message": "Khóa không hợp lệ (Dịch chuyển mod 26 bằng 0 không làm thay đổi văn bản)!"}), 200

        result = caesar_cipher.encrypt_text(text, key)
        return jsonify({"status": "success", "result": result}), 200

    except Exception:
        return jsonify({"status": "error", "message": "Lỗi hệ thống khi xử lý mã hóa Caesar!"}), 200


@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data, err = get_json_safe()
    if err: return err

    text, key_raw, error = validate_common(data, "inputCipherText", "inputKeyCipher")
    if error: return jsonify({"status": "error", "message": error}), 200

    err_text = validate_text_length(text)
    if err_text: return jsonify({"status": "error", "message": err_text}), 200

    try:
        if not re.fullmatch(r"-?\d+", key_raw):
            return jsonify({"status": "error", "message": "Khóa Caesar bắt buộc phải là một số nguyên!"}), 200

        key = int(key_raw) % 26

        if key == 0:
            return jsonify({"status": "error", "message": "Khóa không hợp lệ (Dịch chuyển mod 26 bằng 0)!"}), 200

        result = caesar_cipher.decrypt_text(text, key)
        return jsonify({"status": "success", "result": result}), 200

    except Exception:
        return jsonify({"status": "error", "message": "Lỗi hệ thống khi xử lý giải mã Caesar!"}), 200


# ==========================================
# ENDPOINT: VIGENERE CIPHER
# ==========================================
@app.route("/api/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    data, err = get_json_safe()
    if err: return err

    text, key, error = validate_common(data, "inputPlainText", "inputKeyPlain")
    if error: return jsonify({"status": "error", "message": error}), 200

    err_text = validate_text_length(text)
    if err_text: return jsonify({"status": "error", "message": err_text}), 200

    err_key = validate_alpha_key(key, "Vigenère")
    if err_key: return jsonify({"status": "error", "message": err_key}), 200

    try:
        result = vigenere_cipher.vigenere_encrypt(text, key.upper())
        return jsonify({"status": "success", "result": result}), 200
    except Exception:
        return jsonify({"status": "error", "message": "Lỗi hệ thống khi xử lý mã hóa Vigenère!"}), 200


@app.route("/api/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    data, err = get_json_safe()
    if err: return err

    text, key, error = validate_common(data, "inputCipherText", "inputKeyCipher")
    if error: return jsonify({"status": "error", "message": error}), 200

    err_text = validate_text_length(text)
    if err_text: return jsonify({"status": "error", "message": err_text}), 200

    err_key = validate_alpha_key(key, "Vigenère")
    if err_key: return jsonify({"status": "error", "message": err_key}), 200

    try:
        result = vigenere_cipher.vigenere_decrypt(text, key.upper())
        return jsonify({"status": "success", "result": result}), 200
    except Exception:
        return jsonify({"status": "error", "message": "Lỗi hệ thống khi xử lý giải mã Vigenère!"}), 200


# ==========================================
# ENDPOINT: RAIL FENCE CIPHER
# ==========================================
# ==========================================
# ENDPOINT: RAIL FENCE CIPHER (ĐÃ SỬA CHUẨN HÓA)
# ==========================================
@app.route("/api/railfence/encrypt", methods=["POST"])
def rail_encrypt():
    data, err = get_json_safe()
    if err: return err

    text, key_raw, error = validate_common(data, "inputPlainText", "inputKeyPlain")
    if error: return jsonify({"status": "error", "message": error}), 200

    err_text = validate_text_length(text)
    if err_text: return jsonify({"status": "error", "message": err_text}), 200

    try:
        if not key_raw.isdigit():
            return jsonify({"status": "error", "message": "Khóa Rail Fence phải là số nguyên dương!"}), 200
            
        key = int(key_raw)
        
        # LÀM SẠCH: Chỉ giữ lại các chữ cái từ A-Z / a-z (Bỏ số, bỏ khoảng trắng, dấu câu)
        clean_text = "".join(c for c in text if c.isalpha())

        if key < 2:
            return jsonify({"status": "error", "message": "Số tầng đường ray (Rails) phải ≥ 2!"}), 200

        if key > len(clean_text):
            return jsonify({"status": "error", "message": "Số tầng đường ray không được lớn hơn độ dài chữ cái thực tế!"}), 200

        # SỬA TẠI ĐÂY: Truyền clean_text (đã lọc sạch) thay vì text gốc
        result = railfence_cipher.rail_fence_encrypt(clean_text, key)
        return jsonify({"status": "success", "result": result}), 200

    except Exception:
        return jsonify({"status": "error", "message": "Lỗi hệ thống khi xử lý mã hóa Rail Fence!"}), 200


@app.route("/api/railfence/decrypt", methods=["POST"])
def rail_decrypt():
    data, err = get_json_safe()
    if err: return err

    text, key_raw, error = validate_common(data, "inputCipherText", "inputKeyCipher")
    if error: return jsonify({"status": "error", "message": error}), 200

    try:
        if not key_raw.isdigit():
            return jsonify({"status": "error", "message": "Khóa Rail Fence phải là số nguyên dương!"}), 200

        key = int(key_raw)
        
        # LÀM SẠCH tương tự khi giải mã
        clean_text = "".join(c for c in text if c.isalpha())

        if key < 2:
            return jsonify({"status": "error", "message": "Số tầng đường ray (Rails) phải ≥ 2!"}), 200

        if key > len(clean_text):
            return jsonify({"status": "error", "message": "Số tầng đường ray không hợp lệ!"}), 200

        # SỬA TẠI ĐÂY: Truyền clean_text vào hàm giải mã
        result = railfence_cipher.rail_fence_decrypt(clean_text, key)
        return jsonify({"status": "success", "result": result}), 200

    except Exception:
        return jsonify({"status": "error", "message": "Lỗi hệ thống khi xử lý giải mã Rail Fence!"}), 200


# ==========================================
# ENDPOINT: PLAYFAIR CIPHER
# ==========================================
def validate_playfair_input(text, key):
    if not text:
        return "Văn bản không được để trống."

    if len(text) > MAX_TEXT_LENGTH:
        return "Văn bản quá dài."

    if not key:
        return "Khóa Playfair không được để trống."

    # Ràng buộc chặn việc gõ khoảng trắng giữa khóa
    if " " in key:
        return "Khóa Playfair không được chứa khoảng trắng (chỉ được nhập 1 từ duy nhất)."

    if not re.fullmatch(r"[A-Za-z]+", key):
        return "Khóa Playfair chỉ chứa chữ cái A-Z."

    if len(key) < PLAYFAIR_MIN or len(key) > PLAYFAIR_MAX:
        return "Độ dài khóa Playfair không hợp lệ."

    if len(set(key.upper())) < 2:
        return "Khóa phải có ít nhất 2 ký tự khác nhau."

    if not any(c.isalpha() for c in text):
        return "Văn bản phải có ít nhất 1 chữ cái."

    return None


@app.route("/api/playfair/encrypt", methods=["POST"])
def playfair_encrypt():
    data = request.json or {}
    
    raw_text = str(data.get("inputPlainText", ""))
    raw_key = str(data.get("inputKeyPlain", ""))
    
    text = raw_text.strip().upper()
    key = raw_key.strip().upper().replace("J", "I")

    error = validate_playfair_input(raw_text.strip(), raw_key.strip())
    if error:
        return jsonify({"status": "error", "message": error}), 200

    try:
        matrix = playfair_cipher.create_playfair_matrix(key)
        result = playfair_cipher.playfair_encrypt(text, matrix)

        return jsonify({
            "status": "success", 
            "text": text, 
            "key": key, 
            "result": result, 
            "matrix": matrix
        }), 200

    except Exception:
        return jsonify({"status": "error", "message": "Lỗi hệ thống khi xử lý Playfair Encrypt!"}), 200


@app.route("/api/playfair/decrypt", methods=["POST"])
def playfair_decrypt():
    data = request.json or {}
    
    raw_text = str(data.get("inputCipherText", ""))
    raw_key = str(data.get("inputKeyCipher", ""))
    
    text = raw_text.strip().upper()
    key = raw_key.strip().upper().replace("J", "I")

    error = validate_playfair_input(raw_text.strip(), raw_key.strip())
    if error:
        return jsonify({"status": "error", "message": error}), 200

    if len(re.sub(r'[^A-Z]', '', text)) % 2 != 0:
        return jsonify({"status": "error", "message": "Ciphertext Playfair phải có số ký tự chữ chẵn."}), 200

    try:
        matrix = playfair_cipher.create_playfair_matrix(key)
        result = playfair_cipher.playfair_decrypt(text, matrix)

        return jsonify({
            "status": "success", 
            "text": text, 
            "key": key, 
            "result": result, 
            "matrix": matrix
        }), 200

    except Exception:
        return jsonify({"status": "error", "message": "Lỗi hệ thống khi xử lý Playfair Decrypt!"}), 200


# ==========================================
# RUN SERVER
# ==========================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)