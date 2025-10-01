import shlex
import argparse
import VFS

#   scripts/test_4.bat

def prs_cmd(line):
    try:
        return shlex.split(line)
    except ValueError as e:
        print(f"Ошибка парсинга: {e}")
        return []

def execute_cmd(cmd, args,vfs):
    if cmd == "exit":
        return True
    elif cmd == "ls":
        path = args[0] if args else ""
        items = vfs.list_directory(path)
        for item in items:
            print(item)
    elif cmd == "cd":
        if not args:
            print("cd: отсутствует аргумент")
            return False
        path = args[0]
        if not vfs.change_directory(path):
            print(f"cd: {path}: Нет такого файла или каталога")
    elif cmd == "cat":
        if not args:
            print("cat: отсутствует аргумент")
            return False
        path = args[0]
        if not path.startswith('/'):
            current_dir = vfs.get_current_path()
            if current_dir == "/":
                full_path = f"/{path}"
            else:
                full_path = f"{current_dir}/{path}"
        else:
            full_path = path

        content = vfs.get_file_content(full_path)
        if content is not None:
            print(content)
        else:
            print(f"cat: {path}: Нет такого файла")

    elif cmd == "tree":
        vfs.show_tree()
    else:
        print(f"Неизвестная команда: {cmd}")
    return False


def run_mode(vfs):
    print(f"Введите 'exit' для выхода.")
    while True:
        try:
            current_path = vfs.get_current_path()  # ✅ Получаем текущий путь из VFS
            line = input(f"{current_path}$ ").strip()
            if not line:
                continue

            parsed = prs_cmd(line)
            if not parsed:
                continue

            cmd, args = parsed[0], parsed[1:]
            if execute_cmd(cmd, args,vfs):
                break

        except KeyboardInterrupt:
            print("\nЗавершаем...")
            break


def run_script(script_path,vfs):
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

        current_path = vfs.get_current_path()
        print(f"{current_path}$ {line}")

        parsed = prs_cmd(line)
        if not parsed:
            continue

        cmd, args = parsed[0], parsed[1:]
        if execute_cmd(cmd, args,vfs):
            break

def main():

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

if __name__ == "__main__":
    main()