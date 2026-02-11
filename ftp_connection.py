from ftplib import FTP

# Подключение к FTP серверу
ftp = FTP()
ip = input()
if ip == "":
    ip = "192.168.53.164"
ftp.connect(host=ip, port=5001)  # Замените IP на реальный адрес
ftp.login(user='ftpincomsystem', passwd='ftpabak3')  # Пароль не указан

print("✅ Подключение успешно!")
print({ftp.getwelcome()})

# Закрываем соединение
ftp.quit()