# 🔒 Kremographer

**AES-GCM File Encryption/Decryption CLI Tool**

Kremographer is a lightweight, command-line tool for encrypting and decrypting files using the AES-GCM (Galois/Counter Mode) encryption standard.  
It provides cryptographic protection, password-based key derivation (PBKDF2-HMAC-SHA256), and simple usability from your terminal.

---

## ✨ Features

- 🔐 AES-256-GCM authenticated encryption  
- 🧂 Random salt & nonce generation per file  
- 🔑 Password-based key derivation using PBKDF2-HMAC-SHA256  
- 🚫 Passwords never stored or logged  
- ⚙️ Command-line interface for quick use  
- 🧰 Cross-platform (Linux, macOS, Windows)  
- 🧾 MIT licensed, open-source

---

## 📦 Installation

Install Kremographer directly from [PyPI](https://pypi.org/project/kremographer/):

    pip install kremographer

After installation, you’ll have a CLI command available globally:

    kremographer --help

---

## 🧭 Usage

### 🔹 Encrypt a file

    kremographer encrypt <input_file> <output_file>

Example:

    kremographer encrypt notes.txt notes.enc

You’ll be prompted to create and confirm a secure password.  
Passwords must include:
- At least 12 characters  
- 1 uppercase letter  
- 1 lowercase letter  
- 1 number  
- 1 special character  

---

### 🔹 Decrypt a file

    kremographer decrypt <encrypted_file> <output_file>

Example:

    kremographer decrypt notes.enc notes.txt

You’ll be prompted for your password.  
If the password or file is incorrect, decryption will fail safely.

---

## 🧩 Example session

    $ kremographer encrypt practice.txt practice.enc
    Please create a password: **************
    Please re-enter your password: **************
    -----------------------------------------------------------
    File encrypted --> practice.enc
    -----------------------------------------------------------

    $ kremographer decrypt practice.enc practice_decrypted.txt
    Enter your password for decryption: **************
    -----------------------------------------------------------
    File decrypted --> practice_decrypted.txt
    -----------------------------------------------------------

---

## ⚠️ Notes

- If the output file already exists, you’ll be prompted before overwriting.  
- Each encryption generates a **unique salt and nonce**, ensuring strong cryptographic safety.  
- Passwords are never stored or written to disk — only used to derive a temporary encryption key.  
- Losing your password means your data **cannot** be recovered.

---

## 🛠️ Dependencies

- cryptography >= 42.0  
- Python >= 3.8

---

## 📜 License

This project is licensed under the MIT License.  
Copyright © 2025 **Kareem Mahfouf**

---

## 💡 About

Kremographer was built as a simple yet secure way to handle file encryption using modern cryptographic standards.  
Perfect for learning, research, or real-world file protection.

---

### 🧠 Future ideas
- Directory-wide encryption support  
- Configurable password policies  
- Optional integrity verification mode  
- GUI frontend

---

**Disclaimer:**  
Kremographer is an open-source tool that uses industry-standard encryption (AES-GCM via the Python `cryptography` library).  
While it implements strong cryptographic practices, no software can guarantee absolute security.  
Use at your own risk.


_Developed with ❤️ by Kareem Mahfouf_
