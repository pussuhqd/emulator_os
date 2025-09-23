import shlex
import argparse

#   scripts/test_2_2.bat

def prs_cmd(line):
    try:
        return shlex.split(line)
    except ValueError as e:
        print(f"Ошибка парсинга: {e}")
        return []

def execute_cmd(cmd, args):
    if cmd == "exit":
        return True   # exit
    elif cmd in ["ls", "cd"]:
        print(f"[Заглушка] {cmd}: {args}")
    else:
        print(f"Неизвестная команда: {cmd}")
    return False

def run_mode(vfs_name):
    print(f"Введите 'exit' для выхода.")
    while True:
        try:
            line = input(f"{vfs_name}$ ").strip()
            if not line:
                continue

            parsed = prs_cmd(line)
            if not parsed:
                continue

            cmd, args = parsed[0], parsed[1:]
            if execute_cmd(cmd, args):
                break

        except KeyboardInterrupt:
            print("\nПолучен сигнал завершения (Ctrl+C). Завершаем...")
            break


def run_script(script_path, vfs_name):
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Ошибка: файл '{script_path}' не найден")
        return
    except Exception as e:
        print(f"Ошибка чтения: {e}")
        return

    print(f"Выполнение: {script_path}")

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        print(f"{vfs_name}$ {line}")  # Имитируем ввод

        parsed = prs_cmd(line)
        if not parsed:
            continue

        cmd, args = parsed[0], parsed[1:]
        if execute_cmd(cmd, args):
            break

def main():
    vfs_name = "my_vfs"

    parser = argparse.ArgumentParser(description="Эмулятор unix-os")
    parser.add_argument("--vfs-path", required=True, help="Путь к VFS")
    parser.add_argument("--script", help="Путь к стартовому скрипту")

    args = parser.parse_args()

    # реализация отладочного вывода
    print("[DEBUG] Запуск с параметрами:")
    print(f"\tVFS: {args.vfs_path}")
    print(f"\tСкрипт: {args.script}")


    if args.script:
        run_script(args.script, vfs_name)
    else:
        run_mode(vfs_name)


if __name__ == "__main__":
    main()