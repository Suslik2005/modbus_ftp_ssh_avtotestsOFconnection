from pymodbus.client import ModbusTcpClient
import socket


def test_modbus_connection(ip_address='192.168.53.164', port=502, unit_id=1):
    print(f"Попытка подключения к {ip_address}:{port} (Unit ID: {unit_id})...")

    client = None
    try:
        # 1. Сначала проверим доступность порта
        print("1. Проверка доступности порта...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((ip_address, port))
        sock.close()

        if result != 0:
            print(f"✗ Порт {port} закрыт или недоступен")
            return False
        print(f"✓ Порт {port} открыт")

        # 2. Подключаемся через pymodbus
        print("2. Подключение через Modbus...")
        client = ModbusTcpClient(
            host=ip_address,
            port=port,
            timeout=3
        )

        if not client.connect():
            print("✗ Не удалось подключиться через Modbus клиент")
            return False
        print("✓ Modbus клиент подключен")

        # 3. Пробуем разные варианты вызова
        print("3. Тестирование чтения регистров...")

        # Вариант 1: Без параметра unit/slave (по умолчанию unit=0 или 1)
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
            print("Соединение закрыто")


# Запуск теста
if __name__ == "__main__":
    ip = input()
    if ip == "":
        ip = "192.168.53.164"
    test_modbus_connection(ip, 502, 1)