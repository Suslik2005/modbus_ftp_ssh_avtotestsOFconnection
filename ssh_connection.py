import paramiko

# Подключение по SSH
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ip = input()
    if ip == "":
        ip = "192.168.53.164"
    ssh.connect(hostname=ip, username='root', password='Cw4pi87OlBJ4S3K4', timeout=5)
    print("✅ Подключение по SSH успешно!")

    # Простая команда для проверки
    stdin, stdout, stderr = ssh.exec_command('whoami')
    print(f"Пользователь: {stdout.read().decode().strip()}")

except Exception as e:
    print(f"❌ Ошибка подключения: {e}")
finally:
    ssh.close()
