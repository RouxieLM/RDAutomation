import os
from cryptography.fernet import Fernet

def get_rd_api():
    # Check if the 'fernet.key' file exists
    if os.path.exists("fernet.key"):
        # If it exists, read the encryption key from the file
        with open("fernet.key", "rb") as file:
            key = file.read()
    else: 
        # If 'fernet.key' doesn't exist, generate a new encryption key
        key = Fernet.generate_key()
        # Write the newly generated key to 'fernet.key' for future use
        with open("fernet.key", "wb") as file:
            file.write(key)

    # Check if the 'api.key' file exists
    if os.path.exists("api.key"):
        # If it exists, read the encrypted rd_api from the file
        with open("api.key", "rb") as file:
            encrypted_rd_api = file.read()
    else:
        # If 'api.key' doesn't exist, prompt the user to enter the RD API key
        print("\nIt seems that your API key is not known by the application, please provide it.\n")
        rd_api = input("RD API key: ").encode()

        # Read the encryption key from 'fernet.key'
        with open("fernet.key", "rb") as file:
            key = file.read()
            # Create a Fernet cipher using the encryption key
            f = Fernet(key)
        # Encrypt the user-provided RD API key
        encrypted_rd_api = f.encrypt(rd_api)
        # Write the encrypted RD API key to 'api.key' for future use
        with open("api.key", "wb") as file:
            file.write(encrypted_rd_api)

    # Create a Fernet cipher using the encryption key
    f = Fernet(key)
    # Decrypt the encrypted RD API key and decode it to UTF-8
    rd_api = f.decrypt(encrypted_rd_api).decode('utf-8')

    # Return the decrypted RD API key as a string
    return rd_api


def get_media_root():
    # Check if the 'root_path' folder exists
    if os.path.exists("root_path"):
        # If it exists, read the media library path from the file
        with open("root_path", "r") as file:
            root_path = file.read()
    else:
        # If 'root_path' doesn't exist, prompt the user to enter the media library path
        root_path = input("It seems that the Plex path is not known by the application. Please provide the media library path. Example E:\Plex : ")
    
    # Write the provided or read Plex media library path to 'plex_path' file for future use
    with open("root_path", "w") as file:
        file.write(root_path)