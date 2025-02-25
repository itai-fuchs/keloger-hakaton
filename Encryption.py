from cryptography.fernet import Fernet
import psutil

class EncryptionClient:
    def __init__(self):
        self.MAC = self.get_mac_address()
        print("MAC Address: ", self.MAC)

        # מפתח קבוע מראש להצפנה
        self.KEY = b'K9fT3NQh5z8PZpLTWBcmLPqXEjLJd5mQXMbbZ7VhG4k='
        print("Encryption Key: ", self.KEY)

    @staticmethod
    def get_mac_address():
        """ מחזיר את כתובת ה-MAC של כרטיס ה-Wi-Fi """
        addrs = psutil.net_if_addrs()
        for interface, addrs_list in addrs.items():
            if 'Wi-Fi' in interface:
                for addr in addrs_list:
                    if addr.family == psutil.AF_LINK:
                        return addr.address
        return "00:00:00:00:00:00"  # אם לא נמצא MAC, נותנים ברירת מחדל

    def encrypt_text(self, text):
        """ מצפין טקסט באמצעות המפתח הגלובלי """
        cipher_suite = Fernet(self.KEY)
        return cipher_suite.encrypt(text.encode())

# יצירת מופע של המחלקה ובדיקה
client = EncryptionClient()
encrypted_text = client.encrypt_text("Hello, world!")
print("Encrypted:", encrypted_text)
