import shlex


def prs_cmd(line):
    try:
        return shlex.split(line)
    except ValueError as e:
        print(f"Ошибка парсинга: {e}")
        return []

def execute_cmd(cmd, args):
    """Выполняет команду и выводит результат"""
    if cmd == "exit":
        return True   # exit
    elif cmd in ["ls", "cd"]:
        print(f"[Заглушка] {cmd}: {args}")
    else:
        print(f"Неизвестная команда: {cmd}")
    return False


def run_mode(vfs_name):
    """Интерактивный режим работы консольного приложения"""
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

def main():
    vfs_name = "my_vfs"


if __name__ == "__main__":
    main()