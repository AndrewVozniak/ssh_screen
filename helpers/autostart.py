import os
import shutil


# os: windows 7,8,10,11
def has_write_permission(folder_path):
    try:
        test_file = os.path.join(folder_path, 'test_permission.tmp')
        with open(test_file, 'w') as tmp_file:
            tmp_file.write('test')
        os.remove(test_file)
        return True
    except Exception as e:
        print(f"Ошибка доступа: {e}")
        return False


# Добавление файла в автозагрузку
def add_to_startup(file_path, startup_path=os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup')):
    if has_write_permission(startup_path):
        shutil.copy(file_path, startup_path)
        return f"Файл '{file_path}' успешно добавлен в автозагрузку."
    else:
        return "Недостаточно прав для добавления файла в автозагрузку."
