def truy_cap_phan_tu_tuple(tup_data):
    first_element = tup_data[0]
    last_element = tup_data[-1]
    return first_element, last_element
input_tuple = eval(input("Nhập tuple (ví dụ: (1, 2, 3)): "))
first,last = truy_cap_phan_tu_tuple(input_tuple)
print("Phần tử đầu tiên của tuple là:", first)
print("Phần tử cuối cùng của tuple là:", last)