import psutil
from cryptography.fernet import Fernet
import requests


class EncryptionClient:
    def __init__(self,url="http://127.0.0.1:5000"):
        self.backend_url = url
        self.MAC = self.get_mac_address()
        self.KEY = self.get_key()


    def get_key(self):
        """
        מתודה זו שולחת את כתובת ה-MAC לשרת ומחזירה את מפתח ההצפנה שהשרת מחזיר.
        """
        try:
            response  = requests.get(f"{self.backend_url}/user/{self.MAC}")
            print(response.json())
            if response.status_code == 200:
                data = response.json()  # Parse JSON response
                return data.get("key")  # Return the encryption key
            else:
                print("השרת החזיר שגיאה:", response.status_code, response.text)
                return None
        except requests.RequestException as e:
            print("שגיאה בבקשה לשרת:", e)
            return None



    @staticmethod
    def get_mac_address():
        """
        מחפש את כתובת ה-MAC של ממשק ה-Wi‑Fi.
        """
        addrs = psutil.net_if_addrs()
        for interface, addrs_list in addrs.items():
            if 'Wi-Fi' in interface:  # בדיקה לפי שם הממשק
                for addr in addrs_list:
                    if addr.family == psutil.AF_LINK:
                        print(f" MAC (Wi-Fi): {addr.address}")
                        return addr.address
        return "לא נמצאה כתובת MAC עבור Wi-Fi"

    def encrypt_text(self,arr):
        cipher_suite = Fernet(self.KEY)
        cipher_text = cipher_suite.encrypt(arr.encode())
        return cipher_text

#testing functions
mac = EncryptionClient()
print(f"MAC (Wi-Fi): {mac.MAC}")
encrypted = mac.encrypt_text("hello world")
print("מוצפן",encrypted)
fernet = Fernet(mac.KEY)
decMessage = fernet.decrypt(encrypted).decode()
print("מפוענח",decMessage)
