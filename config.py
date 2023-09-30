import os
from cryptography.fernet import Fernet

def get_rd_api():
    if os.path.exists("fernet.key"):
        with open("fernet.key", "rb") as file:
            key = file.read()
    else: 
        key = Fernet.generate_key()
        with open("fernet.key", "wb") as file:
            file.write(key)

    if os.path.exists("api.key"):
        with open("api.key", "rb") as file:
            encrypted_rd_api = file.read()
    else:
        print("\nIt seems that your API key is not known by the application, please provide it.\n")
        rd_api = input("RD API key: ").encode()

        with open("fernet.key", "rb") as file:
            key = file.read()
            f = Fernet(key)

        encrypted_rd_api = f.encrypt(rd_api)
        with open("api.key", "wb") as file:
            file.write(encrypted_rd_api)

    f = Fernet(key)
    rd_api = f.decrypt(encrypted_rd_api).decode('utf-8')

    return rd_api


def get_media_root():
    if os.path.exists("root_path"):
        with open("root_path", "r") as file:
            root_path = file.read()
    else:
        root_path = input("It seems that the media library path is not known by the application. Please provide the media library path. Example E:\Plex : ")
    
    with open("root_path", "w") as file:
        file.write(root_path)

    return root_path