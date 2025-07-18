# -*- coding: utf-8 -*-
"""Steganography.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ERONb5pnVPaRgOv5tzPtRqKeEW5M5FGP
"""

#pip install opencv-python numpy cryptography



import cv2
import numpy as np
from cryptography.fernet import Fernet
import traceback

def encrypt_message(message, cipher):
    return cipher.encrypt(message.encode())

def decrypt_message(encrypted_data, key):
    return Fernet(key).decrypt(encrypted_data).decode()

def embed_data(image_path, output_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Image not found.")

    # Generate secure key
    key = Fernet.generate_key()
    cipher = Fernet(key)

    message = input("Enter secret message: ")
    encrypted = encrypt_message(message, cipher)
    binary = ''.join(format(byte, '08b') for byte in encrypted)

    print(f"\nEncrypted length (for extraction): {len(encrypted)} bytes")

    rows, cols, _ = img.shape
    if len(binary) > rows * cols * 3:
        raise ValueError("Message too large for this image.")

    data_index = 0
    for i in range(rows):
      for j in range(cols):
        for k in range(3):
            if data_index < len(binary):
                pixel_val = int(img[i, j, k])
                img[i, j, k] = int((pixel_val & ~1) | int(binary[data_index]))
                data_index += 1
            else:
                break


    cv2.imwrite(output_path, img)
    print("\nMessage embedded successfully.")
    print("Output image saved as:", output_path)
    print("Save this key:", key.decode())
    print("Save this message_length:", len(encrypted))

def extract_data(image_path, key_str, message_length):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Image not found.")

    key = key_str.strip("'\"").encode()  # Clean up key input

    rows, cols, _ = img.shape
    total_bits = message_length * 8
    binary_data = ""

    for i in range(rows):
        for j in range(cols):
            for k in range(3):
                binary_data += str(img[i, j, k] & 1)
                if len(binary_data) >= total_bits:
                    break
            if len(binary_data) >= total_bits:
                break
        if len(binary_data) >= total_bits:
            break

    byte_data = bytearray()
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i + 8]
        if len(byte) == 8:
            byte_data.append(int(byte, 2))

    try:
        decrypted = decrypt_message(bytes(byte_data), key)
        print("\nDecrypted Message:", decrypted)
    except Exception:
        print("\nDecryption failed. Reason:")
        traceback.print_exc()

# ===========================
# Main Program with Menu
# ===========================
def main():
    print("Image Steganography Tool")
    print("1. Embed a secret message")
    print("2. Extract a secret message")
    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        embed_data("C:/Users/yuva2/OneDrive/Desktop/Projects/Steganography_with_Encryption/input_image.png", "output_image.png")
    elif choice == '2':
        key = input("Enter the saved key: ")
        length = int(input("Enter the encrypted message length: "))
        extract_data("output_image.png", key, length)
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()