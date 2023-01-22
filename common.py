from cryptography.fernet import Fernet


class CommonClass:
    def __init__(self):
        self.db_key = 'IlM8uJLBvLAEYt4vlM4T8c99KMIvAU7heAI2WPoj61I='

    def encrypt_db(self, dbname_file_name):
        fernet = Fernet(self.db_key)
        with open(dbname_file_name, 'rb') as file:
            original = file.read()
            
        encrypted = fernet.encrypt(original)
        with open(dbname_file_name, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
    
    def decrypt_db(self, dbname_file_name):
        fernet = Fernet(self.db_key)
        with open(dbname_file_name, 'rb') as enc_file:
            encrypted = enc_file.read()
        
        decrypted = fernet.decrypt(encrypted)
        with open(dbname_file_name, 'wb') as dec_file:
            dec_file.write(decrypted)