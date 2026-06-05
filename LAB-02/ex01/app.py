from flask import Flask, render_template, request, jsonify

# Import đúng cấu trúc thư mục từ package cipher
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')


# --- 1. ROUTE CAESAR ---
@app.route("/api/caesar/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form.get('inputPlainText', '').strip()
    key_raw = request.form.get('inputKeyPlain', '').strip()
    
    if not text or not key_raw:
        return jsonify({"status": "error", "message": "Vui lòng nhập đầy đủ văn bản và khóa!"})
    try:
        key = int(key_raw)
    except ValueError:
        return jsonify({"status": "error", "message": "Khóa Caesar phải là một số nguyên!"})
        
    Caesar = CaesarCipher()
    res = Caesar.encrypt_text(text, key)
    return jsonify({"status": "success", "text": text, "key": key, "result": res})

@app.route("/api/caesar/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form.get('inputCipherText', '').strip()
    key_raw = request.form.get('inputKeyCipher', '').strip()
    
    if not text or not key_raw:
        return jsonify({"status": "error", "message": "Vui lòng nhập đầy đủ văn bản và khóa!"})
    try:
        key = int(key_raw)
    except ValueError:
        return jsonify({"status": "error", "message": "Khóa Caesar phải là một số nguyên!"})
        
    Caesar = CaesarCipher()
    res = Caesar.decrypt_text(text, key)
    return jsonify({"status": "success", "text": text, "key": key, "result": res})


# --- 2. ROUTE VIGENÈRE ---
@app.route("/api/vigenere/encrypt", methods=['POST'])
def vigenere_encrypt():
    text = request.form.get('inputPlainText', '').strip()
    key = request.form.get('inputKeyPlain', '').strip().upper()
    
    if not text or not key:
        return jsonify({"status": "error", "message": "Vui lòng nhập đầy đủ văn bản và khóa!"})
    if not key.isalpha():
        return jsonify({"status": "error", "message": "Khóa Vigenère chỉ được chứa các ký tự chữ cái (A-Z)!"})
        
    Vigenere = VigenereCipher() 
    res = Vigenere.vigenere_encrypt(text, key)
    return jsonify({"status": "success", "text": text, "key": key, "result": res})

@app.route("/api/vigenere/decrypt", methods=['POST'])
def vigenere_decrypt():
    text = request.form.get('inputCipherText', '').strip()
    key = request.form.get('inputKeyCipher', '').strip().upper()
    
    if not text or not key:
        return jsonify({"status": "error", "message": "Vui lòng nhập đầy đủ văn bản và khóa!"})
    if not key.isalpha():
        return jsonify({"status": "error", "message": "Khóa Vigenère chỉ được chứa các ký tự chữ cái (A-Z)!"})
        
    Vigenere = VigenereCipher()
    res = Vigenere.vigenere_decrypt(text, key)
    return jsonify({"status": "success", "text": text, "key": key, "result": res})


# --- 3. ROUTE RAIL FENCE ---
@app.route("/api/railfence/encrypt", methods=['POST'])
def railfence_encrypt():
    text = request.form.get('inputPlainText', '').strip()
    key_raw = request.form.get('inputKeyPlain', '').strip()
    
    if not text or not key_raw:
        return jsonify({"status": "error", "message": "Vui lòng nhập đầy đủ văn bản và khóa!"})
    try:
        key = int(key_raw)
        if key < 2:
            return jsonify({"status": "error", "message": "Số đường rào (Rails) phải lớn hơn hoặc bằng 2!"})
    except ValueError:
        return jsonify({"status": "error", "message": "Khóa Rail Fence phải là số nguyên hợp lệ!"})
        
    rf = RailFenceCipher()
    res = rf.rail_fence_encrypt(text, key)
    return jsonify({"status": "success", "text": text, "key": key, "result": res})

@app.route("/api/railfence/decrypt", methods=['POST'])
def railfence_decrypt():
    text = request.form.get('inputCipherText', '').strip()
    key_raw = request.form.get('inputKeyCipher', '').strip()
    
    if not text or not key_raw:
        return jsonify({"status": "error", "message": "Vui lòng nhập đầy đủ văn bản và khóa!"})
    try:
        key = int(key_raw)
        if key < 2:
            return jsonify({"status": "error", "message": "Số đường rào (Rails) phải lớn hơn hoặc bằng 2!"})
    except ValueError:
        return jsonify({"status": "error", "message": "Khóa Rail Fence phải là số nguyên hợp lệ!"})
        
    rf = RailFenceCipher()
    res = rf.rail_fence_decrypt(text, key)
    return jsonify({"status": "success", "text": text, "key": key, "result": res})


# --- 4. ROUTE PLAYFAIR ---
@app.route("/api/playfair/encrypt", methods=['POST'])
def playfair_encrypt():
    text = request.form.get('inputPlainText', '').strip()
    key = request.form.get('inputKeyPlain', '').strip()
    
    if not text or not key:
        return jsonify({"status": "error", "message": "Vui lòng nhập đầy đủ văn bản và khóa!"})
    
    # Lọc chuỗi khóa xem có chứa chữ cái nào không
    clean_key = "".join([c for c in key if c.isalpha()])
    if not clean_key:
        return jsonify({"status": "error", "message": "Khóa Playfair phải chứa ít nhất một chữ cái hợp lệ!"})
        
    pf = PlayFairCipher()
    matrix = pf.create_playfair_matrix(key)
    res = pf.playfair_encrypt(text, matrix)
    
    return jsonify({
        "status": "success",
        "text": text, 
        "key": key.upper(), 
        "result": res,
        "matrix": matrix
    })

@app.route("/api/playfair/decrypt", methods=['POST'])
def playfair_decrypt():
    text = request.form.get('inputCipherText', '').strip()
    key = request.form.get('inputKeyCipher', '').strip()
    
    if not text or not key:
        return jsonify({"status": "error", "message": "Vui lòng nhập đầy đủ văn bản và khóa!"})
        
    clean_key = "".join([c for c in key if c.isalpha()])
    if not clean_key:
        return jsonify({"status": "error", "message": "Khóa Playfair phải chứa ít nhất một chữ cái hợp lệ!"})
        
    pf = PlayFairCipher()
    matrix = pf.create_playfair_matrix(key)
    res = pf.playfair_decrypt(text, matrix)
    
    return jsonify({
        "status": "success",
        "text": text, 
        "key": key.upper(), 
        "result": res,
        "matrix": matrix
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)