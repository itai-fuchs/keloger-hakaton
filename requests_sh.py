import psutil
from cryptography.fernet import Fernet
import requests


class EncryptionClient:
    def __init__(self):
        self.MAC = self.get_mac_address()
        self.KEY = self.get_key()
        self.backend_url = "127.0.0.1:5000"

    def get_key(self):
        """
        מתודה זו שולחת את כתובת ה-MAC לשרת ומחזירה את מפתח ההצפנה שהשרת מחזיר.
        """
        try:
            encryption_key = requests.get(f"{self.backend_url}/user/{self.MAC}")
            print(encryption_key)
            if encryption_key:
                self.KEY = encryption_key
                return encryption_key
            else:
                print("השרת לא החזיר מפתח הצפנה")
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
                        print(addr.address)
                        return addr.address
        return "לא נמצאה כתובת MAC עבור Wi-Fi"

    def encrypt_text(self,arr):
        cipher_suite = Fernet(self.KEY)
        cipher_text = cipher_suite.encrypt(arr.encode())
        return cipher_text

# דוגמת שימוש:
if __name__ == "__main__":
    mac = EncryptionClient.get_mac_address()
    print(f"כתובת MAC (Wi-Fi): {mac}")

    key, encrypted = EncryptionClient.encrypt_text(["hello","world"])
    print(f"מפתח הצפנה: {key}")
    print(f"טקסט מוצפן: {encrypted}")
