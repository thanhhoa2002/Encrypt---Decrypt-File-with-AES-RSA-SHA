import random
import math

# kiểm tra số nguyên tố
def is_prime(n):
    if n <= 1:
        return False

    if n <= 3:
        return True

    if n % 2 == 0 or n % 3 == 0:
        return False

    sqrt_n = int(math.sqrt(n))
    for i in range(5, sqrt_n + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False

    return True

def gen_big_number(min_bit_length, max_bit_length):
    bit_length = random.randint(min_bit_length, max_bit_length)
    binary_string = ''
    for i in range(bit_length):
        binary_string += str(random.randint(0, 1))
    interger_value = int(binary_string, 2)
    return interger_value

# sinh số nguyên tố ngẫu nhiên
def gen_prime_number():
    prime = gen_big_number(58, 64)
    while not is_prime(prime):
        prime = gen_big_number(58, 64)
    return prime

# sinh số nguyên tố cùng nguyên tố với phi_n
def gen_coprime(phi_n):
    coprime = random.randint(2, phi_n - 1)
    while math.gcd(coprime, phi_n) != 1:
        coprime = random.randint(2, phi_n - 1)
    return coprime

# phương pháp euclid mở rộng
def extended_euclidean(a, b):
    if a == 0:
        return b, 0, 1
    d, x1, y1 = extended_euclidean(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return d, x, y

# tính mô đun nghịch đảo bằng pp Euclid mở rộng
def modular_inverse(a, m):
    if math.gcd(a, m) != 1:
        raise ValueError("Không tìm thấy nghịch đảo mô đun với a và m đã cho.")
    _, x, _ = extended_euclidean(a, m)
    return x % m

# phát sinh cặp khoá Kprivate và Kpublic cho thuật toán RSA
def gen_rsa_keypair():
    p = gen_prime_number()
    q = gen_prime_number()
    
    n = p * q
    
    phi_n = (p - 1) * (q - 1)
    
    e = gen_coprime(phi_n)
    
    d = modular_inverse(e, phi_n)
    
    Kprivate = (d, n)
    Kpublic = (e, n)    
    return Kprivate, Kpublic

def rsa_encrypt_string(message, e, n):
    plaintext = [ord(char) for char in message]  # Chuyển đổi chuỗi thành danh sách các giá trị mã ASCII
    ciphertext = [str(pow(char, e, n)) for char in plaintext]  # Mã hoá từng giá trị mã ASCII
    return ' '.join(ciphertext)  # Kết hợp các giá trị mã hoá thành một chuỗi

def rsa_decrypt_string(ciphertext, d, n):
    encrypted_values = ciphertext.split(' ')  # Tách chuỗi mã hoá thành danh sách các giá trị mã hoá
    decrypted_values = [pow(int(char), d, n) for char in encrypted_values]  # Giải mã từng giá trị mã hoá
    plaintext = ''.join([chr(decrypted_char) for decrypted_char in decrypted_values])  # Chuyển đổi thành chuỗi gốc
    return plaintext