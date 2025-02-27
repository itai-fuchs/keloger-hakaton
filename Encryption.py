import psutil
import requests
from cryptography.fernet import Fernet


class EncryptionClient:
    def __init__(self,url="http://127.0.0.1:5000"):
        self.backend_url = url
        self.MAC = self.get_mac_address()
        print("mac: ",self.MAC)
        # with open("public_key.asc") as file:
        #     self.KEY, _ = pgpy.PGPKey.from_blob(file.read())
        self.KEY = self.get_key()
        # print("key: ",self.KEY)

    @staticmethod
    def get_mac_address():
        addrs = psutil.net_if_addrs()
        for interface, addrs_list in addrs.items():
            if 'Wi-Fi' in interface:  # בדיקה לפי שם הממשק
                for addr in addrs_list:
                    if addr.family == psutil.AF_LINK:
                        print(f" MAC (Wi-Fi): {addr.address}")
                        return addr.address
        return "WIFI MAC address not found"

    def get_key(self):

        try:
            response = requests.get(f"{self.backend_url}/user/{self.MAC}")
            print(response.json())
            if response.status_code == 200:
                data = response.json()  # Parse JSON response
                data = response.json()
                # Parse JSON response
                return data.get("key")  # Return the encryption key
            else:
                print("The server returned an error:", response.status_code, response.text)

                return None
        except requests.RequestException as e:
            print("Server request error:", e)
            return None
    def encrypt_text(self,arr):
        cipher_suite = Fernet(self.KEY)
        cipher_text = cipher_suite.encrypt(str(arr).encode())
        return cipher_text

    # def encrypt_text(self,arr):
    #     return arr


# testing functions
mac = EncryptionClient()
# print(f"MAC (Wi-Fi): {mac.MAC}")
encrypted = mac.encrypt_text("hello world")
print("מוצפן",encrypted)
# fernet = Fernet(mac.KEY)
# decMessage = fernet.decrypt(encrypted).decode()
# print("מפוענח",decMessage)
