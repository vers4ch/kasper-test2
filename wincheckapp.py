import winreg  # Импортируем модуль winreg для работы с реестром Windows
import sys     # Импортируем модуль sys для работы с системными параметрами

def get_installed_software():
    software_list = []  # Список для хранения информации об установленных программам

    # Пути к ключам реестра, где хранится информация о установленных программах
    key_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",  # Для 64-битных программ
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"  # Для 32-битных программ на 64-битной ОС
    ]
    
    # Проходим по каждому пути в списке ключей реестра
    for key_path in key_paths:
        try:
            # Открываем ключ реестра, указывая путь и права доступа (чтение)
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_READ)
        except WindowsError:
            # Если ключ не найден, пропускаем путь и переходим к следующему
            continue

        # Получаем количество подпапок в текущем ключе
        for i in range(winreg.QueryInfoKey(key)[0]):
            try:
                # Получаем имя текущей подпапки
                subkey_name = winreg.EnumKey(key, i)
                # Открываем подпапку
                subkey = winreg.OpenKey(key, subkey_name)
                
                try:
                    # Пытаемся получить значение "Publisher" (издатель)
                    vendor = winreg.QueryValueEx(subkey, "Publisher")[0]
                except FileNotFoundError:
                    # Если значение не найдено, устанавливаем "Unknown"
                    vendor = "Unknown"
                
                try:
                    # Пытаемся получить значение "DisplayName" (имя программы)
                    product_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                except FileNotFoundError:
                    # Если значение не найдено, пропускаем эту запись
                    continue
                
                try:
                    # Пытаемся получить значение "DisplayVersion" (версия программы)
                    version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                except FileNotFoundError:
                    # Если значение не найдено, устанавливаем "Unknown"
                    version = "Unknown"
                
                # Добавляем информацию о программе в список
                software_list.append(f"{vendor}\t{product_name}\t{version}")
                
            except WindowsError:
                # Если возникла ошибка при доступе к подпапке, пропускаем её
                continue
            finally:
                # Закрываем текущую подпапку, чтобы освободить ресурсы
                winreg.CloseKey(subkey)
        
        # Закрываем текущий ключ, чтобы освободить ресурсы
        winreg.CloseKey(key)
    
    # Возвращаем список установленных программ
    return software_list

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        # Проверяем, что скрипт запущен на платформе Windows
        installed_software = get_installed_software()  # Получаем список установленных программ
        for software in installed_software:
            # Печатаем информацию о каждой программе
            print(software)
    else:
        # Выводим сообщение, если скрипт запущен на не-Windows платформе
        print("Этот скрипт предназначен только для ОС Windows.")
