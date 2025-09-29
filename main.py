import shlex
import argparse
import VFS

#   scripts/test_3_3.bat

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
        print(cmd,*args)
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
            print("\nЗавершаем...")
            break


def run_script(script_path, vfs_name):
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Файл '{script_path}' не найден")
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

    parser = argparse.ArgumentParser(description="эмулятор unix-os")
    parser.add_argument("--vfs-path", required=True, help="Путь к VFS")
    parser.add_argument("--script", help="Путь к стартовому скрипту")

    args = parser.parse_args()

    print(f"\tVFS: {args.vfs_path}")
    print(f"\tСкрипт: {args.script}\n")


    vfs = VFS.VirtualFileSystem(args.vfs_path)

    if args.script:
        run_script(args.script, vfs)
    else:
        run_mode(vfs)

    if args.script:
        run_script(args.script, vfs_name)
    else:
        run_mode(vfs_name)


if __name__ == "__main__":
    main()