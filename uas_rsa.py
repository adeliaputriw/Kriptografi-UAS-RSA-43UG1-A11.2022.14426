# -*- coding: utf-8 -*-
"""UAS RSA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ktlzwMcXdCQr9j12xnHkG390hxwJdLmI
"""

import random
import math

# Fungsi untuk mengecek apakah suatu bilangan merupakan bilangan prima
def is_prime(number):
    if number < 2:
        return False
    for i in range(2, number // 2 + 1):
        if number % i == 0:
            return False
    return True

# Fungsi untuk mengecek apakah suatu bilangan merupakan bilangan prima
def get_prime_input(message):
    while True:
        try:
            user_input = int(input(message))
            if is_prime(user_input):
                return user_input
            else:
                print("Input is not a prime number. Try again.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

# Fungsi untuk mencari nilai d (private key) dari nilai e (public key) dan totient n
def mod_inverse(e, totient):
    for d in range(3, totient):
        if (d * e) % totient == 1:
            return d
    raise ValueError('No mod inverse for e: %d, totient: %d' % (e, totient))

def make_key():
    p = get_prime_input("Enter a prime number (p): ")
    q = get_prime_input("Enter a prime number (q): ")

    # p dan q tidak boleh sama
    while p == q:
        print("p and q cannot be the same number. Try again.")
        p = get_prime_input("Enter a prime number (p): ")
        q = get_prime_input("Enter a prime number (q): ")

    # nilai n adalah hasil perkalian p dan q dan boleh dibagikan
    n = p * q
    # nilai totient n adalah hasil perkalian p-1 dan q-1 tidak boleh dibagikan karena untuk mencari nilai d
    totient_n = (p - 1) * (q - 1)

    # nilai e adalah nilai yang tidak boleh dibagikan dan harus lebih besar dari 2 dan lebih kecil dari Pembagi persekutuan terbesar / GCD
    e = int(input(f"Enter a public exponent (e) such that 2 < e < {totient_n} and gcd(e, {totient_n}) = 1: "))

    while not (1 < e < totient_n and math.gcd(e, totient_n) == 1):
        print(f"Invalid value for e. Try again.")
        e = int(input(f"Enter a public exponent (e) such that 2 < e < {totient_n} and gcd(e, {totient_n}) = 1: "))

    d = mod_inverse(e, totient_n)

    print("Public key (e, n): ", e, n)
    print("Private key (d, n): ", d, n)


def encryption_menu():
    n = int(input("Masukan nilai n: "))
    e = int(input("Masukan kunci public e: "))
    input_path = input("Masukkan path file untuk dienkripsi (contoh: hasil_encoding.txt): ")
    process_path = input("Masukkan path untuk menyimpan process enkripsi (contoh: process_enkripsi.txt): ")
    output_path = input("Masukkan path untuk menyimpan hasil enkripsi (contoh: hasil_enkripsi.txt): ")

    with open(input_path, 'r') as file:
        # Baca seluruh konten file
        message = file.read()

    # Mengubah pesan menjadi nilai ASCII dan enkripsi
    ciphertext = []
    max_digit = 0
    values = []

    # Open the file in append mode
    with open(process_path, "a") as base64_file:
        # Iterate through each character in the message
        for i in range(0, len(message)):
            block = message[i]
            encoded_block = ord(block)  # Convert character to ASCII value
            encrypted_block = pow(encoded_block, e, n)

            # Append the value to the list
            values.append(encrypted_block)

            # Write the details of the current block to the file
            base64_file.write(f"Block '{block}' is {encoded_block}, {encoded_block}^{e} mod {n} is {encrypted_block}\n")

            current_digit = len(str(encrypted_block))
            max_digit = max(max_digit, current_digit)
            ciphertext.append(encrypted_block)

    ciphertext_str = ''.join([str(block).zfill(max_digit) for block in ciphertext])

     # Simpan hasil enkripsi ke dalam file teks
    with open(output_path, "w") as base64_file:
        base64_file.write(ciphertext_str)
        print("Sukses! Hasil enkripsi tersimpan")

    return max_digit


def decryption_menu(max_digit):
    n = int(input("Masukan nilai n: "))
    d = int(input("Masukan kunci private d: "))
    input_path = input("Masukkan path file untuk didekripsi (contoh: hasil_enkripsi.txt): ")
    process_path = input("Masukkan path untuk menyimpan process dekripsi (contoh process_dekripsi.txt): ")
    output_path = input("Masukkan path untuk menyimpan hasil dekripsi (contoh: hasil_dekripsi.txt): ")

    with open(input_path, 'r') as file:
        # Baca seluruh konten file
        isi_file = file.read()

    ciphertext_str = isi_file

    # Split ciphertext into blocks of size max_digit
    ciphertext_blocks = [int(ciphertext_str[i:i + max_digit]) for i in range(0, len(ciphertext_str), max_digit)]

    decrypted_message = ""

    values = []

    # Open the file in append mode
    with open(process_path, "a") as base64_file:
        # Iterate through each block in the ciphertext
        for block in ciphertext_blocks:
            decrypted_block = pow(block, d, n)
            decrypted_char = chr(decrypted_block)  # Convert ASCII value to character

            # Append the value to the list
            values.append(decrypted_block)

            # Write the details of the current block to the file
            base64_file.write(f"{block}^{d} mod {n} is {decrypted_block} which is '{decrypted_char}'\n")

            decrypted_message += decrypted_char

    # Simpan hasil dekripsi ke dalam file teks
    with open(output_path, "w") as base64_file:
        base64_file.write(decrypted_message)
        print("Sukses! Hasil dekripsi tersimpan")

# Fungsi untuk menghitung totient n dari dua bilangan prima p dan q
def calculate_totient(p, q):
    return (p - 1) * (q - 1)

# Fungsi untuk mencari bilangan prima yang relatif prima terhadap totient n
def generate_coprime(num_digits, totient_n):
    while True:
        random_prime = generate_random_prime(num_digits)
        if math.gcd(random_prime, totient_n) == 1:
            return random_prime


# Fungsi untuk mengenerate bilangan prima dengan jumlah digit yang diinginkan
def generate_random_prime(num_digits):
    min_value = 10 ** (num_digits - 1)
    max_value = (10 ** num_digits) - 1

    while True:
        random_prime = random.randint(min_value, max_value)
        if is_prime(random_prime):
            return random_prime

# Fungsi untuk menampilkan menu bilangan prima custom
def custom_prime_menu():
    num_digits = input("Masukkan jumlah digit bilangan prima yang diinginkan: ")
    # generate bilangan prima dengan jumlah digit yang diinginkan
    prime1 = generate_random_prime(int(num_digits))
    prime2 = generate_random_prime(int(num_digits))

    if prime1 is not None and prime2 is not None:
        print(f"Bilangan prima dengan {num_digits} digit (p): {prime1}")
        print(f"Bilangan prima dengan {num_digits} digit (q): {prime2}")
        totient_n = calculate_totient(prime1, prime2)
        e = generate_coprime(int(num_digits), totient_n)

        print(f"Totient n: {totient_n}")
        print(f"Bilangan prima relatif prima terhadap totient n (e): {e}")
    else  :
        print(f"Tidak ada bilangan prima dengan {num_digits} digit")


if __name__ == "__main__":
    max_digit = 3  # Initialize max_digit outside the loop
    while True:
        print("\nMenu:")
        print("1. Make keys")
        print("2. Encryption")
        print("3. Decryption")
        print("4. Custom Prime")
        print("5. Exit")

        choice = input("Enter your choice (1, 2, 3, 4, or 5): ")
        if choice == '1':
            make_key()  # Capture max_digit from make_key
        elif choice == '2':
            max_digit = encryption_menu()
        elif choice == '3':
            decryption_menu(max_digit)  # Pass max_digit to decryption_menu
        elif choice == '4':
            custom_prime_menu()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, or 5")