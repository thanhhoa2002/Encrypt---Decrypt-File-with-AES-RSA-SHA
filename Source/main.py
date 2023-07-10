import os
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showinfo
import threading

import AES
import SHA
import RSA
import os

n = 0
P = ""
C = ""
Cname = ""
Ks = ""
Kprivate = (0,0)
Kpublic = (0,0)
Kx = ""
HKprivate = ""

def read_file_P():
    # Hiển thị hộp thoại để chọn tệp 
    global P
    P = askopenfilename()
    if P:
        encrypt_display_lable1.config(text=P)
        encrypt_display_lable2.grid(row=2, column=0, columnspan=2, pady=0)
        encrypt_button3.grid(row=2, column=2, pady=10, padx=10)
    else:
        encrypt_display_lable1.config(text="Chọn file để mã hoá")
        showinfo(title="Chọn file để mã hoá", message="Chọn lại file")
        
def write_file_C():
    # phát sinh khoá Ks và mã hoá P->C bằng AES
    global Ks, Kprivate, Kpublic, Kx, HKprivate, Cname, n
    Ks = AES.generate_random_string(16)
    byte_key = AES.string_to_bytes(Ks)
    C = asksaveasfilename()
    print(C)
    if C:
        encrypt_display_lable2.config(text=C)
        AES.encrypt_file(P, C, byte_key)
        Cname = os.path.splitext(os.path.basename(C))[0]
        showinfo(title="Mã hoá tập tin", message="Mã hoá tập tin thành công")
        
        # Tạo cửa sổ con cho hiệu ứng loading
        loading_window = tk.Toplevel(window)
        loading_window.title("Tạo key RSA")
        loading_window.geometry("200x100")
        
        # Tạo label để hiển thị hiệu ứng loading
        loading_label = tk.Label(loading_window, text="Tạo key RSA...")
        loading_label.pack(pady=30)
        
        def gen_key_encrypt():
            global Kprivate
            Kprivate, Kpublic = RSA.gen_rsa_keypair()
            n = Kprivate[1]
            Kx = RSA.rsa_encrypt_string(Ks, Kpublic[0], Kpublic[1])
            HKprivate = SHA.sha1_hash_string(str(Kprivate[0]))
            with open(Cname + ".metadata", "w") as file:
                file.write(Kx)
                file.write('\n')
                file.write(HKprivate)
            file.close()
            # Đóng cửa sổ loading
            loading_window.destroy()
            encrypt_display_lable3_1.config(text="Khoá Private:")
            encrypt_display_lable3_2.config(text=Kprivate[0])
            encrypt_display_lable3_3.config(text=Kprivate[1])
            encrypt_button4.grid(row=4, column=0, padx=10)
            showinfo(title="Tạo key RSA", message="Tạo key RSA thành công")
        
        # Tạo và khởi chạy một luồng riêng biệt
        thread = threading.Thread(target=gen_key_encrypt)
        thread.start()
    else:
        encrypt_display_lable2.config(text="Lưu file đã mã hoá")
        showinfo(title="Mã hoá tập tin", message="Mã hoá không thành công")

def write_Kprivate():
    pri_file = asksaveasfilename()
    if pri_file:
        with open(pri_file, "w") as file:
            file.write(str(Kprivate[0]))
            file.write("\n")
            file.write(str(Kprivate[1]))
        file.close()
        showinfo(title="Lưu khoá Kprivate", message="Lưu thành công")
    else:
        showinfo(title="Lưu khoá Kprivate", message="Lưu không thành công")
        
def read_file_C():
    global C, Cname
    C = askopenfilename()
    Cname = os.path.splitext(os.path.basename(C))[0]
    if C:
        decrypt_display_lable1.config(text=C)
        decrypt_display_lable2.grid(row=2, column=0, columnspan=2, pady=0)
        decrypt_button3.grid(row=2, column=2, pady=20, padx=10)
        decrypt_display_lable3.grid(row=3, column=0, pady=0)
        decrypt_display_lable4.grid(row=4, column=0, pady=0)
        entry1.grid(row=3, column=1, pady=2)
        entry2.grid(row=4, column=1, pady=2)
        decrypt_button4.grid(row=3, rowspan=2, column=2, pady=20, padx=10)
    else:
        encrypt_display_lable1.config(text="Chọn file để giải mã")
        showinfo(title="Chọn file để mã hoá", message="Chọn lại file")
        
