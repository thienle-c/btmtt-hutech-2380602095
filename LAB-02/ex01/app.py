from flask import Flask, render_template, request, jsonify
import re

from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher

app = Flask(__name__)

# =========================
# CONSTANTS
# =========================

MAX_TEXT_LENGTH = 10000

CAESAR_MIN = 1
CAESAR_MAX = 25

VIGENERE_MIN = 2
VIGENERE_MAX = 50

PLAYFAIR_MIN = 3
PLAYFAIR_MAX = 25

RAIL_MIN = 2
RAIL_MAX = 50


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# COMMON VALIDATORS
# =========================

def validate_required(text, key):
    if not text or not key:
        return "Vui lòng nhập đầy đủ văn bản và khóa!"
    return None


def validate_alpha_key(key, cipher_name):
    if not re.fullmatch(r"[A-Za-z]+", key):
        return f"Khóa {cipher_name} chỉ được chứa chữ cái A-Z!"
    return None


# =========================
# CAESAR
# =========================

def validate_caesar_input(text, key_raw):
    if not text:
        return "Văn bản không được để trống."

    if len(text) > MAX_TEXT_LENGTH:
        return f"Văn bản không được vượt quá {MAX_TEXT_LENGTH} ký tự."

    if not key_raw:
        return "Khóa Caesar không được để trống."

    try:
        key = int(key_raw)
    except ValueError:
        return "Khóa Caesar phải là số nguyên."

    if not (CAESAR_MIN <= key <= CAESAR_MAX):
        return "Khóa Caesar phải nằm trong khoảng 1–25."

    return None


@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    text = request.form.get("inputPlainText", "").strip()
    key_raw = request.form.get("inputKeyPlain", "").strip()

    error = validate_caesar_input(text, key_raw)
    if error:
        return jsonify({"status": "error", "message": error}), 400

    try:
        key = int(key_raw)
        cipher = CaesarCipher()
        result = cipher.encrypt_text(text, key)

        return jsonify({"status": "success", "text": text, "key": key, "result": result}), 200

    except Exception:
        return jsonify({"status": "error", "message": "Lỗi hệ thống Caesar Encrypt"}), 500


@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    text = request.form.get("inputCipherText", "").strip()
    key_raw = request.form.get("inputKeyCipher", "").strip()

    error = validate_caesar_input(text, key_raw)
    if error:
        return jsonify({"status": "error", "message": error}), 400

    try:
        key = int(key_raw)
        cipher = CaesarCipher()
        result = cipher.decrypt_text(text, key)

        return jsonify({"status": "success", "text": text, "key": key, "result": result}), 200

    except Exception:
        return jsonify({"status": "error", "message": "Lỗi hệ thống Caesar Decrypt"}), 500


# =========================
# VIGENERE
# =========================

def validate_vigenere_input(text, key):
    if not text:
        return "Văn bản không được để trống."

    if len(text) > MAX_TEXT_LENGTH:
        return "Văn bản quá dài."

    if not key:
        return "Khóa Vigenère không được để trống."

    if not re.fullmatch(r"[A-Za-z]+", key):
        return "Khóa Vigenère chỉ chứa chữ cái A-Z."

    if len(key) < VIGENERE_MIN or len(key) > VIGENERE_MAX:
        return "Độ dài khóa Vigenère không hợp lệ."

    if len(set(key.upper())) == 1:
        return "Khóa không được toàn ký tự giống nhau."

    return None


