from pymodbus.client import ModbusTcpClient
import socket
from ftplib import FTP, error_perm, error_temp, error_reply
import paramiko
import time


def test_modbus_connection(ip_address, port=502, unit_id=1):
    """Тестирование Modbus TCP подключения"""
    print(f"\nТЕСТИРОВАНИЕ MODBUS (порт {port})")
    print("-" * 50)

    client = None
    try:
        # Проверка доступности порта
        print("1. Проверка доступности порта...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((ip_address, port))
        sock.close()

        if result != 0:
            print(f"✗ Порт {port} закрыт или недоступен")
            return False
        print(f"✓ Порт {port} открыт")

        # Подключение через Modbus
        print("2. Подключение через Modbus...")
        client = ModbusTcpClient(
            host=ip_address,
            port=port,
            timeout=3
        )

        if not client.connect():
            print("Не удалось подключиться через Modbus клиент")
            return False
        print("Modbus клиент подключен")

        # Тестирование чтения регистров
        print("3. Тестирование чтения регистров...")

        # Вариант 1: Без параметра unit/slave
        try:
            result = client.read_holding_registers(address=0, count=1)
            if not result.isError():
                print(f"✓ Чтение успешно (по умолчанию unit)")
                print(f"  Регистр 0: {result.registers}")
                return True
        except Exception as e:
            print(f"  Вариант 1: {type(e).__name__}")

        # Вариант 2: С параметром unit
        try:
            result = client.read_holding_registers(address=0, count=1, unit=unit_id)
            if not result.isError():
                print(f"✓ Чтение успешно (unit={unit_id})")
                print(f"  Регистр 0: {result.registers}")
                return True
        except Exception as e:
            print(f"  Вариант 2: {type(e).__name__}")

        # Вариант 3: С параметром slave
        try:
            result = client.read_holding_registers(address=0, count=1, slave=unit_id)
            if not result.isError():
                print(f"✓ Чтение успешно (slave={unit_id})")
                print(f"  Регистр 0: {result.registers}")
                return True
        except Exception as e:
            print(f"  Вариант 3: {type(e).__name__}")

        print("✗ Все варианты чтения не сработали")
        return False

    except socket.timeout:
        print("✗ Таймаут подключения")
        return False
    except socket.error as e:
        print(f"✗ Ошибка сокета: {e}")
        return False
    except Exception as e:
        print(f"✗ Общая ошибка: {type(e).__name__}: {e}")
        return False
    finally:
        if client:
            client.close()
            print("Соединение Modbus закрыто")


def test_ftp_connection(ip_address, port=5001, username='ftpincomsystem', password='ftpabak3'):
    """Тестирование FTP подключения"""
    print(f"\n📁 ТЕСТИРОВАНИЕ FTP (порт {port})")
    print("-" * 50)

    ftp = None
    try:
        # Проверка доступности порта
        print("1. Проверка доступности порта...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((ip_address, port))
        sock.close()

        if result != 0:
            print(f"✗ Порт {port} закрыт или недоступен")
            return False
        print(f"✓ Порт {port} открыт")

        # Подключение к FTP
        print("2. Подключение к FTP серверу...")
        ftp = FTP()
        ftp.connect(host=ip_address, port=port, timeout=5)
        print("✓ TCP соединение установлено")

        # Логин
        print("3. Авторизация...")
        try:
            ftp.login(user=username, passwd=password)
            print(f"Авторизация успешна")
            print(f"  Приветствие: {ftp.getwelcome()}")

            # Дополнительная проверка - получение списка файлов
            try:
                files = ftp.nlst()
                print(f"  Список файлов/папок: {len(files)} элементов")
            except:
                print("  Не удалось получить список файлов")

            return True

        except error_perm as e:
            print(f"✗ Ошибка авторизации (неверный логин/пароль): {e}")
            return False
        except Exception as e:
            print(f"✗ Ошибка при логине: {e}")
            return False

    except socket.timeout:
        print("✗ Таймаут подключения")
        return False
    except ConnectionRefusedError:
        print("✗ Соединение отклонено (сервер не принимает подключения)")
        return False
    except Exception as e:
        print(f"✗ Ошибка подключения: {type(e).__name__}: {e}")
        return False
    finally:
        if ftp:
            try:
                ftp.quit()
                print("Соединение FTP закрыто")
            except:
                ftp.close()
                print("Соединение FTP принудительно закрыто")


def test_ssh_connection(ip_address, port=22, username='root', password='Cw4pi87OlBJ4S3K4'):
    """Тестирование SSH подключения"""
    print(f"ТЕСТИРОВАНИЕ SSH (порт {port})")
    print("-" * 50)

    ssh = None
    try:
        # Проверка доступности порта
        print("1. Проверка доступности порта...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((ip_address, port))
        sock.close()

        if result != 0:
            print(f"✗ Порт {port} закрыт или недоступен")
            return False
        print(f"✓ Порт {port} открыт")

        # Подключение по SSH
        print("2. Подключение к SSH серверу...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname=ip_address,
            port=port,
            username=username,
            password=password,
            timeout=5,
            allow_agent=False,
            look_for_keys=False
        )
        print("Подключение установлено")

        # Проверка выполнения команды
        print("3. Выполнение тестовой команды...")
        try:
            stdin, stdout, stderr = ssh.exec_command('whoami')
            exit_status = stdout.channel.recv_exit_status()

            if exit_status == 0:
                username_output = stdout.read().decode().strip()
                print(f"  ✓ Команда выполнена успешно")
                print(f"  Пользователь: {username_output}")

                # Дополнительная информация о системе
                stdin, stdout, stderr = ssh.exec_command('uname -a')
                system_info = stdout.read().decode().strip()
                print(f"  Система: {system_info[:100]}...")

                return True
            else:
                error = stderr.read().decode().strip()
                print(f"✗ Ошибка выполнения команды: {error}")
                return False

        except Exception as e:
            print(f"Ошибка выполнения команды: {e}")
            return False

    except paramiko.AuthenticationException:
        print("✗ Ошибка аутентификации (неверный логин/пароль)")
        return False
    except paramiko.SSHException as e:
        print(f"✗ Ошибка SSH протокола: {e}")
        return False
    except socket.timeout:
        print("✗ Таймаут подключения")
        return False
    except ConnectionRefusedError:
        print("✗ Соединение отклонено (сервер не принимает подключения)")
        return False
    except Exception as e:
        print(f"✗ Ошибка подключения: {type(e).__name__}: {e}")
        return False
    finally:
        if ssh:
            ssh.close()
            print("Соединение SSH закрыто")


def test_all_connections(ip_address):
    """Тестирование всех протоколов одновременно"""
    print(f"\n{'=' * 60}")
    print(f"НАЧАЛО ТЕСТИРОВАНИЯ ПОДКЛЮЧЕНИЙ К {ip_address}")
    print(f"{'=' * 60}\n")

    results = {}

    # Тестирование Modbus
    results['modbus'] = test_modbus_connection(ip_address)
    time.sleep(1)  # Небольшая пауза между тестами

    # Тестирование FTP
    results['ftp'] = test_ftp_connection(ip_address)
    time.sleep(1)

    # Тестирование SSH
    results['ssh'] = test_ssh_connection(ip_address)

    # Вывод сводки
    print(f"\n{'=' * 60}")
    print("Результаты:")
    print(f"{'=' * 60}")
    print(f"Modbus: {'УСПЕШНО' if results['modbus'] else 'ОШИБКА'}")
    print(f"FTP:    {'УСПЕШНО' if results['ftp'] else 'ОШИБКА'}")
    print(f"SSH:    {'УСПЕШНО' if results['ssh'] else 'ОШИБКА'}")
    print(f"{'=' * 60}")

    return results


def main():
    """Основная функция"""
    print("=" * 60)
    print("ПРОГРАММА ТЕСТИРОВАНИЯ СЕТЕВЫХ ПРОТОКОЛОВ")
    print("=" * 60)

    # Запрос IP-адреса
    ip = input("\nВведите IP-адрес устройства (Enter для использования 192.168.53.164): ").strip()
    if not ip:
        ip = "192.168.53.164"
        print(f"Используется IP по умолчанию: {ip}")

    # Запрос на выбор протоколов
    print("\nВыберите протоколы для тестирования:")
    print("1. Только Modbus")
    print("2. Только FTP")
    print("3. Только SSH")
    print("4. Все протоколы")

    choice = input("Ваш выбор (1-5): ").strip()

    if choice == '1':
        test_modbus_connection(ip)
    elif choice == '2':
        test_ftp_connection(ip)
    elif choice == '3':
        test_ssh_connection(ip)
    elif choice == '4':
        test_all_connections(ip)
    else:
        print("Неверный выбор. Тестируем все протоколы.")
        test_all_connections(ip)


if __name__ == "__main__":
    main()