import keyword
import re
from SinhVien import sinhvien
class QuanLySinhVien:
    listSinhVien = []
    def generateID(self):
        maxId = 1
        if (self.soluongSinhVien() > 0):
            maxId = self.listSinhVien[0]._id
            for sv in self.listSinhVien:
                if (sv._id > maxId):
                    maxId = sv._id
            maxId += 1
            return maxId
    def soluongSinhVien(self):
        return self.listSinhVien.__len__()
    def nhapSinhVien(self):
        svId = self.generateID()
        name = input("Nhập tên sinh viên: ")
        sex = input("Nhập giới tính sinh viên: ")
        major = input("Nhập chuyên ngành sinh viên: ")
        diemTB = float(input("Nhập điểm trung bình sinh viên: "))
        sv = sinhvien(svId, name, sex, major, diemTB)
        self.xeploaiHocLuc(sv)
        self.listSinhVien.append(sv)
    def updatesinhvien(self,ID):
        sv:SinhVien = self.FindByID(ID)
        if (sv != None):
            name = input("Nhập tên sinh viên: ")
            sex = input("Nhập giới tính sinh viên: ")
            major = input("Nhập chuyên ngành sinh viên: ")
            diemTB = float(input("Nhập điểm trung bình sinh viên: "))
            sv._name = name
            sv._sex = sex
            sv._major = major
            sv._diemTB = diemTB
            self.xeploaiHocLuc(sv)
        else:
            print(f"sinh vien co ID = {ID} không tồn tại.".format(ID))
        def sortByID(self):
            self.listSinhVien.sort(key=lambda x: x._id, reverse=False)
            
        def sortByDiemTB(self):
            self.listSinhVien.sort(key=lambda x: x._diemTB, reverse=False)
        def findByID(self,ID):
            searchResult = None
            if (self.soluongSinhVien() > 0):
                for sv in self.listSinhVien:
                    if (sv._id == ID):
                        searchResult = sv
                        break
            return searchResult
        def FindByName(self, Keyword):
            listSV = []
            if (self.soluongSinhVien() > 0):
                for sv in self.listSinhVien:
                    if (keyword.upper() in sv._name.upper()):
                        listSV.append(sv)
            return listSV
        def deleteById(self,ID):
            isDeleted = False
            sv = self.FindByID(ID)
            if (sv != None):
                self.listSinhVien.remove(sv)
                isDeleted = True
            return isDeleted
        def xeploaiHocLuc(self,sv:sinhvien):
            if (sv._diemTB >= 8):
                sv._hocLuc = "Giỏi"
            elif (sv._diemTB >= 6.5):
                sv._hocLuc = "Khá"
            elif (sv._diemTB >= 5):
                sv._hocLuc = "Trung bình"
            else:
                sv._hocLuc = "Yếu"
            
            