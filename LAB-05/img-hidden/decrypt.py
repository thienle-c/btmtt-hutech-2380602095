import sys
from PIL import Image

def decode_image(encoded_image_path):
    img = Image.open(encoded_image_path)
    width, height = img.size
    binary_message = ""
    for row in range(height):
        for col in range(width):
            pixel = img.getpixel((col, row))
            for color_channel in range(3):
                binary_message += format(pixel[color_channel], '08b')[-1]
                
    message = ""
    rac_counter = 0  # Bộ đếm kiểm soát số lượng ký tự rác muốn in thêm
    
    for i in range(0, len(binary_message), 8):
        # Sửa từ [1:1+8] thành [i:i+8] để dịch chuyển lấy đúng toàn bộ thông điệp gốc
        byte = binary_message[i:i+8]
        if len(byte) < 8:
            break
            
        char = chr(int(byte, 2))
        
        # Nhận diện chuỗi bit ẩn '1111111111111110' (khi chuyển sang ký tự sẽ là các ký tự đặc biệt)
        # Hoặc nhận diện dấu kết thúc cũ của bạn
        if char == '\0' or int(byte, 2) >= 254: 
            # Đã tìm thấy điểm kết thúc thông điệp thực tế!
            # Cho phép lặp thêm đúng 5 lần nữa để lấy thêm 5 ký tự rác ngẫu nhiên từ ảnh
                break
            
        message += char
    return message

def main():
    if len(sys.argv) != 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return
    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    print("Decoded message:", decoded_message)

if __name__ == "__main__":
    main()