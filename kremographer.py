import os
import argparse
import re
import getpass
import sys
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

__version__ = "1.0.0"

STRING_SEPARATION = "\n------------------------------------------------------------------------------\n"
SALT_LEN = 16
NONCE_LEN = 12
ITERATIONS = 390000 # standard PBKDF2 hashing iterations


def read_file(file_path):
    """Reads file contents as bytes.
    Parameters: input file path(str)."""
    with open(file_path, "rb") as file:
        return file.read() 

def write_file(file_path, data):
    """Writes file content as bytes.
    Parameters: input file path(str), data to be written(bytes)."""
    with open(file_path, "wb") as file:
        file.write(data)

def get_key(salt, password):
    """Generates a 32-byte AES-256 key using PBKDF2-HMAC-SHA256.
    Parameters: randomly generated salt(bytes), user-supplied password(str)."""
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length = 32, salt=salt, iterations=ITERATIONS)
    key = kdf.derive(password.encode("utf-8"))
    return key 

def encrypt_file(password, in_fpath, out_fpath):
    """Encrypts a file.
    Parameters: user-supplied password(str), input file path(str), output encrypted file path(str)."""

    salt = os.urandom(SALT_LEN) # 16 byte random salt for pbkdf2
    nonce=os.urandom(NONCE_LEN)
    aesgcm=AESGCM(get_key(salt, password))    
    encrypted_text = aesgcm.encrypt(nonce, read_file(in_fpath), None)

    if os.path.exists(out_fpath):
        confirmation = input(f"{STRING_SEPARATION}File {out_fpath} already exists. Overwrite? (y/n): ")
        if confirmation != "y":
            print(f"{STRING_SEPARATION}Encryption cancelled.{STRING_SEPARATION}")
            return

    write_file(out_fpath, salt+nonce+encrypted_text)

    print(f"{STRING_SEPARATION}File encrypted --> {out_fpath}{STRING_SEPARATION}")

def decrypt_file(password, in_fpath, out_fpath):
    """Decrypts an encrypted file.
    Parameters: user-supplied password(str), encrypted file path(str), output decrypted file path(str)."""
    combined_binary = read_file(in_fpath)
    salt = combined_binary[:SALT_LEN]
    nonce = combined_binary[SALT_LEN:SALT_LEN+NONCE_LEN]
    ciphertext = combined_binary[SALT_LEN+NONCE_LEN:]
    key = get_key(salt, password)
    aesgcm = AESGCM(key)
    try:
        decrypted_text = aesgcm.decrypt(nonce, ciphertext, None)
    except InvalidTag:
        print(f"{STRING_SEPARATION}Decryption unsuccessful: Corrupted file or wrong password.\nEnsure you are using the correct password and decrypting the right file.{STRING_SEPARATION}")
        return
    
    if os.path.exists(out_fpath):
        confirmation = input(f"{STRING_SEPARATION}File {out_fpath} already exists. Overwrite? (y/n): ")
        if confirmation != "y":
            print(f"{STRING_SEPARATION}Decryption cancelled.{STRING_SEPARATION}")
            return
        
        
    write_file(out_fpath, decrypted_text)

    print(f"{STRING_SEPARATION}File decrypted --> {out_fpath}{STRING_SEPARATION}")    


def pass_is_valid(password):
    """Ensure user created password conforms with password security protocols.
    Parameters: user-supplied password(str)"""
    if not(
        len(password)>=12 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"\d", password) and
        re.search(r"[^A-Za-z0-9]", password)
    ):
        print(f"{STRING_SEPARATION}ERROR: Invalid password\n\nPassword requirements:\n- 12 characters minimum\n- At least 1 capital letter\n- At least 1 lower case letter\n- At least 1 number\n- At least 1 special character\n{STRING_SEPARATION}")
        return False
    else:
        return True

def main():

    # argparse 
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="Kremographer — A command-line tool for secure AES-256-GCM file encryption "
                                     "and decryption using password-based key derivation (PBKDF2-HMAC-SHA256).")
    
    #version
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.epilog = (
        "Examples:\n"
        "kremographer encrypt my_file.txt my_file.enc\n"
        "kremographer decrypt my_file.enc my_file_decrypted.txt\n"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # encrypt parser
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a file using AES-256-GCM encryption")
    encrypt_parser.add_argument("input", help="Path to the file to encrypt")
    encrypt_parser.add_argument("output", help="Path to save the encrypted file")

    #decrypt parser
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt an encrypted (.enc) file using your password")
    decrypt_parser.add_argument("input", help="Path to the encrypted (.enc) file ")
    decrypt_parser.add_argument("output", help="Path to save the decrypted output file")

    
    args = parser.parse_args()


    # deal with case of non-existent file
    if not os.path.exists(args.input):
            print(f"{STRING_SEPARATION}ERROR: File {args.input} doesn't exist. {STRING_SEPARATION}")
            sys.exit(1)

    # deal with case of empty file on either operation
    operation = args.command
    if os.path.getsize(args.input) == 0:
                print(f"{STRING_SEPARATION}ERROR: File is empty, nothing to {operation}.{STRING_SEPARATION}")
                sys.exit(1)

    while True:

        if args.command == "encrypt":
            password1 = getpass.getpass("Please create a password: ")
            if not pass_is_valid(password1):
                continue
            password2 = getpass.getpass("Please re-enter your password: ")
            if password1==password2:
                password = password1
                break
            else:
                print(f"{STRING_SEPARATION}ERROR: Passwords do not match.{STRING_SEPARATION}")
                continue
        elif args.command == "decrypt":
            password = getpass.getpass("Enter your password for decryption: ")
            break


    if args.command == "encrypt":
        encrypt_file(password, args.input, args.output)

    elif args.command == "decrypt":
        decrypt_file(password, args.input, args.output)



if __name__ == "__main__":
    main()