@app.route("/api/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    text = request.form.get("inputPlainText", "").strip()
    key = request.form.get("inputKeyPlain", "").strip().upper()

    error = validate_vigenere_input(text, key)
    if error:
        return jsonify({"status": "error", "message": error}), 400

    try:
        cipher = VigenereCipher()
        result = cipher.vigenere_encrypt(text, key)

        return jsonify({"status": "success", "text": text, "key": key, "result": result}), 200

    except Exception:
        return jsonify({"status": "error", "message": "Lỗi hệ thống Vigenère Encrypt"}), 500


@app.route("/api/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    text = request.form.get("inputCipherText", "").strip()
    key = request.form.get("inputKeyCipher", "").strip().upper()

    error = validate_vigenere_input(text, key)
    if error:
        return jsonify({"status": "error", "message": error}), 400

    try:
        cipher = VigenereCipher()
        result = cipher.vigenere_decrypt(text, key)

        return jsonify({"status": "success", "text": text, "key": key, "result": result}), 200

    except Exception:
        return jsonify({"status": "error", "message": "Lỗi hệ thống Vigenère Decrypt"}), 500


# =========================
# RAIL FENCE
# =========================

def validate_railfence_input(text, key_raw):
    if not text:
        return None, "Văn bản không được để trống."

    if len(text) > MAX_TEXT_LENGTH:
        return None, "Văn bản quá dài."

    if not key_raw:
        return None, "Khóa Rail Fence không được để trống."

    try:
        key = int(key_raw)
    except ValueError:
        return None, "Khóa phải là số nguyên."

    if key < RAIL_MIN or key > RAIL_MAX:
        return None, "Khóa Rail Fence không hợp lệ."

    if key >= len(text):
        return None, "Khóa phải nhỏ hơn độ dài văn bản."

    return key, None


@app.route("/api/railfence/encrypt", methods=["POST"])
def railfence_encrypt():
    text = request.form.get("inputPlainText", "").strip()
    key_raw = request.form.get("inputKeyPlain", "").strip()

    key, error = validate_railfence_input(text, key_raw)
    if error:
        return jsonify({"status": "error", "message": error}), 400

    try:
        cipher = RailFenceCipher()
        result = cipher.rail_fence_encrypt(text, key)

        return jsonify({"status": "success", "text": text, "key": key, "result": result}), 200

    except Exception:
        return jsonify({"status": "error", "message": "Lỗi Rail Fence Encrypt"}), 500


@app.route("/api/railfence/decrypt", methods=["POST"])
def railfence_decrypt():
    text = request.form.get("inputCipherText", "").strip()
    key_raw = request.form.get("inputKeyCipher", "").strip()

    key, error = validate_railfence_input(text, key_raw)
    if error:
        return jsonify({"status": "error", "message": error}), 400

    try:
        cipher = RailFenceCipher()
        result = cipher.rail_fence_decrypt(text, key)

        return jsonify({"status": "success", "text": text, "key": key, "result": result}), 200

    except Exception:
        return jsonify({"status": "error", "message": "Lỗi Rail Fence Decrypt"}), 500


# =========================
# PLAYFAIR
# =========================

def validate_playfair_input(text, key):
    if not text:
        return "Văn bản không được để trống."

    if len(text) > MAX_TEXT_LENGTH:
        return "Văn bản quá dài."

    if not key:
        return "Khóa Playfair không được để trống."

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
    text = request.form.get("inputPlainText", "").strip().upper()
    key = request.form.get("inputKeyPlain", "").strip().upper().replace("J", "I")

    error = validate_playfair_input(text, key)
    if error:
        return jsonify({"status": "error", "message": error}), 400

    try:
        cipher = PlayFairCipher()
        matrix = cipher.create_playfair_matrix(key)
        result = cipher.playfair_encrypt(text, matrix)

        return jsonify({"status": "success", "text": text, "key": key, "result": result, "matrix": matrix}), 200

    except Exception:
        return jsonify({"status": "error", "message": "Lỗi Playfair Encrypt"}), 500


@app.route("/api/playfair/decrypt", methods=["POST"])
def playfair_decrypt():
    text = request.form.get("inputCipherText", "").strip().upper()
    key = request.form.get("inputKeyCipher", "").strip().upper().replace("J", "I")

    error = validate_playfair_input(text, key)
    if error:
        return jsonify({"status": "error", "message": error}), 400

    if len(re.sub(r'[^A-Z]', '', text)) % 2 != 0:
        return jsonify({"status": "error", "message": "Ciphertext Playfair phải có số ký tự chẵn."}), 400

    try:
        cipher = PlayFairCipher()
        matrix = cipher.create_playfair_matrix(key)
        result = cipher.playfair_decrypt(text, matrix)

        return jsonify({"status": "success", "text": text, "key": key, "result": result, "matrix": matrix}), 200

    except Exception:
        return jsonify({"status": "error", "message": "Lỗi Playfair Decrypt"}), 500


# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)