def read_Kprivate():
    global Kprivate
    pri_file = askopenfilename()
    if pri_file:
        with open(pri_file, "r") as file:
            d = int(file.readline())
            n = int(file.readline())
            Kprivate = (d, n)
            write_file_P()
        file.close()
    else:
        showinfo(title="Đọc khoá Kprivate", message="Đọc không thành công")

def check_input():
    global Kprivate
    if entry1.get().isdigit():
        if entry2.get().isdigit():
            Kprivate = (entry1.get(), entry2.get())
            write_file_P()
        else:
            showinfo(title="Nhập key", message="Hãy nhập số n")
    else:
        showinfo(title="Nhập key", message="Hãy nhập số d")

def write_file_P():
    metadata_file = Cname + ".metadata"
    if metadata_file:
        with open(metadata_file, "r") as file:
            Kx = file.readline()
            HKprivate = file.readline()
        file.close()
        Kprivate_hash = SHA.sha1_hash_string(str(Kprivate[0]))
        if Kprivate_hash != HKprivate:
            showinfo(title="Giải mã tập tin", message="Giải mã thất bại")
        else:
            Ks = RSA.rsa_decrypt_string(Kx, Kprivate[0], Kprivate[1])
            byte_key = AES.string_to_bytes(Ks)
            showinfo(title="Giải mã tập tin", message="Giải mã thành công\nHãy lưu file giải mã")
            P = asksaveasfilename()
            AES.decrypt_file(C, P, byte_key)
            decrypt_to_main()
    else:
        showinfo(title="Metadata", message="Dữ liệu metadata không tồn tại")
        decrypt_to_main()
    

# Hàm để hiển thị giao diện mới
def main_to_encrypt():
    main_frame.pack_forget()
    encrypt_display_lable1.config(text="Chọn file để mã hoá")
    encrypt_display_lable2.config(text="Lưu file đã mã hoá")
    encrypt_display_lable3_1.config(text="")
    encrypt_display_lable3_2.config(text="")
    encrypt_display_lable3_3.config(text="")
    encrypt_display_lable2.grid_forget()
    encrypt_button3.grid_forget()
    encrypt_button4.grid_forget()
    encrypt_frame.pack()
    
def main_to_decrypt():
    main_frame.pack_forget()
    decrypt_display_lable1.config(text="Chọn file để giải mã")
    decrypt_display_lable2.grid_forget()
    decrypt_button3.grid_forget()
    decrypt_display_lable3.grid_forget()
    decrypt_display_lable4.grid_forget()
    entry1.grid_forget()
    entry2.grid_forget()
    decrypt_button4.grid_forget()
    decrypt_frame.pack()    

# Hàm để quay lại giao diện chính
def encrypt_to_main():
    global n, P, C, Cname, Ks, Kprivate, Kpublic, Kx, HKprivate
    n = 0
    P = ""
    C = ""
    Cname = ""
    Ks = ""
    Kprivate = (0,0)
    Kpublic = (0,0)
    Kx = ""
    HKprivate = ""
    encrypt_frame.pack_forget()
    main_frame.pack()
    
def decrypt_to_main():
    global n, P, C, Cname, Ks, Kprivate, Kpublic, Kx, HKprivate
    n = 0
    P = ""
    C = ""
    Cname = ""
    Ks = ""
    Kprivate = (0,0)
    Kpublic = (0,0)
    Kx = ""
    HKprivate = ""
    decrypt_frame.pack_forget()
    main_frame.pack()
    
# Hàm để đóng cửa sổ
def close_window():
    window.destroy()    

#####################################

# Tạo cửa sổ giao diện
window = tk.Tk()
window.title("Mã hoá - Giải mã tập tin")
window.geometry("800x500")

# Tạo khung cho giao diện chính
main_frame = tk.Frame(window)
main_frame.pack()

# main_frame
main_lable = tk.Label(main_frame, text="MÃ HOÁ - GIẢI MÃ TẬP TIN", font=("Arial", 40), fg="black", pady=40)
main_lable.pack()
main_button_1 = tk.Button(main_frame, text="Mã hoá tập tin", font=("Arial", 20), fg="black", bg="orange", width=15, command=main_to_encrypt)
main_button_1.pack(pady=10)
main_button_2 = tk.Button(main_frame, text="Giải mã tập tin", font=("Arial", 20), fg="black", bg="lime", width=15, command=main_to_decrypt)
main_button_2.pack(pady=10)
main_button_3 = tk.Button(main_frame, text="Thoát", font=("Arial", 20), fg="white", bg="red", width=15, command=close_window)
main_button_3.pack(pady=10)


# mã hoá
encrypt_frame = tk.Frame(window)
encrypt_lable = tk.Label(encrypt_frame, text="MÃ HOÁ TẬP TIN", font=("Arial", 40), fg="black", pady=40)
encrypt_lable.grid(row=0, column=1, pady=0)
encrypt_button = tk.Button(encrypt_frame, text="<", font=("Arial", 15), fg="white", bg="red", command=encrypt_to_main)
encrypt_button.grid(row=0, column=0, pady=10)

encrypt_display_lable1 = tk.Label(encrypt_frame, text="Chọn file để mã hoá", font=("Arial", 15), fg="black", width=50, height=2, borderwidth=2, relief="solid")
encrypt_display_lable1.grid(row=1, column=0, columnspan=2, pady=0)
encrypt_button2 = tk.Button(encrypt_frame, text="File...", font=("Arial", 15), fg="black", command=read_file_P)
encrypt_button2.grid(row=1, column=2, pady=10, padx=10)

encrypt_display_lable2 = tk.Label(encrypt_frame, text="Lưu file đã mã hoá", font=("Arial", 15), fg="black", width=50, height=2, borderwidth=2, relief="solid")
encrypt_button3 = tk.Button(encrypt_frame, text="File...", font=("Arial", 15), fg="black", command=write_file_C)

encrypt_display_lable3_1 = tk.Label(encrypt_frame, text="", font=("Arial", 15), fg="green")
encrypt_display_lable3_1.grid(row=3, column=0, pady=20, padx=10)
encrypt_display_lable3_2 = tk.Label(encrypt_frame, text="", font=("Arial", 15), fg="red", anchor="w", wraplength=500)
encrypt_display_lable3_2.grid(row=3, column=1, columnspan=2 , pady=0, padx=0)
encrypt_display_lable3_3 = tk.Label(encrypt_frame, text="", font=("Arial", 15), fg="black", anchor="w", wraplength=500)
encrypt_display_lable3_3.grid(row=4, column=1, columnspan=2, pady=0, padx=0)
encrypt_button4 = tk.Button(encrypt_frame, text="Lưu khoá", font=("Arial", 15), fg="black", command=write_Kprivate)


# giải mã
decrypt_frame = tk.Frame(window)
decrypt_lable = tk.Label(decrypt_frame, text="GIẢI MÃ TẬP TIN", font=("Arial", 40), fg="black", pady=40)
decrypt_lable.grid(row=0, column=1, pady=0)
decrypt_button = tk.Button(decrypt_frame, text="<", font=("Arial", 15), fg="white", bg="red", command=decrypt_to_main)
decrypt_button.grid(row=0, column=0, pady=0)

decrypt_display_lable1 = tk.Label(decrypt_frame, text="Chọn file để giải mã", font=("Arial", 15), fg="black", width=50, height=2, borderwidth=2, relief="solid")
decrypt_display_lable1.grid(row=1, column=0, columnspan=2, pady=20)
decrypt_button2 = tk.Button(decrypt_frame, text="File...", font=("Arial", 15), fg="black", command=read_file_C)
decrypt_button2.grid(row=1, column=2, pady=20, padx=10)

decrypt_display_lable2 = tk.Label(decrypt_frame, text="Nhập khoá Kprivate hoặc chọn từ file", font=("Arial", 15), fg="black", width=50, height=2)
decrypt_button3 = tk.Button(decrypt_frame, text="File...", font=("Arial", 15), fg="black", command=read_Kprivate)
decrypt_display_lable3 = tk.Label(decrypt_frame, text="d", font=("Arial", 15), fg="black", anchor="w")
decrypt_display_lable4 = tk.Label(decrypt_frame, text="n", font=("Arial", 15), fg="black", anchor="w")
entry1 = tk.Entry(decrypt_frame, font=("Arial", 15), fg="black", width=50, borderwidth=2, relief="solid")
entry2 = tk.Entry(decrypt_frame, font=("Arial", 15), fg="black", width=50, borderwidth=2, relief="solid")
decrypt_button4 = tk.Button(decrypt_frame, text="Nhập", font=("Arial", 15), fg="black", command=check_input)


# Chạy vòng lặp chờ sự kiện
window.mainloop()